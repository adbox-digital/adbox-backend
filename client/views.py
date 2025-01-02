from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from dashboard import serializer as dashboard_serializer
from dashboard import models as dashboard_model

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template

import logging

logger = logging.getLogger(__name__)

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size' 
    max_page_size = 50  

class HomepageContentAPIView(APIView):
    """
    API view for fetching homepage metrix data for users.
    """

    def get(self, request):
        try:
            queryset = dashboard_model.HomepageContent.objects.filter(is_deleted=False)
            serializer = dashboard_serializer.HomepageContentSerializer(queryset, many=True, context={'request': request})

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "message" : "Homepage Metrix data fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving homepage metrix data: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve homepage metrix data",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TestimonialAPIView(APIView):
    """
    API view for fetching testimonial data for users.
    """

    def get(self, request):
        try:
            queryset = dashboard_model.Testimonial.objects.filter(is_deleted=False)
            serializer = dashboard_serializer.TestimonialSerializer(queryset, many=True, context={'request': request})

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "message" : "Testimonial data fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving Testimonial data: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve Testimonial data",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FaqAPIView(APIView):
    """
    API view for fetching faq data for users.
    """

    def get(self, request):
        try:
            queryset = dashboard_model.FAQ.objects.filter(is_deleted=False)
            serializer = dashboard_serializer.FAQSerializer(queryset, many=True, context={'request': request})

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "message" : "Faq data fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving Faq data: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve Faq data",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BlogsAPIView(APIView):
    """
    API view for fetching Blog and Blog Details for users with pagination.
    """
    pagination_class = CustomPageNumberPagination
    model = dashboard_model.Blog
    serializers_class = dashboard_serializer.BlogSerializer

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

                serializer = dashboard_serializer.BlogDetailSerializer(
                    instance, 
                    context={'request': request}
                )

                response_data = {
                    "StatusCode": 6000,
                    "details": "Success",
                    "data": serializer.data,
                    "message": "Blog details retrieved successfully"
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
                "message" : "Blog's data fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving Blog's: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve Blog's",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self, slug):
        try:
            return self.model.objects.filter(slug=slug).first()
        except Exception as e:
            logger.error(f"Error retrieving object: {str(e)}")
            return None

class GalleryAPIView(APIView):
    """
    API view for fetching gallery images for users.
    """

    def get(self, request):
        try:
            queryset = dashboard_model.Gallery.objects.filter(is_deleted=False)
            serializer = dashboard_serializer.GallerySerializer(queryset, many=True, context={'request': request})

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "message" : "dallery images fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving dallery images: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve dallery images",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OurApproachAPIView(APIView):
    """
    API view for fetching our approach for users.
    """

    def get(self, request):
        try:
            queryset = dashboard_model.OurApproach.objects.filter(is_deleted=False)
            serializer = dashboard_serializer.OurApproachSerializer(queryset, many=True, context={'request': request})

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "message" : "our approach fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving our approach: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve our approach",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OurProcesAPIView(APIView):
    """
    API view for fetching our proces for users.
    """

    def get(self, request):
        try:
            queryset = dashboard_model.OurProces.objects.filter(is_deleted=False)
            serializer = dashboard_serializer.OurProcesSerializer(queryset, many=True, context={'request': request})

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "message" : "Our Proces fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving Our Proces: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve Our Proces",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)