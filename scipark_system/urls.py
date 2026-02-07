"""
URL configuration for scipark_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),

    path('', views.dashboard, name='dashboard'),

    path('projects/', views.project_list, name='project_list'),
    path('training/', views.training_list, name='training_list'),
    path('training/create/', views.training_create, name='training_create'),
    path('training/<str:training_id>/', views.training_detail, name='training_detail'),
    path('training/<str:training_id>/edit/', views.training_edit, name='training_edit'),
    path('training/<str:training_id>/delete/', views.training_delete, name='training_delete'),
    path('projects/create/', views.project_create, name='project_create'), # Moved up
    path('projects/<str:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<str:project_id>/add_member/', views.project_add_member, name='project_add_member'),
    
    # Timeline Management
    path('projects/<str:project_id>/add_timeline/', views.project_add_timeline, name='project_add_timeline'),
    path('projects/<str:timeline_id>/edit_timeline/', views.project_edit_timeline, name='project_edit_timeline'),
    path('projects/<str:timeline_id>/delete_timeline/', views.project_delete_timeline, name='project_delete_timeline'),
    path('projects/<str:project_id>/add_award/', views.project_add_award, name='project_add_award'),

    path('students/', views.student_list, name='student_list'),
    path('students/<str:student_id>/', views.student_detail, name='student_detail'), # New URL
    
    path('booking/', views.booking_create, name='booking_create'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
