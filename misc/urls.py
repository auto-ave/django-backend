from django.urls import path

from misc.views import *

urlpatterns = [
    path('imageupload/', StoreImageUpload.as_view()),
    path('feedback/', FeedbackView.as_view()),
    path('contact/', ContactView.as_view()),
    
    path('health/', HealthCheck.as_view()),
    # path('danger/', DangerView.as_view()),
    
    
    
    ## IRELAND URLS
    path('ie/imageupload/', StoreImageUpload.as_view()),
    path('ie/feedback/', FeedbackView.as_view()),
    path('ie/contact/', ContactView.as_view()),
    
    path('ie/health/', HealthCheck.as_view()),
    # path('ie/danger/', DangerView.as_view()),
]