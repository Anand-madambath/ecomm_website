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
- Authenticated users can post one review per product
- Reviews include rating (1-5) and feedback
- Product rating

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
- Django 
- Django REST Framework
- SQLite3


