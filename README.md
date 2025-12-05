# 🛒 Allora Shop Backend  
A clean and modular backend for **Allora Shop**, built with **Django + Django REST Framework**.  
This service provides authentication, product management, comments, wishlist, discounts, tickets, and user profile APIs for a Next.js frontend.

---

## 🚀 Tech Stack
- **Python 3.11**
- **Django 5**
- **Django REST Framework**
- **PyJWT** (Authentication)
- **SQLite** (Dev database)
- **CORS + Cookie-based JWT**

---

## 📦 Features

### 🔐 Authentication
- Signup / Login / Logout  
- JWT Access Token stored in HttpOnly cookie  
- User roles (USER / ADMIN)  
- `/api/auth/me/` returns logged-in user  

### 🛍 Products
- Create products (Admin)  
- Upload multiple images  
- Fully supports variants (color, size, stock, price)  
- Product score auto-calculated from comments  

### ⭐ Comments
- Add comments with score (1–5)  
- Admin approve/reject  
- Auto-update product average score  

### ❤️ Wishlist
- Add / Remove product from wishlist  

### 🎫 Discounts
- Validate discount code  
- Track usage count (maxUse / uses)  

### 🎟 Tickets
- Users can send tickets  
- Admin can answer tickets  
- Replies are linked to main ticket  

### 👤 User
- Update profile  
- Ban user (email + phone)  
- Toggle role (USER ↔ ADMIN)  

---

## 🗂 Project Setup

### 1. Clone
```bash
git clone <REPO_URL>
cd allora_backend
```

### 2. Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate     # Linux/macOS
# .venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver 8000
```

Backend runs at:
```
http://127.0.0.1:8000
```

---

## 🔌 Essential API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/signup/ | Register |
| POST | /api/auth/signin/ | Login |
| POST | /api/auth/signout/ | Logout |
| GET | /api/auth/me/ | Current user |

### Products
| Method | Endpoint |
|--------|----------|
| GET | /api/products/ |
| POST | /api/products/ |

### Comments
| Method | Endpoint |
|--------|----------|
| GET | /api/comments/ |
| POST | /api/comments/ |
| PUT | /api/comments/accept/ |
| PUT | /api/comments/reject/ |

### Wishlist
| Method | Endpoint |
|--------|----------|
| POST | /api/wishlist/ |
| DELETE | /api/wishlist/<product_id>/ |

### Discounts
| Method | Endpoint |
|--------|----------|
| PUT | /api/discounts/use/ |

### Tickets
| Method | Endpoint |
|--------|----------|
| POST | /api/tickets/ |
| POST | /api/tickets/answer/ |

### User
| Method | Endpoint |
|--------|----------|
| POST | /api/user/ |
| POST | /api/user/ban/ |
| PUT | /api/user/role/ |

---

## 🌐 Frontend Integration
Frontend **must** send requests with cookies:

```ts
fetch("/api/...", {
  method: "...",
  credentials: "include",
  headers: { "Content-Type": "application/json" },
});
```


---

## 👨‍💻 Developer
Backend Developer: **AkbarMansourifar**

