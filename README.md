# ExploreSphere Django Web Application


## Description

ExploreSphere is an interactive web application built using Django that allows users to explore different regions in India. It provides users with information about regional details, weather, cultural insights, travel tips, and more. Additionally, users can interact with a chatbot for dynamic queries, make subscription payments, and request support.

## Features

- **User Authentication**: Secure login, registration, and profile management.
- **Region Information**: Detailed pages for various regions, with data on culture, safety, cuisine, attractions, and more.
- **Chatbot Integration**: A dynamic chatbot that uses predefined responses and AI-powered Ollama API to answer user queries about regions.
- **Weather Data**: Fetch live weather data using the OpenWeather API for each region.
- **Subscription System**: Users can subscribe to premium features through Stripe, including access to exclusive content.
- **Support Requests**: Users can create and manage customer support requests.
- **Interactive Maps**: Real-time maps powered by Folium, showing the geographical location of each region.
  
## Technologies Used

- **Django**: Web framework for building the application.
- **PostgreSQL**: Database for storing user and region-related data.
- **Stripe**: Payment gateway for subscription management.
- **Folium**: For creating interactive maps with geographical information.
- **Ollama API**: Used to generate dynamic chatbot responses.
- **OpenWeather API**: Fetches live weather data for regions.

## Requirements

- Python 3.x
- Django 3.x or higher
- Sqlite (or other configured database)
- Stripe API Key
- OpenWeather API Key
- Ollama API Key
- Installed dependencies in `requirements.txt`

## Installation

### Step 1: Clone the repository

Clone the repository to your local machine:

```bash
git clone https://github.com/priyamjha/ExploreSphere.git
```

### Step 2: Set up the environment

Navigate to the project directory and create a virtual environment:

```bash
cd ExploreSphere
python -m venv venv
source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
```

### Step 3: Install dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Step 4: Configure the environment variables

Create a `.env` file in the project root and add the following:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost, 127.0.0.1

DATABASE_URL=postgres://username:password@localhost/dbname

STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key

OPENWEATHER_API_KEY=your_openweather_api_key
OLLAMA_API_URL=http://localhost:11434/v1/chat/completions
```

Make sure to replace placeholders with your actual credentials.

### Step 5: Set up the database

Run the database migrations to set up the schema:

```bash
python manage.py migrate
```

### Step 6: Create a superuser

Create a superuser to access the Django admin interface:

```bash
python manage.py createsuperuser
```

### Step 7: Run the server

Start the Django development server:

```bash
python manage.py runserver
```

You can now access the application at `http://127.0.0.1:8000/`.

## How to Use

### User Authentication

- Users can **register** and **log in** to the platform. Profile management is available, where users can update their details and profile picture.

### Region Information

- On the **Region List** page, users can browse different states and regions in India. Each region has a detailed page showcasing:
  - **Weather Information**: Current weather conditions via OpenWeather API.
  - **Regional Information**: About the region, safety tips, local cuisine, attractions, cultural insights, etc.
  - **Interactive Map**: Displays a map centered around the region’s geographical location, powered by Folium.

### Chatbot

- Users can interact with the **TravelMate chatbot** by sending queries about specific regions. The chatbot utilizes both predefined responses and dynamic AI-powered responses from the Ollama API.

### Subscription

- Users can subscribe to premium content via Stripe. Payment and subscription management are handled through Stripe's checkout process.
  - **Subscription Success**: After a successful payment, users gain access to premium content.
  - **Subscription Invoice**: View invoice details for all subscription-related transactions.

### Support Requests

- Users can create **support requests** which are stored in the database for admins to respond to.

## API Endpoints

- **GET `/regions/<state_id>/`**: Lists all regions for a given state.
- **GET `/region/<region_id>/`**: Displays region-specific information including weather, cultural insights, and a map.
- **POST `/chatbot/<region_id>/`**: Send a user message to the chatbot for dynamic answers regarding the region.
- **POST `/subscription/`**: Initiates the subscription process with Stripe.
  
### Core Components

- **models.py**: Defines all the database models including `Region`, `Subscription`, `ChatMessage`, and `CustomerRequest`.
- **views.py**: Handles the main logic for rendering region pages, handling subscriptions, managing chatbot interactions, and processing support requests.
- **forms.py**: Handles form rendering for user registration, profile updates, and support requests.
- **utils.py**: Contains utility functions like fetching weather data and interacting with the Ollama API.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/) - Web framework for building the project.
- [Stripe](https://stripe.com/) - Payment processing for subscriptions.
- [Folium](https://python-visualization.github.io/folium/) - Used for rendering interactive maps.
- [Ollama API](https://ollama.com/) - AI-powered chatbot service used for dynamic responses.
- [OpenWeather API](https://openweathermap.org/api) - Used for fetching weather information.


### Key Updates:
- **Comprehensive Overview**: The `README.md` provides a full description of your application, its features, and instructions on how to set it up.
- **Step-by-Step Setup**: Clear instructions are provided for installing dependencies, setting up environment variables, and running the server.
- **Technology Stack**: The tools used in the project (Django, Stripe, Folium, Ollama, etc.) are clearly explained.
- **Usage Section**: It details how users can interact with the app, including subscription management, chatbot functionality, and exploring different regions.


