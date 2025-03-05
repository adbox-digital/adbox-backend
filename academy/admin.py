from django.contrib import admin
from .models import AcademyFAQ, AcademyEnquiry, AcademyBlog

# Register your models here.

@admin.register(AcademyFAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'date_added', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('question', 'answer')
    readonly_fields = ('date_added', 'date_updated')
    
@admin.register(AcademyBlog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('title', 'introduction', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('date_added', 'date_updated')
    
@admin.register(AcademyEnquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_added', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('date_added', 'date_updated')
    