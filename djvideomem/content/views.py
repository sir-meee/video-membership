from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Course


class CourseListView(ListView):
    model = Course
    template_name = "content/course_list.html"
    queryset = Course.objects.all()


class CourseDetailView(DetailView):
    template_name = "content/course_detail.html"
    queryset = Course.objects.all()