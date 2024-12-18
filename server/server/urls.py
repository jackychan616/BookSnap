"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
<<<<<<< HEAD
<<<<<<< HEAD
from rest_framework.routers import DefaultRouter
from blog.views import (
    PostViewSet, PostTypeViewSet, PostImageViewSet,
    EventViewSet, TemplateImageViewSet
)

<<<<<<< HEAD
<<<<<<< HEAD
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'post-types', PostTypeViewSet)
router.register(r'post-images', PostImageViewSet)
router.register(r'events', EventViewSet)
router.register(r'template-images', TemplateImageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
=======
=======
>>>>>>> 675d26b (reel model)
from blog.views import upload_file, post_list, dashboard, create_reel, reel_list

urlpatterns = [
    path('admin/', admin.site.urls),
=======
from django.contrib.auth import views as auth_views

from blog.views import upload_file, post_list, dashboard, create_reel, reel_list

urlpatterns = [
    path('admin/', admin.site.urls),
>>>>>>> 419ef2a (blog)
    path('api/', include("blog.urls")),
    path('upload/', upload_file, name='upload_file'),
    path('reel/create/', create_reel, name='create_reel'),
    path('reel/list/', reel_list, name='reel_list'),
    path("post-list/", post_list, name="post-list"),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True,
        next_page='dashboard'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),
    path('', dashboard, name='dashboard'),
<<<<<<< HEAD
>>>>>>> 675d26b (reel model)
=======
>>>>>>> 419ef2a (blog)
=======

from blog.views import upload_file, post_list

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include("blog.urls")),
    path('upload/', upload_file, name='upload_file'),
    path("post-list/", post_list, name="post-list"),
>>>>>>> ae2a2fd (new)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
