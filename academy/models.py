from django.db import models
from utils.helper import OptimalImageField
from django_ckeditor_5.fields import CKEditor5Field
from dashboard.models import BaseModel
# Create your models here.

class AcademyBlog(BaseModel):
    title = models.CharField(max_length=255)
    image = OptimalImageField(
        upload_to='academy/blog/',
        size_threshold_kb=600,  
        max_dimensions=(1920, 1080)  ,
        blank=True, null=True
    )
    image_alt = models.CharField(max_length=255, blank=True, null=True)
    introduction = CKEditor5Field('Introduction', config_name='extends') 
    description = CKEditor5Field('Description', config_name='extends')
    meta_title = models.CharField(max_length=300, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'academy.blogs'
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering = ('-date_added',)

    def __str__(self):
        return self.title if self.title else str(self.id)
    
    
class AcademyFAQ(BaseModel):
    question = models.CharField(max_length=255)
    answer = CKEditor5Field('Answer', config_name='extends')

    class Meta:
        db_table = 'academy.faq'
        verbose_name = 'FAQ'
        verbose_name_plural = "FAQs"
        ordering = ('-date_added',)

    def __str__(self):
        return self.question if self.question else str(self.id)
    
    
class AcademyEnquiry(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    program = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "academy.enquiry"
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return self.name if self.name else str(self.id)
    
class AcademyGallery(BaseModel):
    image = OptimalImageField(
        upload_to='academy/gallery/',
        size_threshold_kb=600,  
        max_dimensions=(1920, 1080)  ,
        blank=True, null=True
    )
    image_alt = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'academy.gallery'
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'
        ordering = ('-date_added',)

    def __str__(self):
        return self.image_alt if self.image_alt else str(self.id)
