from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid




class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Add username here for superuser creation

    

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, related_name="states", on_delete=models.CASCADE)
    svg_id = models.CharField(
        max_length=50,
        unique=True,
        help_text="ID of the SVG path for this state. Must match the 'id' attribute in the SVG file.",
    )
    path_data = models.TextField(
        help_text="The 'd' attribute data for the SVG path of this state."
    )
    bio = models.TextField(help_text="A short bio about this state.", blank=True)

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, related_name="regions", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='regions/', blank=True, null=True)
    head_line = models.TextField(help_text="A short note about this region.", blank=True)
    bio = models.TextField(help_text="A short bio about this region.", blank=True)
    latitude = models.FloatField(help_text="Latitude of the region", blank=True, null=True)
    longitude = models.FloatField(help_text="Longitude of the region", blank=True, null=True)
    hotels_url = models.URLField(help_text="URL for hotels", blank=True, null=True)
    cottages_url = models.URLField(help_text="URL for hostels", blank=True, null=True)
    restaurants_url = models.URLField(help_text="URL for restaurants", blank=True, null=True)
    local_cuisine = models.TextField(help_text="Local cuisine about this region. Example: Must-Try Foods: Dal Baati", blank=True)
    popular_activities = models.TextField(help_text="Popular activities about this region. Example: Trekking Boating Beach", blank=True)
    estimate_cost = models.TextField(help_text="Estimate cost about this region. Example: Avg. Daily Cost: ₹2000-₹3000.", blank=True)
    travel_tips = models.TextField(help_text="Travel tips about this region. Example: Best Time to Visit: October to February. Weather: Moderate. Tip: Carry warm clothing.", blank=True)
    top_attractions = models.TextField(help_text="Top attractions about this region. Example: Top Attractions: XYZ Temple, ABC Park.", blank=True)
    events_festival = models.TextField(help_text="Events and Festival about this region. Example: Upcoming Festival: Desert Festival (Feb 15-18).", blank=True)
    safety_info = models.TextField(help_text="Safety and Emergency Info about the region. Example: Emergency Contact: 100 (Police), 108 (Ambulance).", blank=True)
    cultural_insights = models.TextField(help_text="cultural insights about the region. Example: Local Language: Hindi. Traditions: Remove shoes before entering temples.", blank=True)

    def __str__(self):
        return self.name



class ChatMessage(models.Model):
    region = models.ForeignKey('Region', related_name="chat_messages", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"



class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription")
    is_active = models.BooleanField(default=False)
    sub_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    payment_date = models.DateField(auto_now_add=True)

    def activate_subscription(self):
        self.is_active = True
        self.save()

    def __str__(self):
        return f"Subscription for {self.user.username} - Active: {self.is_active}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class CustomerRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    solution = models.TextField(null=True, blank=True)  # Admin solution

    def __str__(self):
        return f"Request from {self.user.username}: {self.subject}"
    
    


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class EmailContent(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()  # You can use `TextField` for HTML content as well
    is_html = models.BooleanField(default=True)  # To determine if the email is HTML or plain text
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject