# 🛒 E-Commerce Backend API

A RESTful E-Commerce Backend API built using **Python, Flask, SQLAlchemy, SQLite, and JWT authentication**.

This project provides backend functionality for users, products, categories, shopping carts, orders, inventory, wishlists, and product reviews.

The API is tested using **Postman** and deployed on **Render**.

---

## 🚀 Live API

**Live URL:**  
https://e-commerce-backend-api-tlah.onrender.com

Test the API:

```text
GET /
```

Response:

```json
{
    "message": "E-Commerce Backend API is running",
    "status": "success"
}
```

---

## ✨ Features

### 🔐 Authentication & Authorization
- User registration and login
- JWT-based authentication
- Protected endpoints
- Role-based authorization
- Admin-only operations
- Password hashing

### 📦 Product Management
- Product CRUD
- Product validation
- Inventory/stock management

### 🗂️ Category Management
- Create and view categories
- Admin-only category creation

### 🔎 Search & Filtering
- Search by product name
- Filter by category
- Minimum/maximum price filtering
- Combined filters

### 🛒 Shopping Cart
- Add, view, update, and remove cart items
- Automatic total calculation
- Stock validation

### 📋 Orders
- Place orders
- Order history and details
- Automatic total calculation
- Stock deduction
- Cart clearing after successful order

### ❤️ Wishlist
- Add, view, and remove wishlist items
- Duplicate prevention

### ⭐ Reviews & Ratings
- Add product reviews
- 1–5 ratings
- View, update, and delete own reviews
- Duplicate review prevention

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | REST API framework |
| Flask-SQLAlchemy | Database ORM |
| SQLite | Database |
| Flask-JWT-Extended | JWT authentication |
| Werkzeug | Password hashing |
| python-dotenv | Environment variables |
| Gunicorn | Production server |
| Postman | API testing |
| Render | Deployment |
| Git & GitHub | Version control |

---

## 🏗️ Project Architecture

```text
Client / Postman
       ↓
    Flask API
       ↓
Authentication & Authorization
       ↓
     Routes
       ↓
     Models
       ↓
   SQLAlchemy
       ↓
     SQLite
```

---

## 📂 Project Structure

```text
E-Commerce-Backend-API/
│
├── models/
│   ├── user.py
│   ├── category.py
│   ├── product.py
│   ├── cart.py
│   ├── order.py
│   ├── wishlist.py
│   └── review.py
│
├── routes/
│   ├── auth_routes.py
│   ├── protected_routes.py
│   ├── admin_routes.py
│   ├── category_routes.py
│   ├── product_routes.py
│   ├── cart_routes.py
│   ├── order_routes.py
│   ├── wishlist_routes.py
│   └── review_routes.py
│
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🔐 Authentication

The API uses **JWT (JSON Web Token)** authentication.

### Register

```http
POST /register
```

Example:

```json
{
    "username": "john",
    "email": "john@example.com",
    "password": "Password@123"
}
```

Newly registered users are assigned the `user` role.

### Login

```http
POST /login
```

Example:

```json
{
    "email": "john@example.com",
    "password": "Password@123"
}
```

Protected requests use:

```text
Authorization: Bearer <JWT_TOKEN>
```

---

# 👥 Role-Based Authorization

The API supports:

```text
user
admin
```

Administrators can perform operations such as creating, updating, and deleting products and creating categories.

Unauthorized users receive appropriate HTTP status codes.

---

# 📡 API Endpoints

## Authentication

| Method | Endpoint | Authentication |
|---|---|---|
| POST | `/register` | Public |
| POST | `/login` | Public |
| GET | `/profile` | JWT |

## Admin

| Method | Endpoint | Authentication |
|---|---|---|
| GET | `/admin` | Admin |

## Categories

| Method | Endpoint | Authentication |
|---|---|---|
| POST | `/categories` | Admin |
| GET | `/categories` | Public |

## Products

| Method | Endpoint | Authentication |
|---|---|---|
| POST | `/products` | Admin |
| GET | `/products` | Public |
| GET | `/products/<id>` | Public |
| PUT | `/products/<id>` | Admin |
| DELETE | `/products/<id>` | Admin |

## Cart

| Method | Endpoint | Authentication |
|---|---|---|
| POST | `/cart` | JWT |
| GET | `/cart` | JWT |
| PUT | `/cart/<item_id>` | JWT |
| DELETE | `/cart/<item_id>` | JWT |

## Orders

| Method | Endpoint | Authentication |
|---|---|---|
| POST | `/orders` | JWT |
| GET | `/orders` | JWT |
| GET | `/orders/<id>` | JWT |

## Wishlist

| Method | Endpoint | Authentication |
|---|---|---|
| POST | `/wishlist` | JWT |
| GET | `/wishlist` | JWT |
| DELETE | `/wishlist/<item_id>` | JWT |

## Reviews

| Method | Endpoint | Authentication |
|---|---|---|
| POST | `/products/<product_id>/reviews` | JWT |
| GET | `/products/<product_id>/reviews` | Public |
| PUT | `/reviews/<review_id>` | JWT |
| DELETE | `/reviews/<review_id>` | JWT |

---

# 🔎 Search & Filtering

Examples:

```http
GET /products?search=headphones
```

```http
GET /products?min_price=2000&max_price=3000
```

```http
GET /products?category_id=1
```

Multiple filters can be combined.

---

# 🛒 Cart Flow

```text
User Login
    ↓
