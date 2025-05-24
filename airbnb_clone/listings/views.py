from django.shortcuts import render, get_object_or_404  # You need get_object_or_404 here
from .models import Listing

from django.http import HttpResponse
from .utils import get_users_query


from .utils import get_users_query, update_user_email

def debug_all_users_view(request):
    users = get_users_query()
    usernames = ", ".join([user.username for user in users])
    return HttpResponse(f"Users: {usernames}")

def debug_update_email_view(request):
    try:
        update_user_email(user_id=1, new_email='debug_updated@example.com')
        return HttpResponse("Email updated successfully!")
    except Exception as e:
        return HttpResponse(f"Error occurred: {str(e)}")

def listing_list(request):
    listings = Listing.objects.all()
    return render(request, 'listings/home.html', {'listings': listings})

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/detail.html', {'listing': listing})

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
import os
from django.conf import settings

@staff_member_required  # only accessible by admin/staff users
def view_logs(request):
    log_file_path = os.path.join(settings.BASE_DIR, 'user_queries.log')
    logs = []
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            logs = file.readlines()

    return render(request, 'listings/logs.html', {'logs': logs})

# listings/views.py

from django.http import HttpResponse
from .utils import get_user_by_id

def debug_user_view(request):
    user = get_user_by_id(user_id=1)
    if user:
        return HttpResponse(f"User found: {user}")
    return HttpResponse("User not found.")
