from django.db import models
import uuid
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.translation import gettext_lazy as _ 
from utils.helper import OptimalImageField
from django.core.exceptions import ValidationError
from django.utils.html import format_html


# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, default=timezone.now, editable=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.date_added:
            self.date_added = timezone.now()
        super(BaseModel, self).save(*args, **kwargs)


class Brand(BaseModel):
    name = models.CharField(max_length=255, blank = True, null = True)
    logo = models.FileField(upload_to='brands')
    image_alt = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'brand'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        ordering = ('-date_added',)

    def __str__(self):
        return self.name if self.name else str(self.id)

class Testimonial(BaseModel):
    class TestimonialType(models.TextChoices):
        VIDEO = 'video', _('Video')
        TEXT = 'text', _('Text')

    type = models.CharField(
    max_length=10,
    choices=TestimonialType.choices,
    default=TestimonialType.TEXT,
    help_text="Type of testimonial: Video or Text."
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Name of the person giving the testimonial."
    )
    image = OptimalImageField(
        upload_to='testimonials/',
        size_threshold_kb=600,  
        max_dimensions=(1920, 1080),
        blank=True, null=True
    )
    image_alt = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Alternative text for the image."
    )
    description = CKEditor5Field(
        'Description',
        config_name='extends',
        help_text="Detailed text content of the testimonial."
    )
    work_category = models.CharField(max_length=255, blank=True, null=True)
    video = models.FileField(upload_to='testimonials', blank=True, null=True)
    thumbnail = OptimalImageField(
        upload_to='testimonials/',
        size_threshold_kb=600,  
        max_dimensions=(1920, 1080)  ,
        blank=True, null=True
    )

    def clean(self):
        if self.type == self.TestimonialType.VIDEO and not self.video:
            raise ValidationError("Video field is required for video testimonials.")


    class Meta:
        db_table = 'testimonial'
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ('-date_added',)

    def __str__(self):
        return self.name if self.name else str(self.id)

class FAQ(BaseModel):
    question = models.CharField(max_length=255)
    answer = CKEditor5Field('Answer', config_name='extends')

    class Meta:
        db_table = 'faq'
        verbose_name = 'FAQ'
        verbose_name_plural = "FAQs"
        ordering = ('-date_added',)

    def __str__(self):
        return self.question if self.question else str(self.id)

