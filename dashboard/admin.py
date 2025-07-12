from django.contrib import admin

from dashboard import models

admin.site.register(models.Exam)
admin.site.register(models.Course)
admin.site.register(models.Degree)
admin.site.register(models.Student)
admin.site.register(models.Semester)
admin.site.register(models.Enrollment)
admin.site.register(models.Quicklink)
