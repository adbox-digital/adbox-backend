from django.urls import path
from . import views
urlpatterns = [
    path('brand/', views.BrandAPIView.as_view(), name='brand-get'),
    path('our-metrics/', views.HomepageContentAPIView.as_view(), name='metrix-get'),
    path('testimonial/', views.TestimonialAPIView.as_view(), name='testimonial-get'),
    path('faq/', views.FaqAPIView.as_view(), name='faq-get'),
    path('blogs/', views.BlogsAPIView.as_view(), name='blog-get'),
    path('blog/<slug:slug>', views.BlogsAPIView.as_view(), name='blog-details'),
    path('gallery/', views.GalleryAPIView.as_view(), name='gallery-get'),
    path('our-approach/', views.OurApproachAPIView.as_view(), name='our-approach-get'),
    path('our-proces/', views.OurProcesAPIView.as_view(), name='our-proces-get'),
    path('seo/', views.SeoListAPIView.as_view(), name='seo-get'),

    path('services/', views.ServicesAPIView.as_view(), name='services-get'),
    path('services/<slug:slug>', views.ServicesAPIView.as_view(), name='services-get'),
    
    path('case-study/', views.CaseStudyAPIView.as_view(), name='our-case-study-get'),
    path('case-study/<slug:slug>', views.CaseStudyAPIView.as_view(), name='our-case-study-details'),
    
    path('enquiry/', views.ServiceEnquiryAPIView.as_view(), name="user-enquiry"),
    path('job-enquiry/', views.JobEnquiryAPIView.as_view(), name="job-enquiry"),
    path('job-post/', views.JobPostAPIView.as_view(), name="job-post-enquiry"),
    path('job-post/<uuid:id>', views.JobPostAPIView.as_view(), name="job-post-enquiry"),

    path('dynamic-sitemap/', views.DynamicSiteMapAPIView.as_view(), name="dynamicsite-map"),

]
