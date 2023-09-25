from rest_framework.routers import DefaultRouter
from .views import FileViewSet
from django.urls import path
from . import views



urlpatterns = [
    path('file-list/', views.file_list, name='file_list'),
    path('', views.home, name='home'),
    path('gfile_list/',views.guest_file_list,name='gfile_list'),
    path('signup/', views.signup, name='signup_user'),
    
    path('login/', views.CustomLoginView.as_view(), name='login_user'),
    
    path('signout/', views.signout_user, name='signout_user'),
 
    path('download-file/<str:token>/', views.download_file_by_token, name='download-file'),
    
    
   


]


router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')  




urlpatterns += router.urls
