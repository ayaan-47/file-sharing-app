from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm  
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import action,api_view
from django.shortcuts import get_object_or_404,render, redirect
from .models import File
from .serializers import FileSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FileUploadParser
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseBadRequest, JsonResponse, HttpResponse, Http404
from django.contrib.auth.views import LoginView
from rest_framework import viewsets, permissions
from django.core import signing

from django.contrib import messages
class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
    def get_queryset(self):
        user = self.request.user
        if user.is_ops_user:
            return File.objects.all()
        else:
            return File.objects.all()
        
        
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
        
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        else:
    
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


    @action(detail=True, methods=['GET'])
    def download(self, request, pk=None):
        file = self.get_object()

        file_info = {
            'file_id': file.id,
        }

       
        signed_url = signing.dumps(file_info)

        response_data = {
            "download-link": request.build_absolute_uri(reverse('download-file')) + f'?token={signed_url}',
            "message": "success"
        }

        return Response(response_data)


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if user.is_ops_user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        # 
        data = {
            'title': instance.title,
            'download-link': reverse('file-download', kwargs={'pk': instance.pk}),
        }
        return Response(data)





def guest_file_list(request):
    files= File.objects.all()
    return render(request, 'file_list.html', {'files': files})



@login_required
def file_list(request):
    files = File.objects.all()
    encrypted_download_links = []

    for file in files:
        file_info = {'file_id': file.id}
        signed_url = signing.dumps(file_info)
        download_link = request.build_absolute_uri(reverse('download-file', kwargs={'token': signed_url}))
        encrypted_download_links.append({'title': file.title, 'download_link': download_link})

    context = {'files': encrypted_download_links}
    return render(request, 'file_list.html', context)




def home(request):

    files= File.objects.all()
    return render(request, 'home.html', {'files': files})
    



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('file_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})



def signout_user(request):
    logout(request)
    return redirect('home') 
    




class CustomLoginView(LoginView):
    template_name = 'login.html' 
    
    def get_success_url(self):
        user = self.request.user
        if user.is_ops_user:
            return reverse('file-list')  
        else:
            return reverse('file_list')  
    print("Successfully Logged In")
    




def download_file_by_token(request, token):
    if not request.user.is_authenticated:
        messages.error(request, "Cannot Download the file: Please Login First.")
        return redirect(reverse('login_user'))  
    try:
        file_info = signing.loads(token)
        file_id = file_info.get('file_id')
        file = get_object_or_404(File, id=file_id)
        
        response = FileResponse(file.file, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
        return response
    except signing.BadSignature:
        return HttpResponseBadRequest("Invalid token")
