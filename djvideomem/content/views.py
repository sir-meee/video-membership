from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Course, Video
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import CoursePermissionsMixin


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
       
        context = super().get_context_data(**kwargs)
        
        context['latest_courses'] = Course.objects.order_by('-created_at')[:4]
        context['site_name'] = "My Awesome Site"
        
        return context

        
class CourseListView(ListView):
    model = Course
    template_name = "content/course_list.html"
    queryset = Course.objects.all()


class CourseDetailView(DetailView):
    template_name = "content/course_detail.html"
    queryset = Course.objects.all()


class VideoDetailView(LoginRequiredMixin, CoursePermissionsMixin,DetailView):
    template_name = "content/video_detail.html"

    def get_object(self):
        video = get_object_or_404(Video, slug=self.kwargs["video_slug"])
        return video

    def get_queryset(self):
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        return course.videos.all()