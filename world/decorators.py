from django.contrib import messages
from django.shortcuts import redirect



def subscription_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.profile.is_subscribed:
            messages.error(request, "You must subscribe to access this feature.")
            return redirect("subscription_page")
        return view_func(request, *args, **kwargs)
    return wrapper