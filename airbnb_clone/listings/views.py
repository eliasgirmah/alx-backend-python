from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
import os
from django.conf import settings

from .models import Listing
from .utils import (
    get_users_query,
    get_user_by_id,
    update_user_email,
    fetch_users_with_retry,
)

# Show all listings
def listing_list(request):
    listings = Listing.objects.all()
    return render(request, 'listings/home.html', {'listings': listings})

# Show listing details by primary key
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'listings/detail.html', {'listing': listing})

# Admin-only view to display log file contents
@staff_member_required
def view_logs(request):
    log_file_path = os.path.join(settings.BASE_DIR, 'user_queries.log')
    logs = []
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            logs = file.readlines()
    return render(request, 'listings/logs.html', {'logs': logs})

# Debug: Show user with id=1 using DB utility
def debug_user_view(request):
    user = get_user_by_id(user_id=1)
    if user:
        return HttpResponse(f"User found: {user}")
    return HttpResponse("User not found.")

# Debug: Show all users from raw SQL query
def debug_all_users_view(request):
    users = get_users_query()
    usernames = ", ".join([str(user['username']) for user in users])  # FIX: If user is a dict
    return HttpResponse(f"Users: {usernames}")

# Debug: Update email of user with id=1 and report success/error
def debug_update_email_view(request):
    try:
        update_user_email(user_id=1, new_email='debug_updated@example.com')
        return HttpResponse("Email updated successfully!")
    except Exception as e:
        return HttpResponse(f"Error occurred: {str(e)}")

# Debug: Fetch users with retry decorator and show result
def debug_fetch_users(request):
    try:
        users = fetch_users_with_retry()
        usernames = ", ".join(str(user) for user in users)
        return HttpResponse(f"Users fetched: {usernames}")
    except Exception as e:
        return HttpResponse(f"Failed to fetch users: {e}")
