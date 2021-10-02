from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('login_user/', views.login_user, name='login_user'),
    path('gallery/', views.gallery, name='gallery'),
    path('upload/', views.model_form_upload, name='upload'),
    path('delete_new/', views.delete_new, name='delete_new'),
    path('delete_gallery/', views.delete_gallery, name='delete_gallery'),
    path('add_mem_admin/', views.add_mem_admin, name='add_mem_admin'),
    path('load-more-image/', views.dynamicImageLoad, name='load-more-image'),
    path('chat/', views.chat, name='chat'),
    path('add_admin/', views.add_admin, name='add_admin'),
    path('delete/', views.delete, name='delete'),
    path('select_category/', views.select_category, name='select_category')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
