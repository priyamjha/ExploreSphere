from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import User, Country, State, Region, ChatMessage, Subscription, CustomerRequest, NewsletterSubscription  
from .forms import UserForm, MyUserCreationForm, CustomerRequestForm, NewsletterForm
import folium
from .utils import get_weather
import json
from django.http import JsonResponse
import stripe
from django.conf import settings
from .decorators import subscription_required
import requests
from datetime import datetime
from django.db.models import Prefetch
from django.core.mail import send_mail





stripe.api_key = settings.STRIPE_SECRET_KEY


OLLAMA_API_URL = 'http://localhost:11434/v1/chat/completions'  # Make sure this is the correct API endpoint

def get_ollama_response(query, region_name):
    """Fetch concise dynamic content using the Ollama API."""
    
    # Craft a short, direct system message
    system_message = f"""
    Your name is TravelMate. You are an assistant providing clear, brief answers about India's regions. 
    Respond in short, simple sentences. Provide essential information and use emojis to make it engaging.
    Avoid unnecessary details and special characters like '*' and '#', stars, hashtags, or long explanations.
    """

    # Create the payload with a more specific query
    payload = {
        "model": "gemma:2b",  # Or your specific model
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Tell me about {region_name} focusing on: {query}"}
        ],
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse and return a concise answer
        data = response.json()
        
        if 'choices' in data and len(data['choices']) > 0:
            return data['choices'][0].get('message', {}).get('content', "Sorry, I couldn't find any relevant information.")
        else:
            return "Sorry, I couldn't fetch the information. Please try again later."
    
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during request: {e}")
        return "Sorry, I couldn't fetch the information. Please try again later."

    except Exception as e:
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred. Please try again later."




