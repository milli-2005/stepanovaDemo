from django.contrib import admin

from .models import CourseApplication, Profile, Review


admin.site.register(Profile)
admin.site.register(CourseApplication)
admin.site.register(Review)

#register your models here