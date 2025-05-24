from django.shortcuts import render, get_object_or_404  # You need get_object_or_404 here
from .models import Listing

def listing_list(request):
    listings = Listing.objects.all()
    return render(request, 'listings/home.html', {'listings': listings})

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/detail.html', {'listing': listing})
