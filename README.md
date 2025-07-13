# ecomm_website
product review project with django DRF

# 🛒 Django Product Review API

A RESTful Product Review System built using Django and Django REST Framework.  
Supports **admin product management**, **user reviews**, and **authentication with role-based access**.

---

## 🚀 Features

### 🔐 Authentication & Roles
- Admins and regular users
- Login, logout, and registration with API tokens
- Only authenticated users can review

### 🛍️ Product Management
- Admins: Create, update, delete products
- Users: Browse product catalog with filters
- Products include name, description, price, image, and category

### ⭐ Review System
- Authenticated users can post **one review per product**
- Reviews include rating (1-5) and feedback
- Product ratings are **aggregated automatically**
- Admins can delete any review

### 🔄 API Endpoints
- `/api/products/` — View all products (All users)
- `/api/reviews/` — Submit/view reviews (Users)
- `/api/users/` — Admins can view/manage users
- `/api/register/` — Register new users
- `/api/login/` — Login to get token
- `/api/logout/` — Logout and invalidate token

---

## 🛠️ Tech Stack

- Python 3
- Django 4.x
- Django REST Framework
- SQLite3 (or use PostgreSQL in production)

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser (admin)
python manage.py createsuperuser

# Run the server
python manage.py runserver
