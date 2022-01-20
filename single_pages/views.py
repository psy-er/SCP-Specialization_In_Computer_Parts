from django.shortcuts import render
from computer.models import Item
# Create your views here.

def landing(request):
    recent_items = Item.objects.order_by('-pk')[:3]
    return render (request, 'single_pages/landing.html',
                   {'recent_items' : recent_items })

def about_me(request):
    return render (request, 'single_pages/about_me.html')

def intro(request):
    return render (request, 'single_pages/intro.html')
