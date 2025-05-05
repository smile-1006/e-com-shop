# 🛒 Django Vue E-commerce Application

## 🚀 Introduction
This project is a full-stack e-commerce web application built with **Django** as the backend and **Vue.js** as the frontend. It supports product browsing, filtering, cart management, and user authentication via mobile OTP. The app provides a modern, responsive UI and a RESTful API for seamless interaction between frontend and backend.

---
Live Backend Deployment:
Access the production backend here 👉 https://e-com-shop.onrender.com

## 🛠️ Technologies Used

### Backend
- Python 3.x 🐍
- Django 5.x 🌐
- Django REST Framework 🔧
- Django Filters
- Twilio API for SMS OTP authentication 📱
- SQLite (default database) 🗄️

### Frontend
- Vue.js 3 🖥️
- Vue Router 🔀
- Vuex for state management 📦
- Axios for API calls ⚡

### Other Tools
- ESLint for code linting 🧹
- Puppeteer (for browser automation in development/testing) 🤖
- VSCode as IDE 💻

---

## 📁 Folder Structure

### Backend (`backend_ecom/`)
```
backend_ecom/
├── app/                  # Custom user model, authentication, core app logic
├── products/             # Product, cart, order models, serializers, views
├── backend/              # Django project settings, URLs, WSGI/ASGI config
├── templates/            # Django HTML templates for server-side rendering
├── manage.py             # Django management script
└── db.sqlite3            # SQLite database file
```

### Frontend (`frontend/`)
```
frontend/
├── src/
│   ├── api/              # Axios API call definitions
│   ├── components/       # Reusable Vue components (Navbar, HelloWorld, etc.)
│   ├── store/            # Vuex store modules (user, products, cart)
│   ├── views/            # Vue pages for routing (Signin, Signup, Order, etc.)
│   ├── router/           # Vue Router configuration
│   ├── assets/           # Static assets like images and styles
│   ├── App.vue           # Root Vue component
│   └── main.js           # Vue app entry point
├── public/               # Public static files
└── package.json          # Frontend dependencies and scripts
```

---

## 🔗 Backend API Endpoints

### Authentication & User Management
- `POST /send-otp/`  
  Request mobile number to receive OTP via SMS.
- `POST /verify-otp/`  
  Verify OTP and authenticate user.

### Products
- `GET /products/`  
  List products with optional filters: category, sold status, price range, search.
- `GET /products/most_bought/`  
  List top 10 most bought products.

### Cart Management
- `GET /cart/`  
  Get current user's cart items.
- `POST /cart/add_to_cart/`  
  Add product to cart.
- `POST /cart/{cart_item_id}/increase_quantity/`  
  Increase quantity of a cart item.
- `POST /cart/{cart_item_id}/decrease_quantity/`  
  Decrease quantity of a cart item.
- `DELETE /cart/{cart_item_id}/remove_from_cart/`  
  Remove item from cart.

### Order Management
- `POST /place_order/`  
  Place an order for items in the cart.
- `GET /get_orders/`  
  Get orders for the authenticated user.
- `POST /cancel_order/{order_id}/`  
  Cancel an order if it is pending.

---

## 🔌 Frontend API Usage
- `sendOtp(mobile)` - Sends OTP to the given mobile number.
- `verifyOtp(mobile, otp)` - Verifies the OTP for the mobile number.
- `fetchProducts(params)` - Fetches products with optional filters.
- `fetchCategories()` - Fetches product categories.
- `fetchCart()` - Fetches current cart items.
- `addToCart(productId, quantity)` - Adds product to cart.
- `increaseCartQuantity(cartItemId)` - Increases quantity of cart item.
- `decreaseCartQuantity(cartItemId)` - Decreases quantity of cart item.
- `removeFromCart(cartItemId)` - Removes item from cart.

---

## 🛠️ Implementation Procedure

1. **Backend Setup:**
   - Create Django project and apps (`app`, `products`).
   - Define models for User, Product, CartManagement, OrderManagement, OrderItem.
   - Implement REST API endpoints using Django REST Framework.
   - Integrate Twilio API for OTP-based authentication.
   - Configure custom User model with mobile number as username.
   - Setup URL routing and permissions.

2. **Frontend Setup:**
   - Initialize Vue.js project.
   - Setup Vue Router for navigation.
   - Setup Vuex for state management (user authentication, cart).
   - Create components and views for product listing, cart, signup, signin.
   - Implement API calls using Axios.
   - Implement OTP login flow with send OTP and verify OTP.
   - Style components with responsive and modern design.

3. **Testing & Deployment:**
   - Test API endpoints with Postman or similar tools.
   - Test frontend functionality and integration.
   - Run backend and frontend servers concurrently.
   - Deploy to production environment as needed.

---

## ▶️ Running the Application

### Backend
1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r backend_ecom/requirements.txt
   ```
3. Apply migrations:
   ```bash
   python backend_ecom/manage.py migrate
   ```
4. Run the development server:
   ```bash
   python backend_ecom/manage.py runserver
   ```

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run serve
   ```
4. Access the frontend at `http://localhost:8080` (default Vue dev server port).

---

## ⚠️ Notes
- Ensure Twilio credentials are set in environment variables or in Django settings.
- The mobile number for OTP must be in E.164 format (e.g., +919876543210).
- The custom User model uses mobile number as the username field.
- Vuex store manages user authentication state and cart state.

---

## 📞 Contact
For any issues or contributions, please open an issue or pull request on the GitHub repository.

---

