from django.conf.urls.static import static
from django.urls import path

from proiectLic import settings
from . import views

urlpatterns = [
    path('home/<int:pk>/<int:user_id>', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('practice/<int:user_id>/', views.practice, name='practice'),
    path('activityflow/<int:user_id>/', views.activityflow, name='activityflow'),
    path('profile/<int:user_id>/<int:connected_user_id>/', views.profile, name='profile'),
    path('test/<int:pk>/<int:user_id>/', views.test, name='test'),
    path('bug/<int:pk>/<int:user_id>/', views.bug, name='bug'),
    path('', views.landing, name='landing')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
