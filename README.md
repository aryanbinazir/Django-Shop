
# Django-Shop

An e-commerce web application built with Django that allows users to browse products without login and manage their shopping cart after authentication.

## 🚀 Features

- 🛍 Browse products without login
- 🔑 User authentication and registration
- 🛒 Add, remove, and manage products in user’s shopping cart
- 💳 Checkout and payment integration (planned)
- 🔄 Forgot password and OTP verification
- 🔧 Admin panel for managing products and orders

## 🛠 Tech Stack

- Python 3
- Django
- Bootstrap (frontend styling)
- Celery & RabbitMQ (task queue for async tasks)
- SQLite (default DB, can be changed)

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/aryanbinazir/Django-Shop.git
cd Django-Shop
```

### 2. Create Virtual Environment and Activate

```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser (for admin panel)

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open `http://localhost:8000` to browse the shop.

## 🔍 App Overview

- **Product Catalog:** Browse all products without login.
- **User Authentication:** Register, login, logout, password reset with OTP.
- **Shopping Cart:** Authenticated users can add/remove products and proceed to checkout.
- **Admin Panel:** Manage products, orders, and users.

## 🔧 Additional Info

- Celery is configured to handle async tasks via RabbitMQ (make sure RabbitMQ is running).
- Payment integration is a planned feature.
- The project uses Bootstrap for UI components.

## 🧪 Running Tests

```bash
python manage.py test
```

## 📂 Project Structure (simplified)

```
Django-Shop/
├── shop/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── static/
├── manage.py
├── requirements.txt
└── celery.py
```
