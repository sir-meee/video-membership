from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save


class Course(models.Model):
    name = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to="thumbnails/")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    vimeo_id = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    

def pre_save_course(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

def pre_save_video(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_course, sender=Course)
pre_save.connect(pre_save_video, sender=Video)