@subscription_required
def chatbot(request, region_id):
    region = Region.objects.get(id=region_id)

    # Initialize the conversation for this specific region if not already in session
    conversation_key = f'conversation_{region_id}'
    options_key = f'options_{region_id}'

    if conversation_key not in request.session:
        request.session[conversation_key] = []

    # Initialize timestamp if it's the user's first interaction
    if 'chat_start_time' not in request.session:
        request.session['chat_start_time'] = datetime.now().timestamp()

    # Check if 5 minutes have passed since the last interaction
    if datetime.now().timestamp() - request.session['chat_start_time'] > 60 * 60:
        # If 60 minutes have passed, clear the conversation and reset the start time
        request.session[conversation_key] = []
        request.session['chat_start_time'] = datetime.now().timestamp()

    user_message = ""
    bot_response = ""
    options = []  # Default: no options to show at first

    if request.method == "POST":
        user_message = request.POST.get("message")

        if user_message:
            # Add the user's message to the conversation history for this region
            request.session[conversation_key].append({"role": "user", "content": user_message})

            # Predefined responses based on user message
            greeting_keywords = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'yo', 'what’s up', 'sup']
            if any(greeting in user_message.lower() for greeting in greeting_keywords):
                bot_response = "Namaste 🙏! What would you like to know about?"
                options = [
                    "⚠️ Safety", "💸 Cost", "💡 Tips", "🏛️ Culture"
                ]
            # Handle variations of "bio" inquiries
            elif any(phrase in user_message.lower() for phrase in ['bio', 'about the region', 'information about the region', 'region bio', 'overview', 'summary']):
                bot_response = region.bio if region.bio else "No bio available for this region."
            # Handle variations of "safety" inquiries
            elif any(phrase in user_message.lower() for phrase in ['safety', 'safety info', 'safety information', 'emergency', 'travel safety', 'safety precautions']):
                bot_response = region.safety_info if region.safety_info else "No safety information available."
            # Handle variations of "local cuisine" inquiries
            elif any(phrase in user_message.lower() for phrase in ['local cuisine', 'food', 'must-try foods', 'regional cuisine', 'specialty dishes', 'best food']):
                bot_response = region.local_cuisine if region.local_cuisine else "No information about local cuisine."
            # Handle variations of "cost" inquiries
            elif any(phrase in user_message.lower() for phrase in ['cost', 'estimate cost', 'expenses', 'average cost', 'budget', 'price range', 'how much does it cost']):
                bot_response = region.estimate_cost if region.estimate_cost else "No cost estimate available."
            # Handle variations of "attractions" inquiries
            elif any(phrase in user_message.lower() for phrase in ['attractions', 'top attractions', 'must-see places', 'sightseeing', 'tourist spots', 'landmarks']):
                bot_response = region.top_attractions if region.top_attractions else "No information about attractions."
            # Handle variations of "tips" inquiries
            elif any(phrase in user_message.lower() for phrase in ['tips', 'travel tips', 'advice', 'guidelines', 'recommendations', 'suggestions']):
                bot_response = region.travel_tips if region.travel_tips else "No travel tips available."
            # Handle variations of "events" inquiries
            elif any(phrase in user_message.lower() for phrase in ['events', 'festivals', 'upcoming events', 'regional festivals', 'local events', 'what’s happening']):
                bot_response = region.events_festival if region.events_festival else "No event information available."
            # Handle variations of "cultural insights" inquiries
            elif any(phrase in user_message.lower() for phrase in ['culture', 'cultural insights', 'traditions', 'local culture', 'heritage', 'customs', 'local customs']):
                bot_response = region.cultural_insights if region.cultural_insights else "No cultural insights available."
            else:
                # If the question doesn't match predefined queries, ask Ollama for help
                bot_response = get_ollama_response(user_message, region.name)
                options = [
                    "⚠️ Safety", "💸 Cost", "💡 Tips", "🏛️ Culture"
                ]
            
            # Add the bot's response to the conversation history for this region
            request.session[conversation_key].append({"role": "bot", "content": bot_response})

            # Store the options in the session for this region
            request.session[options_key] = options

            # Save session data
            request.session.modified = True

            # Redirect to prevent re-posting on refresh
            return redirect('chatbot', region_id=region_id)

    # Retrieve the options from session only if a message has been sent
    options = request.session.get(options_key, [])

    return render(request, 'base/chatbot.html', {
        'region': region,
        'conversation': request.session[conversation_key],
        'options': options
    })






@subscription_required
def create_request(request):
    # Handle creation of new support request
    if request.method == 'POST' and 'create_request' in request.POST:
        form = CustomerRequestForm(request.POST)
        if form.is_valid():
            customer_request = form.save(commit=False)
            customer_request.user = request.user
            customer_request.save()
            return redirect('create_request')
    else:
        form = CustomerRequestForm()

    # Fetch all requests of the user or all requests for admin, ordered by created_at in descending order
    requests = CustomerRequest.objects.filter(user=request.user).order_by('-created_at') if not request.user.is_staff else CustomerRequest.objects.all().order_by('-created_at')
    
    return render(request, 'base/create_request.html', {'form': form, 'requests': requests})




@login_required
def subscription_page(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            price_id = data.get('priceId')

            if not price_id:
                return JsonResponse({"error": "Price ID is required."}, status=400)

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="payment",  # Use 'payment' mode for one-time payment
                line_items=[{
                    "price": price_id,
                    "quantity": 1,
                }],
                success_url=request.build_absolute_uri("/subscription/success/"),
                cancel_url=request.build_absolute_uri("/subscription/cancel/"),
            )

            return JsonResponse({'url': session.url})

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect("subscribe")

    return render(request, "base/subscription.html", {
        "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
    })



@login_required
def subscription_success(request):
    try:
        # Mark the user as subscribed
        profile = request.user.profile
        profile.is_subscribed = True
        profile.save()

        # Create or update the Subscription instance
        subscription, created = Subscription.objects.get_or_create(user=request.user)
        subscription.activate_subscription()


        messages.success(request, "Subscription successful! You can now access all features.")
        
        # Redirect to the invoice page after success
        return render(request, "base/subscription_success.html", {
            "subscription": subscription
        })

    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect("home")

    
    
    
