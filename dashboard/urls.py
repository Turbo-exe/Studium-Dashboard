from django.contrib import admin
from django.urls import path, include

from dashboard import views
from dashboard.components.quicklinks.quicklinks import Quicklinks

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path("edit-course/<int:course_id>/", views.edit_course, name="edit_course"),
    path("add-quicklink/", Quicklinks().add_quicklink, name="add_quicklink"),
    path("delete-quicklink/", Quicklinks().delete_quicklink, name="delete_quicklink"),
    path("", include("django_components.urls")),
]
