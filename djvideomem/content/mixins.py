from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Course


class CoursePermissionsMixin:
    def dispatch(self, request, *args, **kwargs):
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        subscription = request.user.subscription
        pricing_tier = subscription.pricing

        print(f"User's Pricing Tier: {pricing_tier}")
        print(f"Course's Allowed Pricing Tiers: {course.pricing_tiers.all()}")

        # Check if the user's pricing tier is not allowed for the course
        if not pricing_tier in course.pricing_tiers.all():
            messages.info(request, "You do not have access to this course")
            return redirect("content:course-list")
        # If the user has access, continue with the request
        return super().dispatch(request, *args, **kwargs)