@login_required
def subscription_invoice(request):
    try:
        # Get the user's subscription details
        subscription = Subscription.objects.get(user=request.user)
        
        # Pass subscription details to the template
        return render(request, "base/subscription_invoice.html", {
            "subscription": subscription
        })

    except Subscription.DoesNotExist:
        messages.error(request, "No subscription found.")
        return redirect("home")




def delete_message(request, message_id):
    # Fetch the message
    message = ChatMessage.objects.get(id=message_id)
    
    # Check if the current user is the message's author or an admin
    if message.user == request.user or request.user.is_staff:
        message.delete()  # Delete the message
        
    # Redirect back to the region detail page after deleting
    return redirect('region_detail', region_id=message.region.id)


def region_list(request, state_id):
    state = State.objects.get(id=state_id)
    regions = Region.objects.filter(state=state)
    return render(request, 'base/region_list.html', {'state': state, 'regions': regions})



def region_detail(request, region_id):
    # Use select_related to optimize queries for related fields like state, user (if needed), etc.
    region = Region.objects.select_related('state').get(id=region_id)
    weather = None

    # Only fetch weather if latitude and longitude are valid
    if region.latitude and region.longitude:
        weather = get_weather(region.latitude, region.longitude)

    # Fetch chat messages with prefetch_related to optimize fetching related User model
    chat_messages = ChatMessage.objects.filter(region=region).order_by('timestamp').select_related('user')

    # Create folium map only if latitude and longitude are available
    map_html = None
    if region.latitude and region.longitude:
        m = folium.Map(location=[region.latitude, region.longitude], zoom_start=12)
        folium.Marker([region.latitude, region.longitude], popup=f"{region.name}").add_to(m)
        map_html = m._repr_html_()

    return render(request, 'base/region_detail.html', {
        'region': region,
        'map_html': map_html,
        'weather': weather,
        'chat_messages': chat_messages,
    })



# def region_detail(request, region_id):
#     # Use select_related to optimize queries for related fields like state, user (if needed), etc.
#     region = Region.objects.select_related('state').get(id=region_id)
#     weather = None

#     # Only fetch weather if latitude and longitude are valid
#     if region.latitude and region.longitude:
#         weather = get_weather(region.latitude, region.longitude)

#     # Fetch chat messages with prefetch_related to optimize fetching related User model
#     chat_messages = ChatMessage.objects.filter(region=region).order_by('timestamp').select_related('user')

#     if request.method == "POST" and request.user.is_authenticated:
#         message_text = request.POST.get("message")
#         if message_text:
#             ChatMessage.objects.create(region=region, user=request.user, message=message_text)

#         # After the message is sent, redirect to avoid re-submission
#         return redirect('region_detail', region_id=region.id)

#     # Create folium map only if latitude and longitude are available
#     map_html = None
#     if region.latitude and region.longitude:
#         m = folium.Map(location=[region.latitude, region.longitude], zoom_start=12)
#         folium.Marker([region.latitude, region.longitude], popup=f"{region.name}").add_to(m)
#         map_html = m._repr_html_()

#     return render(request, 'base/region_detail.html', {
#         'region': region,
#         'map_html': map_html,
#         'weather': weather,
#         'chat_messages': chat_messages,
#     })
    
    

def home(request):
    country = Country.objects.get(name="India")
    states = country.states.all()
    
    query = request.GET.get('q', '')  # Get the search query
    if query:
        # Search for matching states and regions by name
        states = country.states.filter(name__icontains=query)
        regions = Region.objects.filter(name__icontains=query)  # Ensure it's checking the correct field
    else:
        # If no query, display all states
        states = country.states.all()
        regions = Region.objects.all()
        
    # Get the most recent 5 chat messages (you can adjust this number as needed)
    recent_activities = ChatMessage.objects.select_related('user', 'region').order_by('-timestamp')[:7]
    
    return render(request, 'base/home.html', {'states': states, 'regions': regions, 'recent_activities': recent_activities})





