from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Notes, UserProfile
import pytz

def home(request):
    return render(request,'note_app/home.html')# -------------------- SIGNUP --------------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        timezone = request.POST.get("timezone", "UTC")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, password=password)
            UserProfile.objects.create(user=user, timezone=timezone)
            login(request, user)
            return redirect("notes")
    timezones = [(tz, tz) for tz in pytz.common_timezones]
    return render(request, "note_app/signup.html", {"timezones": timezones})

# -------------------- LOGIN --------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("notes")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "note_app/login.html")

# -------------------- LOGOUT --------------------
def logout_view(request):
    logout(request)
    return redirect("login")

# -------------------- NOTES --------------------
@login_required
def notes_view(request):
    # Ensure UserProfile exists
    UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'timezone': 'UTC'}
    )

    if request.method == "POST":
        note_title = request.POST.get("notes", "")
        note_desc = request.POST.get("description", "")
        if note_title and note_desc:
            Notes.objects.create(
                user=request.user,
                notes=note_title,
                description=note_desc,
                
            )
        return redirect("notes")

    all_notes = Notes.objects.filter(user=request.user).order_by("-created_at")
    user_timezone = request.user.userprofile.timezone
    for note in all_notes:
        note.created_at = note.created_at.astimezone(pytz.timezone(user_timezone))
    return render(request, "note_app/notes.html", {"all_notes": all_notes})

# -------------------- EDIT --------------------
@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Notes, id=note_id, user=request.user)
    if request.method == "POST":
        note_title = request.POST.get("notes")
        note_desc = request.POST.get("description")
        if note_title and note_desc:
            note.notes = note_title
            note.description = note_desc
            note.save()
            return redirect("notes")
    return render(request, "note_app/edit_note.html", {"note": note})

# -------------------- DELETE --------------------
@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Notes, id=note_id, user=request.user)
    note.delete()
    return redirect("notes")
