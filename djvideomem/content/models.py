from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from allauth.account.signals import email_confirmed 
from allauth.account.models import EmailAddress
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length =30)

    def __str__(self):
        return self.name


class Pricing(models.Model):
    name = models.CharField(max_length=100)  # Basic / Pro / Premium

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE, related_name="subscriptions")
    stripe_subscription_id = models.CharField(max_length=50)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscription for {self.user.email} ({self.pricing.name}) - {self.status} since {self.created_at.strftime('%Y-%m-%d')}"


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnails/")
    category = models.ManyToManyField(Category, blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("content:course-detail", kwargs={"slug":self.slug})

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    vimeo_id = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("content:video-detail", kwargs={
            "video_slug":self.slug,
            "slug":self.course.slug
        })
    

def pre_save_course(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

def pre_save_video(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

def post_email_confirmed(request, email_address, *args, **kwargs):
    user = User.objects.get(email=email_address.email )
    free_trial_pricing = Pricing.objects.get(name="Free Trial")
    subscription = Subscription.objects.create(user=user, pricing=free_trial_pricing)
    stripe_customer = stripe.Customer.create(
        email=user.email
    )
    stripe_subscription = stripe.Subscription.create(
        customer=stripe_customer["id"],
        items = [
            {'price': 'price_1HACxXC5EmFqfM1Pw9BPOeJ1'}
        ],
        trial_period_days=7
    )
    # print(stripe_subscription)
    subscription.status = stripe_subscription["status"]
    subscription.stripe_subscription_id = stripe_subscription["id"]
    subscription.save()

# post_save.connect(post_save_user, sender=User)
email_confirmed.connect(post_email_confirmed)
pre_save.connect(pre_save_course, sender=Course)
pre_save.connect(pre_save_video, sender=Video)