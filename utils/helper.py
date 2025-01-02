from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import io
import os
import sys
from pathlib import Path


class OptimalImageField(models.ImageField):
    def __init__(self, 
                 max_length=100,
                 size_threshold_kb=700,  # Default threshold of 700KB
                 max_quality=95,
                 min_quality=50,
                 max_dimensions=(1920, 1080),
                 *args, **kwargs):
        """
        Initialize OptimalImageField with configurable parameters
        
        Args:
            size_threshold_kb: Files larger than this will be compressed (in KB)
            max_quality: Maximum JPEG quality for small images
            min_quality: Minimum JPEG quality for large images
            max_dimensions: Maximum allowed dimensions (width, height)
        """
        self.size_threshold_kb = size_threshold_kb
        self.max_quality = max_quality
        self.min_quality = min_quality
        self.max_dimensions = max_dimensions
        super().__init__(max_length=max_length, *args, **kwargs)

    def _get_file_size_kb(self, file_obj):
        """Get file size in KB"""
        try:
            if hasattr(file_obj, 'seek') and hasattr(file_obj, 'tell'):
                pos = file_obj.tell()
                file_obj.seek(0, os.SEEK_END)
                size_kb = file_obj.tell() / 1024
                file_obj.seek(pos)
                return size_kb
            return file_obj.size / 1024
        except (AttributeError, IOError):
            return 0

    def _calculate_dimensions(self, img):
        """Calculate new dimensions maintaining aspect ratio"""
        original_width, original_height = img.size
        max_width, max_height = self.max_dimensions
        
        # If image is smaller than max dimensions, return original size
        if original_width <= max_width and original_height <= max_height:
            return original_width, original_height

        # Calculate ratios
        width_ratio = max_width / original_width
        height_ratio = max_height / original_height
        ratio = min(width_ratio, height_ratio)

        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)

        return new_width, new_height

    def _optimize_quality(self, img, target_size_kb):
        """Binary search for optimal quality to reach target size"""
        quality_min = self.min_quality
        quality_max = self.max_quality
        best_quality = quality_max
        best_size = float('inf')
        best_buffer = None

        while quality_min <= quality_max:
            current_quality = (quality_min + quality_max) // 2
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=current_quality, optimize=True)
            current_size = buffer.tell() / 1024

            if abs(current_size - target_size_kb) < abs(best_size - target_size_kb):
                best_quality = current_quality
                best_size = current_size
                best_buffer = buffer

            if current_size > target_size_kb:
                quality_max = current_quality - 1
            else:
                quality_min = current_quality + 1

        return best_buffer, best_quality, best_size

    def process_image(self, image_file):
        """Process image based on size and format"""
        original_size_kb = self._get_file_size_kb(image_file)
        
        # Open image and get info
        img = Image.open(image_file)
        original_format = img.format
        original_mode = img.mode
        
        # Convert RGBA/P to RGB if needed
        if original_mode in ['RGBA', 'P']:
            img = img.convert('RGB')
        
        # Calculate new dimensions if needed
        new_width, new_height = self._calculate_dimensions(img)
        if (new_width, new_height) != img.size:
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # If image is already small enough and doesn't need format conversion
        if original_size_kb <= self.size_threshold_kb and original_format == 'JPEG':
            output = io.BytesIO()
            img.save(output, format='WEBP', quality=self.max_quality)
            output.seek(0)
            
            return self._create_file(
                output, 
                image_file.name,
                {
                    'action': 'preserved',
                    'original_size_kb': original_size_kb,
                    'final_size_kb': self._get_file_size_kb(output),
                    'quality': self.max_quality,
                    'dimensions': f"{new_width}x{new_height}",
                    'resized': (new_width, new_height) != img.size
                }
            )
        
        # Compress image if needed
        output, quality, final_size = self._optimize_quality(img, self.size_threshold_kb)
        output.seek(0)
        
        return self._create_file(
            output,
            image_file.name,
            {
                'action': 'compressed',
                'original_size_kb': original_size_kb,
                'final_size_kb': final_size,
                'quality': quality,
                'dimensions': f"{new_width}x{new_height}",
                'resized': (new_width, new_height) != img.size
            }
        )

    def _create_file(self, buffer, original_name, info):
        """Create new file with processing info"""
        # Generate appropriate filename
        name_root = Path(original_name).stem
        if info['action'] == 'compressed':
            new_name = f"{name_root}.webp"
        else:
            new_name = f"{name_root}.webp"

        file = InMemoryUploadedFile(
            buffer,
            'ImageField',
            new_name,
            'image/webp',
            sys.getsizeof(buffer),
            None
        )
        file.processing_info = info
        return file

    def pre_save(self, model_instance, add):
        file = getattr(model_instance, self.attname)
        
        if file and hasattr(file, 'name'):
            processed_file = self.process_image(file)
            setattr(model_instance, self.attname, processed_file)
            
            # Log processing info
            if hasattr(processed_file, 'processing_info'):
                info = processed_file.processing_info
                print(f"""
                Image Processing Results:
                Action: {info['action']}
                Original Size: {info['original_size_kb']:.2f} KB
                Final Size: {info['final_size_kb']:.2f} KB
                Quality: {info['quality']}
                Dimensions: {info['dimensions']}
                Resized: {info['resized']}
                """)
        
        return super().pre_save(model_instance, add)