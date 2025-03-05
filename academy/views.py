from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from academy import serializer as academy_serializer
from academy import models as academy_model

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template

from client.views import CustomPageNumberPagination

import logging

logger = logging.getLogger(__name__)

# Create your views here.

class AcademyBlogsAPIView(APIView):
    """
    API view for fetching academy blog and academy blog Details for users with pagination.
    """
    pagination_class = CustomPageNumberPagination
    model = academy_model.AcademyBlog
    serializers_class = academy_serializer.AcademyBlogSerializer

    def get(self, request, slug = None):
        try:
            if slug:
                instance = self.get_object(slug)
                if not instance:
                    return Response({
                        "StatusCode": 6002,
                        "details": "Error",
                        "message": "Blog not found",
                    }, status=status.HTTP_404_NOT_FOUND)

                serializer = academy_serializer.AcademyBlogDetailSerializer(
                    instance, 
                    context={'request': request}
                )

                related_blogs = self.model.objects.filter(is_deleted=False).exclude(slug=slug).values('title', 'slug', 'date_added')[:3]
                response_data = {
                    "StatusCode": 6000,
                    "details": "Success",
                    "data": serializer.data,
                    "related_blogs": related_blogs,
                    "message": "Academy blog details retrieved successfully"
                }
                return Response(response_data, status=status.HTTP_200_OK)

            queryset = self.model.objects.filter(is_deleted=False)
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)

            serializer = self.serializers_class(
                    page, 
                    many=True, 
                    context={'request': request}
                )

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "pagination": {
                        "total_items": paginator.page.paginator.count,
                        "total_pages": paginator.page.paginator.num_pages,
                        "current_page": paginator.page.number,
                        "next": paginator.get_next_link(),
                        "previous": paginator.get_previous_link()
                    },
                "message" : "Academy blog's data fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving Blog's: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve academy blog's",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self, slug):
        try:
            return self.model.objects.filter(slug=slug).first()
        except Exception as e:
            logger.error(f"Error retrieving object: {str(e)}")
            return None
        
class AcademyFaqAPIView(APIView):
    """
    API view for fetching academy faq data for users.
    """
    def get(self, request):
        try:
            queryset = academy_model.AcademyFAQ.objects.filter(is_deleted=False)
            serializer = academy_serializer.AcademyFAQSerializer(queryset, many=True, context={'request': request})

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "message" : "Academy faq data fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving academy faq data: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve academy faq data",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
class AcademyEnquiryAPIView(APIView):
    def post(self,request):
        try:
            serializer = academy_serializer.AcademyEnquirySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                context = {
                    'name': serializer.data['name'],
                    'email': serializer.data['email'],
                    'number': serializer.data['number'],
                    'program': serializer.data['program'],
                    'date_added': serializer.data['date_added']
                }
                template = get_template('academy_enquiry.html').render(context, request=request)
                send_mail(
                    'Enquiry Data from academy.adbox.in',
                    None, 
                    settings.EMAIL_HOST_USER,
                    ['adboxdigitalagency@gmail.com'],
                    fail_silently=False,
                    html_message = template,
                    )
                response_data = {
                    "StatusCode": 6001,
                    "detail": "success",
                    "data": serializer.data,
                    "message": "Academy enquiry successfully"
                }
            else:
                response_data = {
                    "StatusCode": 6002,
                    "detail": "validation error",
                    "data": serializer.errors,
                    "message": ""
                }
        except Exception as e:
            logger.error(f"Error subminting object: {str(e)}")
            response_data = {
                 "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to enquery",
                "error": str(e)
            }
        return Response(response_data, status=status.HTTP_200_OK)