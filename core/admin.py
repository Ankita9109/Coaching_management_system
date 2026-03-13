from django.contrib import admin
from .models import Course, Student, Fee, Attendance

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Fee)
admin.site.register(Attendance)
