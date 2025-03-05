from rest_framework import serializers
from .models import *


class AcademyBlogSerializer(serializers.ModelSerializer):
    date_added = serializers.SerializerMethodField()
    class Meta:
        model = AcademyBlog
        fields = ['id', 'title', 'image', 'image_alt', 'introduction', 'slug', 'date_added']

    def get_date_added(self, obj):
        return obj.date_added.strftime("%d %b %Y") if obj.date_added else None


class AcademyBlogDetailSerializer(serializers.ModelSerializer):
    date_added = serializers.SerializerMethodField()

    class Meta:
        model = AcademyBlog
        fields = ['id', 'title', 'image', 'image_alt', 'introduction', 'slug',
            'description', 'meta_title', 'meta_description', 'date_added']

    def get_date_added(self, obj):
        return obj.date_added.strftime("%d %b %Y") if obj.date_added else None


class AcademyFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademyFAQ
        fields = ['id', 'question', 'answer']

class AcademyEnquirySerializer(serializers.ModelSerializer):
    date_added = serializers.SerializerMethodField()

    class Meta:
        model = AcademyEnquiry
        fields = ['id', 'name', 'number', 'email', 'program', 'date_added']

    def get_date_added(self, obj):
        return obj.date_added.strftime("%d %b %Y") if obj.date_added else None