def front(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to sign up for the newsletter.")
            return redirect('login')
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
                        
            # Save the email to the NewsletterSubscription model
            NewsletterSubscription.objects.create(email=email)
            
            # Send the confirmation email
            send_mail(
    subject="Thank You for Signing Up for Our Newsletter!",  # Subject
    message="""
        Hello,

        Thank you for signing up for our newsletter! We're thrilled to have you join our community. By subscribing, you'll stay updated on the latest news, exciting developments, and exclusive special offers. 

        As a subscriber, you can expect to receive:
        - News and updates about our latest regions and services
        - Special promotions and offers available only to our newsletter members
        - Tips and insights to help you get the most out of our products/services

        We value your interest and are committed to keeping you informed and engaged with content tailored just for you.

        If you ever want to update your preferences or unsubscribe, you'll find the options at the bottom of every email we send.

        Thank you again for your support, and we look forward to connecting with you!

        Best regards,
        The Explore Sphere Team
        https://explorespheree.pythonanywhere.com/

        P.S. Feel free to share this newsletter with friends and family who may also be interested!
    """, 
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[email],
    fail_silently=False,
)

            
            # Show success message to the user
            messages.success(request, "Thank you for signing up! A confirmation email has been sent to your inbox.")
            return redirect('home')
        else:
            messages.success(request, "This email is already subscribed.")
            return redirect('home')
            
    else:
        form = NewsletterForm()

    return render(request, 'base/front.html', {'form': form})


# def fetch_tavus_video():
#     url = "https://tavusapi.com/v2/videos/video id"

#     headers = {"x-api-key": "api-key"}
    
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Will raise an error if the status code is not 200
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching video data: {e}")
#         return None



# def front(request):  
#     video_data = fetch_tavus_video()
#     if request.method == 'POST':
#         if not request.user.is_authenticated:
#             messages.warning(request, "You must be logged in to sign up for the newsletter.")
#             return redirect('login')
#         form = NewsletterForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
                        
#             # Save the email to the NewsletterSubscription model
#             NewsletterSubscription.objects.create(email=email)
            
#             # Send the confirmation email
#             send_mail(
#     subject="Thank You for Signing Up for Our Newsletter!",  # Subject
#     message="""
#         Hello,

#         Thank you for signing up for our newsletter! We're thrilled to have you join our community. By subscribing, you'll stay updated on the latest news, exciting developments, and exclusive special offers. 

#         As a subscriber, you can expect to receive:
#         - News and updates about our latest regions and services
#         - Special promotions and offers available only to our newsletter members
#         - Tips and insights to help you get the most out of our products/services

#         We value your interest and are committed to keeping you informed and engaged with content tailored just for you.

#         If you ever want to update your preferences or unsubscribe, you'll find the options at the bottom of every email we send.

#         Thank you again for your support, and we look forward to connecting with you!

#         Best regards,
#         The Explore Sphere Team
#         https://explorespheree.pythonanywhere.com/

#         P.S. Feel free to share this newsletter with friends and family who may also be interested!
#     """, 
#     from_email=settings.DEFAULT_FROM_EMAIL,
#     recipient_list=[email],
#     fail_silently=False,
# )

            
#             # Show success message to the user
#             messages.success(request, "Thank you for signing up! A confirmation email has been sent to your inbox.")
#             return redirect('home')
#         else:
#             messages.success(request, "This email is already subscribed.")
#             return redirect('home')
            
#     else:
#         form = NewsletterForm()

#     return render(request, 'base/front.html', {'form': form, 'video_data': video_data})




def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})





@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/update-user.html', {'form': form})

