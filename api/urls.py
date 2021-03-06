from django.urls import path

from . import views

urlpatterns = [
    path('generateMarkings', views.marking),
    path('translate', views.translation),
    path('checkForPlagiarism', views.plagiarism),
    path('uploadDocument', views.upload_document),
    path('ping', views.ping)
]