class Blog(BaseModel):
    title = models.CharField(max_length=255)
    image = OptimalImageField(
        upload_to='blog/',
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
        db_table = 'blogs'
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering = ('-date_added',)

    def __str__(self):
        return self.title if self.title else str(self.id)

class HomepageContent(BaseModel):
    our_metrics_description = models.TextField(help_text="Description for the Our Metrics section.")
    
    box1_number = models.IntegerField(help_text="Number for the first metric box.")
    box1_description = models.TextField(help_text="Description for the first metric box.")
    
    box2_number = models.IntegerField(help_text="Number for the second metric box.")
    box2_description = models.TextField(help_text="Description for the second metric box.")
    
    box3_number = models.IntegerField(help_text="Number for the third metric box.")
    box3_description = models.TextField(help_text="Description for the third metric box.")

    class Meta:
        db_table = "homepage_content"
        verbose_name = "Homepage Content"
        verbose_name_plural = "Homepage Contents"

    def save(self, *args, **kwargs):
        if HomepageContent.objects.exists() and not self.pk:
            raise ValidationError("Only one Homepage Content instance is allowed.")
        super().save(*args, **kwargs)

    def __str__(self):
        return "Homepage Content"

class Gallery(BaseModel):
    image = OptimalImageField(
        upload_to='gallery/',
        size_threshold_kb=600,  
        max_dimensions=(1920, 1080)  ,
        blank=True, null=True
    )
    image_alt = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'Gallery'
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'
        ordering = ('-date_added',)

    def __str__(self):
        return self.image_alt if self.image_alt else str(self.id)


class OurApproach(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'our_approach'
        verbose_name = 'Our Approach'
        verbose_name_plural = "Our Approach"
        ordering = ('-date_added',)

    def __str__(self):
        return self.title if self.title else str(self.id)

class OurProces(BaseModel):
    icon = models.FileField(upload_to='our_proces', null=True, blank=True)
    image_alt = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = CKEditor5Field('Description', config_name='extends')

    class Meta:
        db_table = 'our_proces'
        verbose_name = 'Our Proces'
        verbose_name_plural = "Our Proces"
        ordering = ('-date_added',)

    def __str__(self):
        return self.title if self.title else str(self.id)

class CaseStudy(BaseModel):
    # Hero Section
    hero_title = models.CharField(max_length=255, help_text="Main title displayed in the hero section.", verbose_name="Case Study Title"  )
    hero_subtitle = models.CharField(max_length=255, help_text="Subtitle displayed in the hero section.")
    hero_image = OptimalImageField(
        upload_to='case_study/hero/',
        size_threshold_kb=600,  
        max_dimensions=(1920, 1080),
        blank=True, null=True
    )
    image_alt = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    # About Section
    about_description = CKEditor5Field(
        'About Description',
        config_name='extends',
        help_text="Description text for the About section."
    )

    # Approach Section
    approach_description = CKEditor5Field(
        'Approach Description',
        config_name='extends',
        help_text="Detailed description for the Approach section."
    )
    slug = models.SlugField(unique=True)
    meta_title = models.CharField(max_length=300, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = "case_study"
        verbose_name = "Case Study"
        verbose_name_plural = "Case Studies"

    def __str__(self):
        return self.hero_title

class ExpertiseItem(BaseModel):
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)
    expertise_items = models.CharField(max_length=255)

    class Meta:
        db_table = "expertise_item"
        verbose_name = "Expertise Item"
        verbose_name_plural = "Expertise Items"

    def __str__(self):
        return self.expertise_items

class CaseStudyImages(BaseModel):
    case_study = models.ForeignKey(CaseStudy, on_delete=models.CASCADE)
    image = OptimalImageField(
        upload_to='case_study/',
        size_threshold_kb=600,  
        max_dimensions=(1920, 1080),
        blank=True, null=True
    )
    image_alt = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "case_study_images"
        verbose_name = "CaseStudy Image"
        verbose_name_plural = "CaseStudy Imagess"

    def __str__(self):
        return self.image_alt if self.image_alt else str(self.id)

class Services(BaseModel):
    name = models.CharField(max_length=255, help_text="Your Service eg:STRATEGY")
    title = models.CharField(max_length=255, help_text="",blank=True, null=True)
    is_home = models.BooleanField(default=False, help_text="Display on the home page.")
    home_page_descrption = models.TextField(blank=True, null=True, help_text="Description for the home page.")
    description = CKEditor5Field('Description', config_name='extends')
    slug = models.SlugField(unique=True,)
    meta_title = models.CharField(max_length=300, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "services"
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name if self.name else str(self.id)

class ServiceItems(BaseModel):
    services = models.ForeignKey(Services, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, help_text="")
    icon = models.FileField(upload_to='service/item', blank=True, null=True)
    image_alt = models.CharField(max_length=200, blank=True, null=True)
    description = CKEditor5Field('Description', config_name='extends')

    class Meta:
        db_table = "service_items"
        verbose_name = "Service Item"
        verbose_name_plural = "Service Items"

    def __str__(self):
        return self.title if self.title else str(self.id)

class JobPost(BaseModel):
    job_title = models.CharField(
    max_length=255,
    help_text="Title of the job position."
    )
    job_description = models.TextField(blank=True, null=True,help_text="Detailed description of the job.")
    contents = CKEditor5Field(
        'Contents',
        config_name='extends',
        help_text="Detailed description of the job."
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Location where the job is based."
    )
    job_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Type of job, e.g., Full-time, Part-time, etc."
    )
    meta_title = models.CharField(max_length=300, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    class Meta:
        db_table = "job_post"
        verbose_name = "Job Post"
        verbose_name_plural = "Job Posts"

    def __str__(self):
        return self.job_title if self.job_title else str(self.id)

class Applications(BaseModel):
    position = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    cv = models.FileField(upload_to='applications',blank=True, null=True)

    class Meta:
        db_table = "appplications"
        verbose_name = "Applications"
        verbose_name_plural = "Applications"

    def __str__(self):
        return self.name if self.name else str(self.id)

class Enquiry(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "enquiry"
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return self.name if self.name else str(self.id)

class SEO(BaseModel):
    page=models.CharField(max_length=200,blank=True,null=True)
    path=models.CharField(max_length=200)
    meta_title=models.TextField(blank=True,null=True)
    meta_description=models.TextField(blank=True,null=True)
    class Meta:
        db_table='web.seo'
        verbose_name = ('SEO')
        verbose_name_plural = ('SEO')
        ordering = ('date_added',)

    def __str__(self):
        return self.path if self.path else str(self.id)