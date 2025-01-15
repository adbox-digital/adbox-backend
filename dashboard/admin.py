from django.contrib import admin
from .models import *

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo', 'date_added', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name',)
    readonly_fields = ('date_added', 'date_updated') 

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'work_category', 'date_added', 'is_deleted')
    list_filter = ('type', 'work_category', 'is_deleted')
    search_fields = ('name', 'description', 'work_category')
    readonly_fields = ('date_added', 'date_updated')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'date_added', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('question', 'answer')
    readonly_fields = ('date_added', 'date_updated')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('title', 'introduction', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('date_added', 'date_updated')

@admin.register(HomepageContent)
class HomepageContentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Allow adding only if no instance exists
        return not HomepageContent.objects.exists()

    def changelist_view(self, request, extra_context=None):
        # Redirect to the edit page if an instance exists
        if HomepageContent.objects.exists():
            head_office = HomepageContent.objects.first()
            return self.change_view(request, object_id=str(head_office.pk))
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('image_alt', 'date_added', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('image_alt',)
    readonly_fields = ('date_added', 'date_updated')

@admin.register(OurApproach)
class OurApproachAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('title', 'description')
    readonly_fields = ('date_added', 'date_updated')

@admin.register(OurProces)
class OurProcessAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('title', 'description')
    readonly_fields = ('date_added', 'date_updated')

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('hero_title', 'location')
    search_fields = ('hero_title', 'hero_subtitle', 'location')
    prepopulated_fields = {'slug': ('hero_title',)}

@admin.register(ExpertiseItem)
class ExpertiseItemAdmin(admin.ModelAdmin):
    list_display = ('expertise_items', 'case_study', 'date_added', 'is_deleted')
    list_filter = ('case_study__hero_title', 'is_deleted')
    search_fields = ('expertise_items',)
    readonly_fields = ('date_added', 'date_updated')

@admin.register(CaseStudyImages)
class CaseStudyImagesAdmin(admin.ModelAdmin):
    list_display = ('image_alt', 'case_study', 'date_added', 'is_deleted')
    list_filter = ('case_study__hero_title', 'is_deleted')
    search_fields = ('image_alt',)
    readonly_fields = ('date_added', 'date_updated')

class ServiceItemsInline(admin.TabularInline): 
    model = ServiceItems
    extra = 0
    fields = ('title', 'icon', 'description', 'is_deleted') 
    readonly_fields = ('date_added', 'date_updated')

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'date_added', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name', 'title', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('date_added', 'date_updated')
    inlines = [ServiceItemsInline] 

@admin.register(ServiceItems)
class ServiceItemsAdmin(admin.ModelAdmin):
    list_display = ('title', 'services', 'date_added', 'is_deleted')
    list_filter = ('services__name', 'is_deleted')
    search_fields = ('title', 'description')
    readonly_fields = ('date_added', 'date_updated')

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'location', 'job_type', 'date_added', 'is_deleted')
    list_filter = ('job_type', 'location', 'is_deleted')
    search_fields = ('job_title', 'job_description', 'location')
    readonly_fields = ('date_added', 'date_updated')

@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'email', 'location', 'date_added', 'is_deleted')
    list_filter = ('position', 'location', 'is_deleted')
    search_fields = ('name', 'email', 'location')
    readonly_fields = ('date_added', 'date_updated')

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_added', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('date_added', 'date_updated')