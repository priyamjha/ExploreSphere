# 🌏 ExploreSphere – Discover India Like Never Before

## 📝 Description

**ExploreSphere** is an interactive and intelligent travel exploration platform built with Django. It enables users to dive deep into India’s regional diversity through cultural insights, weather information, attractions, cuisine, and safety tips. The platform offers personalized features like AI-powered chat, subscription services, and even a video-based AI guide powered by **Tavus.io** to explain the website’s purpose!

## 🚀 Features

- 🔐 **User Authentication** – Secure login, registration, and profile management.
- 📍 **Regional Exploration** – Pages rich with cultural, culinary, and safety information for different Indian regions.
- 🤖 **AI TravelMate Chatbot** – Dynamic travel Q&A bot using the **Ollama API**.
- 🌦️ **Live Weather Updates** – Integrated with the **OpenWeather API**.
- 💳 **Premium Subscriptions** – Unlock exclusive content via **Stripe** checkout.
- 🗺️ **Interactive Maps** – Regional maps built using **Folium**.
- 📬 **Newsletter Subscription** – Stay updated with curated travel tips and updates.
- 🧠 **AI Video Guide** – AI agent video (powered by **Tavus.io**) that introduces the site and its features.
- 🛠️ **Support System** – Users can create and track support requests.

---

## 🛠️ Technologies Used

- **Backend**: Django, Django REST Framework
- **Database**: SQLite
- **Payment Gateway**: Stripe
- **Chatbot**: Ollama API
- **Maps**: Folium
- **Weather**: OpenWeather API
- **AI Video Agent**: Tavus.io
- **Newsletter**: Custom Email Integration (SMTP-based)

---

## ⚙️ Requirements

- Python 3.x  
- Django 3.x or above  
- SQLite  
- Stripe, OpenWeather, and Ollama API keys  
- Virtual environment (`venv`)  
- All Python packages in `requirements.txt`

---

## 🧩 Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/priyamjha/ExploreSphere.git
cd ExploreSphere
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root folder:

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=postgres://username:password@localhost/dbname

STRIPE_SECRET_KEY=your_stripe_secret
STRIPE_PUBLISHABLE_KEY=your_stripe_public

OPENWEATHER_API_KEY=your_weather_key
OLLAMA_API_URL=http://localhost:11434/v1/chat/completions
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Create Admin User

```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```

---

## 🧭 Usage Instructions

### 🌍 Region Exploration

- Visit the **Regions** section to explore state-wise data on culture, cuisine, weather, maps, and more.

### 💬 Chatbot

- Chat with the **TravelMate** bot for travel guidance and region-based suggestions.

### 💎 Premium Subscription

- Unlock premium content via **Stripe checkout**. Users get:
  - Advanced regional insights
  - Early newsletter access
  - Chatbot enhancements

### 📺 AI Video Agent

- Meet our AI spokesperson powered by **Tavus.io**, who walks you through ExploreSphere’s goals and features.

### 📰 Newsletter

- Sign up to our newsletter to receive travel stories, cultural tips, and platform updates right in your inbox.

### ❓ Support

- Create and manage **support tickets** for any issues or feedback.

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/regions/<state_id>/` | GET | List all regions under a state |
| `/region/<region_id>/` | GET | Region details + weather + map |
| `/chatbot/<region_id>/` | POST | Ask chatbot questions |
| `/subscription/` | POST | Stripe subscription process |
| `/newsletter/` | POST | Subscribe to newsletter |

---

## 🗂️ Code Structure Highlights

- `models.py` – Region, Subscription, ChatMessage, Newsletter, CustomerRequest  
- `views.py` – Business logic for all core features  
- `forms.py` – User auth, profile, newsletter, and support forms  
- `utils.py` – Utility functions for APIs and chatbot

---

## 📄 License

MIT License – see the [LICENSE](LICENSE) file.

---

## 🙌 Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Stripe](https://stripe.com/)
- [Folium](https://python-visualization.github.io/folium/)
- [Ollama](https://ollama.com/)
- [OpenWeather](https://openweathermap.org/api)
- [Tavus.io](https://tavus.io) – For AI video integration

---

Let me know if you want this README in a downloadable `.md` file or if you'd like a badge-based header section like:
```
![Django](https://img.shields.io/badge/Django-3.x-blue)
...
