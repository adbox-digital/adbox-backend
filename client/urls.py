from django.urls import path
from . import views
urlpatterns = [
    path('metrix/', views.HomepageContentAPIView.as_view(), name='metrix-get'),
    path('testimonial/', views.TestimonialAPIView.as_view(), name='testimonial-get'),
    path('faq/', views.FaqAPIView.as_view(), name='faq-get'),
    path('blog/', views.BlogsAPIView.as_view(), name='blog-get'),
    path('blog/<slug:slug>', views.BlogsAPIView.as_view(), name='blog-details'),
    path('gallery/', views.GalleryAPIView.as_view(), name='gallery-get'),
    path('our-approach/', views.OurApproachAPIView.as_view(), name='our-approach-get'),
    path('our-proces/', views.OurProcesAPIView.as_view(), name='our-proces-get'),
]
