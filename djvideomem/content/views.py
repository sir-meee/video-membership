from django.shortcuts import render
from django.views.generic import ListView
from .models import Course


class CourseListView(ListView):
    model = Course
    template_name = "content/course_list.html"
    queryset = Course.objects.all()