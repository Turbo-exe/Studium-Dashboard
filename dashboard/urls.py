from django.contrib import admin
from django.urls import path, include

from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path("add-enrollment/", views.add_enrollment, name="add_enrollment"),
    path("get-enrollment/<int:enrollment_id>/", views.get_enrollment, name="get_enrollments"),
    path("edit-enrollment/<int:enrollment_id>/", views.edit_enrollment, name="edit_enrollment"),
    path("delete-enrollment/<int:enrollment_id>/", views.delete_enrollment, name="delete_enrollment"),
    path("add-quicklink/", views.add_quicklink, name="add_quicklink"),
    path("get-quicklink/<int:quicklink_id>/", views.get_quicklink, name="get_quicklink"),
    path("delete-quicklink/<int:quicklink_id>/", views.delete_quicklink, name="delete_quicklink"),
    path("", include("django_components.urls")),
    path('i18n/', include('django.conf.urls.i18n')),
]
