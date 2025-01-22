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

class BrandAPIView(APIView):
    """
    API view for fetching brand's data for users.
    """
    def get(self, request):
        try:
            queryset = dashboard_model.Brand.objects.filter(is_deleted=False)
            serializer = dashboard_serializer.BrandSerializer(queryset, many=True, context={'request': request})

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "message" : "Brand data fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving Brand data: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve Brand data",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HomepageContentAPIView(APIView):
    """
    API view for fetching homepage metrix data for users.
    """
    def get(self, request):
        try:
            queryset = dashboard_model.HomepageContent.objects.filter(is_deleted=False).first()
            serializer = dashboard_serializer.HomepageContentSerializer(queryset, context={'request': request})

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

                related_blogs = self.model.objects.filter(is_deleted=False).exclude(slug=slug).values('title', 'slug', 'date_added')[:3]
                response_data = {
                    "StatusCode": 6000,
                    "details": "Success",
                    "data": serializer.data,
                    "related_blogs": related_blogs,
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
        

class CaseStudyAPIView(APIView):
    """
    API view for fetching Case Study and Case Study Details for users.
    """
    model = dashboard_model.CaseStudy
    serializers_class = dashboard_serializer.CaseStudySerializer

    def get(self, request, slug = None):
        try:
            if slug:
                instance = self.get_object(slug)
                if not instance:
                    return Response({
                        "StatusCode": 6002,
                        "details": "Error",
                        "message": "Case Study not found",
                    }, status=status.HTTP_404_NOT_FOUND)

                serializer = dashboard_serializer.CaseStudyDetailSerializer(
                    instance, 
                    context={'request': request}
                )

                response_data = {
                    "StatusCode": 6000,
                    "details": "Success",
                    "data": serializer.data,
                    "message": "Case Study details retrieved successfully"
                }
                return Response(response_data, status=status.HTTP_200_OK)

            queryset = self.model.objects.filter(is_deleted=False)
            
            serializer = self.serializers_class(
                    queryset, 
                    many=True, 
                    context={'request': request}
                )

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "message" : "Case Study's data fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving Case Study's: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve Case Study's",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self, slug):
        try:
            return self.model.objects.filter(slug=slug).first()
        except Exception as e:
            logger.error(f"Error retrieving object: {str(e)}")
            return None


