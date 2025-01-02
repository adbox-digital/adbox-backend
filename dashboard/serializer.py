from rest_framework import serializers
from .models import *

class HomepageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomepageContent
        fields = ['id', 'our_metrics_description', 'box1_number', 'box1_description', 
            'box2_number', 'box2_description', 'box3_number', 'box3_description'] 

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'type', 'name', 'image', 'image_alt', 'description', 'work_category', 'video', 'thumbnail']

    def validate(self, data):
        testimonial_type = data.get('type', '').strip().lower()
        if not testimonial_type:
            raise serializers.ValidationError({"type": "Type is required for testimonials."})

        if testimonial_type == 'video' and not data.get('video'):
            raise serializers.ValidationError({"video": "Video file is required for video testimonials."})

        if testimonial_type == 'text' and not data.get('image'):
            raise serializers.ValidationError({"image": "Image is required for text testimonials."})

        return data

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']


class BlogSerializer(serializers.ModelSerializer):
    date_added = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = ['id', 'title', 'image', 'image_alt', 'introduction', 'slug', 'date_added']

    def get_date_added(self, obj):
        return obj.date_added.strftime("%d %b %Y") if obj.date_added else None


class BlogDetailSerializer(serializers.ModelSerializer):
    date_added = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'image', 'image_alt', 'introduction', 'slug',
            'description', 'meta_title', 'meta_description', 'date_added']

    def get_date_added(self, obj):
        return obj.date_added.strftime("%d %b %Y") if obj.date_added else None


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'image', 'image_alt']

class OurApproachSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurApproach
        fields = ['id', 'title', 'description']

class OurProcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurProces
        fields = ['id', 'icon', 'title', 'description']

class CaseStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = ['id', 'hero_title', 'hero_image']

class ExpertiseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseItem
        fields = ['id', 'case_study', 'expertise_items']

class CaseStudyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyImages
        fields = ['id', 'case_study', 'image', 'image_alt']

class CaseStudyDetailSerializer(serializers.ModelSerializer):
    expertise_items = ExpertiseItemSerializer(many=True, source='expertiseitem_set')
    case_study_images = CaseStudyImagesSerializer(many=True, source='casestudyimages_set')
    class Meta:
        model = CaseStudy
        fields = ['id', 'hero_title', 'hero_subtitle', 'hero_image', 'location'
            'about_description', 'approach_description', 'expertise_items', 'case_study_images']

class ServiceItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceItems
        fields = ['id', 'services', 'title', 'icon', 'description']

class ServicesListingSerializer(serializers.ModelSerializer):
    expertise_items = serializers.SerializerMethodField()
    class Meta:
        model = Services
        fields = ['id', 'name', 'title', 'description']

    def get_expertise_items(self, obj):
        items = obj.serviceitems_set.all()[:3]
        return ServiceItemsSerializer(items, many=True).data

class ServicesDetailSerializer(serializers.ModelSerializer):
    expertise_items = ServiceItemsSerializer(many=True, source='serviceitems_set')

    class Meta:
        model = Services
        fields = ['id', 'name', 'title', 'description', 'expertise_items']


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields =  ['id', 'job_title', 'job_description', 'location', 'job_type']

class ApplicationsSerializer(serializers.ModelSerializer):
    date_added = serializers.SerializerMethodField()

    class Meta:
        model = Applications
        fields = ['id', 'position', 'name', 'number', 'email', 'location', 'cv', 'date_added']

    def get_date_added(self, obj):
        return obj.date_added.strftime("%d %b %Y") if obj.date_added else None

class EnquirySerializer(serializers.ModelSerializer):
    date_added = serializers.SerializerMethodField()

    class Meta:
        model = Enquiry
        fields = ['id', 'name', 'number', 'email', 'message', 'date_added']

    def get_date_added(self, obj):
        return obj.date_added.strftime("%d %b %Y") if obj.date_added else None
