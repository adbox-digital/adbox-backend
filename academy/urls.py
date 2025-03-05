from django.urls import path
from . import views
urlpatterns = [
path('faq/', views.AcademyFaqAPIView.as_view(), name='faq-get'),
    path('blogs/', views.AcademyBlogsAPIView.as_view(), name='blog-get'),
    path('blog/<slug:slug>', views.AcademyBlogsAPIView.as_view(), name='blog-details'),
    path('enquiry/', views.AcademyEnquiryAPIView.as_view(), name="user-enquiry"),

]