Add Product to Cart
    ↓
Check Product Stock
    ↓
Calculate Cart Total
    ↓
Update Quantity
    ↓
Remove Item
```

---

# 📋 Order Flow

```text
Add Products to Cart
        ↓
     Place Order
        ↓
Check Cart
        ↓
Check Product Stock
        ↓
Calculate Total
        ↓
Create Order
        ↓
Create Order Items
        ↓
Reduce Product Stock
        ↓
Clear Cart
```

The order stores the product price at the time of purchase.

---

# ❤️ Wishlist Flow

```text
User Login
    ↓
Select Product
    ↓
Add to Wishlist
    ↓
View Wishlist
    ↓
Remove Product
```

---

# ⭐ Review Flow

```text
User Login
    ↓
Select Product
    ↓
Submit Rating + Comment
    ↓
View Reviews
    ↓
Update Own Review
    ↓
Delete Own Review
```

Ratings are restricted to **1–5**.

---

# 🛡️ Security & Validation

- JWT authentication
- JWT expiration
- Role-based authorization
- Password hashing
- Protected endpoints
- User ownership checks
- Product and category existence validation
- Stock validation
- Positive cart quantity validation
- Rating validation from 1–5
- Negative price/stock prevention
- Duplicate wishlist/review prevention
- JSON error responses

---

# 🧪 API Testing

The API was tested using **Postman**.

Tested functionality includes:

- Registration and login
- JWT authentication
- Admin authorization
- Product CRUD
- Search and filtering
- Inventory validation
- Cart operations
- Order placement and history
- Wishlist operations
- Review operations
- Error handling and security validation

## Security Testing Results

| Test | Expected | Result |
|---|---|---|
| Profile without JWT | 401 | ✅ |
| Normal user accessing admin | 403 | ✅ |
| Normal user updating product | 403 | ✅ |
| Normal user deleting product | 403 | ✅ |
| Invalid product ID | 404 | ✅ |
| Negative product price | 400 | ✅ |

---

# ⚙️ Local Installation

## 1. Clone the repository

```bash
git clone https://github.com/kumaravel2908-k-m/E-Commerce-Backend-API.git
```

## 2. Open the project

```bash
cd E-Commerce-Backend-API
```

## 3. Create a virtual environment

```bash
python -m venv .venv
```

## 4. Activate on Windows

```bash
.venv\Scripts\activate
```

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
ADMIN_EMAIL=your-admin-email
ADMIN_PASSWORD=your-admin-password
```

Never commit `.env` to GitHub.

---

# ▶️ Run Locally

```bash
python app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

---

# ☁️ Deployment

The API is deployed using **Render**.

Production server:

```text
Gunicorn
```

Start command:

```bash
gunicorn app:app
```

Live API:

https://e-commerce-backend-api-tlah.onrender.com

---

# ⚠️ Database Note

This project currently uses **SQLite** for simplicity and development purposes.

On a free Render service, SQLite data may not persist across certain redeployments or service restarts. For a production e-commerce application, a managed database such as **PostgreSQL** would be recommended.

---

# 🔮 Future Improvements

- PostgreSQL database
- Payment gateway integration
- Product image upload
- Email notifications
- Coupons and discount system
- Redis caching
- Rate limiting
- Swagger/OpenAPI documentation
- Docker containerization
- Automated tests
- CI/CD pipeline
- Order status management
- Advanced product recommendations

---

# 📌 Project Highlights

This project demonstrates:

- REST API development
- Flask application architecture
- SQLAlchemy ORM
- Database relationships
- JWT authentication
- Role-based authorization
- Password security
- Input validation
- CRUD operations
- Query parameters
- Inventory management
- Cart and order processing
- Postman API testing
- Git/GitHub workflow
- Cloud deployment

---

# 🔗 Project Links

### GitHub Repository

https://github.com/kumaravel2908-k-m/E-Commerce-Backend-API

### Live API

https://e-commerce-backend-api-tlah.onrender.com

---

# 👨‍💻 Author

**Kumaravel K M**

B.Tech Information Technology

---

## 📄 License

This project is created for learning, portfolio, and internship purposes.
