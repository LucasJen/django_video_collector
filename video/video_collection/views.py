from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower
from .forms import VideoForm, SearchForm
from .models import Video


def home(request):
    app_name = 'Video Upload Site'
    return(render(request, 'video_collection/home.html', {app_name: 'app_name'}))

def add(request):

    if request.method == "POST":
        new_video_form = VideoForm(request.POST) # Creates variable that stores the POST request data for VideoForm
        if new_video_form.is_valid(): # Uses built in is_valid function to ensure request information is valid
            try:
                new_video_form.save()
                return redirect('video_list')
                # messages.info(request, 'New video saved!')
            except ValidationError: # User facing error
                messages.warning(request, 'Invalid Youtube URL.')
            except IntegrityError: # User facing error if video is already added.
                messages.warning(request, 'This video has already been added.')

         # if the form is not valid, it will returnt he same page with the user provided information still in the boxes
        messages.warning(request, 'Please check the data entered.')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})         
    
    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

def video_list(request):

    search_form = SearchForm(request.GET) # create form from data that the user provides
    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term']
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name')) #orders data by name

    else: # for is not filled in or this the first time the user has visited
        search_form = SearchForm()
        videos = Video.objects.order_by(Lower('name'))

    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form})