class ServicesAPIView(APIView):
    """
    API view for fetching Services and Services Details for users with pagination.
    """
    # pagination_class = CustomPageNumberPagination
    model = dashboard_model.Services
    serializers_class = dashboard_serializer.ServicesListingSerializer

    def get(self, request, slug = None):
        try:
            is_home = request.query_params.get('is_home', None)
            if is_home:
                queryset = self.model.objects.values('id', 'name', 'home_page_descrption', 'slug').filter(is_deleted=False, is_home = True)[:3]
                response_data = {
                    "StatusCode": 6000,
                    "details": "Success",
                    "data": queryset,
                    "message": "Services retrieved successfully"
                }
                return Response(response_data, status=status.HTTP_200_OK)
            if slug:
                instance = self.get_object(slug)
                if not instance:
                    return Response({
                        "StatusCode": 6002,
                        "details": "Error",
                        "message": "Services not found",
                    }, status=status.HTTP_404_NOT_FOUND)

                serializer = dashboard_serializer.ServicesDetailSerializer(
                    instance, 
                    context={'request': request}
                )

                response_data = {
                    "StatusCode": 6000,
                    "details": "Success",
                    "data": serializer.data,
                    "message": "Services details retrieved successfully"
                }
                return Response(response_data, status=status.HTTP_200_OK)

            queryset = self.model.objects.filter(is_deleted=False)

            serializer = self.serializers_class(
                    queryset, 
                    many=True, 
                    context={'request': request}
                )

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "message" : "Services data fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving Services: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve Services",
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
    API view for fetching Gallery for users.
    """
    def get(self, request):
        try:
            is_home = request.query_params.get('is_home', None)
            if is_home:
                queryset = dashboard_model.Gallery.objects.filter(is_deleted=False)[:6]
            else:
                queryset = dashboard_model.Gallery.objects.filter(is_deleted=False)
            serializer = dashboard_serializer.GallerySerializer(queryset, many=True, context={'request': request})

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "message" : "Gallery images fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving Gallery: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve Gallery",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class ServiceEnquiryAPIView(APIView):
    def post(self,request):
        try:
            serializer = dashboard_serializer.EnquirySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                context = {
                    'name': serializer.data['name'],
                    'email': serializer.data['email'],
                    'number': serializer.data['number'],
                    'message': serializer.data['message'],
                    'date_added': serializer.data['date_added']
                }
                template = get_template('enquiry.html').render(context, request=request)
                send_mail(
                    'Enquiry Data',
                    None, 
                    settings.EMAIL_HOST_USER,
                    ['muhammadsifan.accolades@gmail.com'],
                    fail_silently=False,
                    html_message = template,
                    )
                response_data = {
                    "StatusCode": 6001,
                    "detail": "success",
                    "data": serializer.data,
                    "message": "Enquiry successfully"
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


class JobPostAPIView(APIView):
    """
    API view for fetching Job list for users.
    """
    model = dashboard_model.JobPost
    serializer_class = dashboard_serializer.JobPostSerializer
    def get(self, request, id=None):
        try:
            if id:
                instance = self.get_object(id)
                if not instance:
                    return Response({
                        "StatusCode": 6002,
                        "details": "Error",
                        "message": "Services not found",
                    }, status=status.HTTP_404_NOT_FOUND)

                serializer = self.serializer_class(
                    instance, 
                    context={'request': request}
                )

                response_data = {
                    "StatusCode": 6000,
                    "details": "Success",
                    "data": serializer.data,
                    "message": "Services details retrieved successfully"
                }
                return Response(response_data, status=status.HTTP_200_OK)
            queryset = self.model.objects.filter(is_deleted=False)
            serializer = self.serializer_class(queryset, many=True, context={'request': request})

            response_data = {
                "StatusCode" : 6000,
                "details" : "Success",
                "data" : serializer.data,
                "message" : "Job list fetched successfully"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error retrieving Job list: {str(e)}")
            return Response({
                "StatusCode": 6002,
                "api": request.get_full_path(),
                "details": "Error",
                "message": "Failed to retrieve Job list",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get_object(self, id):
        try:
            return self.model.objects.filter(id=id).first()
        except Exception as e:
            logger.error(f"Error retrieving object: {str(e)}")
            return None
        
        
class JobEnquiryAPIView(APIView):
    def post(self,request):
        try:
            serializer = dashboard_serializer.ApplicationsSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                application = serializer.save()
               
                context = {
                    'name': application.name,
                    'email': application.email,
                    'number': application.number,
                    'position': application.position.job_title if application.position else None,
                    'location': application.location,
                    'cv': request.build_absolute_uri(application.cv.url) if application.cv else None,
                    'date_added': application.date_added,
                }
                template = get_template('career_enquiry.html').render(context, request=request)
                send_mail(
                    'Enquiry Data',
                    None, 
                    settings.EMAIL_HOST_USER,
                    ['muhammadsifan.accolades@gmail.com'],
                    fail_silently=False,
                    html_message = template,
                    )
                response_data = {
                    "StatusCode": 6001,
                    "detail": "success",
                    "data": serializer.data,
                    "message": "Enquiry successfully"
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
    
    
class SeoListAPIView(APIView):
    """
    Get Seo details for user side
    """
    model = dashboard_model.SEO
    serializer_class = dashboard_serializer.SEOSerializer

    def get(self, request):
        path = request.query_params.get('path', None)
        try:
            if path:
                queryset = self.model.objects.filter(path=path)
            else:
                queryset = self.model.objects.filter(is_deleted=False)
            
            serializer = self.serializer_class(queryset, many=True, context={'request': request})

            response_data = {
                "StatusCode": 6000,
                "detail": "Success",
                "data": serializer.data,
                "message": "SEO's Data fetched successfully"
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching SEO details: {str(e)}")
            response_data = {
                "StatusCode": 6002,
                "detail": "Error",
                "data": "",
                "message": f"Something went wrong: {str(e)}"
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)