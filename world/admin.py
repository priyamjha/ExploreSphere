from django.contrib import admin
from django.utils import timezone
from .models import User, Country, State, Region, ChatMessage,Subscription, UserProfile, CustomerRequest, NewsletterSubscription, EmailContent
from django.core.mail import send_mail
from django.conf import settings


admin.site.register(User)
admin.site.register(NewsletterSubscription)
admin.site.register(Country)
admin.site.register(State)


class RegionAdmin(admin.ModelAdmin):
    # Display fields in the list view
    list_display = (
        'name', 'state', 'image', 'hotels_url', 'restaurants_url', 'cottages_url'
    )
    
    # Add filters for better searching
    list_filter = ('state', 'name')
    
    # Add search bar for name, state, and more
    search_fields = ('name', 'state__name')
    
    # Add editable fields in the list display
    list_editable = ('hotels_url', 'restaurants_url', 'cottages_url')
    

# Register your models
admin.site.register(Region, RegionAdmin)


admin.site.register(ChatMessage)
admin.site.register(Subscription)
admin.site.register(UserProfile)

class CustomerRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'status', 'created_at', 'resolved_at')
    list_filter = ('status', 'user')
    search_fields = ('subject', 'description')
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        # Admin action to mark requests as resolved
        queryset.update(status='resolved', resolved_at=timezone.now())
        self.message_user(request, "Selected requests have been marked as resolved.")
    mark_as_resolved.short_description = "Mark selected requests as resolved"

admin.site.register(CustomerRequest, CustomerRequestAdmin)


def send_bulk_newsletter_email(modeladmin, request, queryset):
    # Ensure at least one email content is selected
    if not queryset:
        modeladmin.message_user(request, "Please select an email content to send.")
        return
    
    # You can send the first selected email or handle the case if multiple emails are selected
    email_content = queryset.first()  # Get the first selected email content
    
    if not email_content:
        modeladmin.message_user(request, "No email content found. Please create content first.")
        return

    # Collect all the emails from all subscribers
    email_list = [subscriber.email for subscriber in NewsletterSubscription.objects.all()]
    
    if email_list:
        send_mail(
            subject=email_content.subject,
            message=email_content.message,  # Send the message content (can be HTML if set)
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=email_list,  # Send to all subscribers
            fail_silently=False,
            html_message=email_content.message if email_content.is_html else None  # HTML email support
        )
        modeladmin.message_user(request, f"Newsletter email '{email_content.subject}' has been sent to all subscribers.")
    else:
        modeladmin.message_user(request, "No subscribers found.")
        
# def send_bulk_newsletter_email(modeladmin, request, queryset):
#     # Ensure at least one email content is selected
#     if not queryset:
#         modeladmin.message_user(request, "Please select at least one email content to send.")
#         return
    
#     # Collect all the emails from all subscribers
#     email_list = [subscriber.email for subscriber in NewsletterSubscription.objects.all()]

#     if not email_list:
#         modeladmin.message_user(request, "No subscribers found.")
#         return
    
#     # Loop through the selected email content entries and send them one by one
#     for email_content in queryset:
#         send_mail(
#             subject=email_content.subject,
#             message=email_content.message,  # Send the message content (can be HTML if set)
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=email_list,  # Send to all subscribers
#             fail_silently=False,
#             html_message=email_content.message if email_content.is_html else None  # HTML email support
#         )
#         modeladmin.message_user(request, f"Newsletter email '{email_content.subject}' has been sent to all subscribers.")



# Register EmailContent model with the custom admin action
class EmailContentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at', 'updated_at')
    actions = [send_bulk_newsletter_email]  # Add the custom action to send emails

admin.site.register(EmailContent, EmailContentAdmin)