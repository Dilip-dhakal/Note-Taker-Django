from note_app import views
from django.urls import path

urlpatterns = [
    path('',views.home,name='home'),
    path('notes/',views.notes_view,name='notes'),
    path('login/',views.login_view,name='login'),
    path('signup/',views.signup_view,name='signup'),
    path('logout/',views.logout_view,name='logout'),
    path("notes/edit/<int:note_id>/", views.edit_note, name="edit_note"),
    path("notes/delete/<int:note_id>/", views.delete_note, name="delete_note"),
]
