from django.contrib import admin
from django.urls import path, include

from dashboard import views
from dashboard.components.quicklinks.quicklinks import QuicklinksComponent

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path("edit-course/<int:course_id>/", views.edit_course, name="edit_course"),
    path("add-quicklink/", QuicklinksComponent().add_quicklink, name="add_quicklink"),
    path("delete-quicklink/", QuicklinksComponent().delete_quicklink, name="delete_quicklink"),
    path("", include("django_components.urls")),
    path('i18n/', include('django.conf.urls.i18n')),
]
