# Tradexa Technologies — Django Assignment

A Django 4.2 application demonstrating multi-database architecture, custom user models, and authenticated post creation.

---

## Features

| Feature | Detail |
|---|---|
| Custom User Model | `AbstractBaseUser` with `first_name`, `last_name`, `email`, `password`, `username` |
| Post Model | `user`, `text`, `created_at`, `updated_at`; logical FK (no DB constraint) |
| Product Model | `name`, `weight`, `price`, `created_at`, `updated_at` |
| Dual Databases | `db_users.sqlite3` (users/posts) · `db_products.sqlite3` (products) |
| Database Router | `ProductsRouter` auto-routes all reads/writes |
| Auth | Login, Register, Logout with custom `UserManager` |
| Post Form | Authenticated users only; image upload supported |
| CRUD Products | Create / Read / Update / Delete with search & pagination |
| Django Admin | Both models registered with full configurations |
| Pagination | 10 posts · 12 products per page |

---

## Project Structure

```
tradexa/
├── tradexa_project/
│   ├── settings.py          # DATABASES, AUTH_USER_MODEL, routers
│   ├── routers.py           # ProductsRouter — dual DB routing
│   └── urls.py
├── users/                   # App 1 → db_users.sqlite3
│   ├── models.py            # User, Post
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── products/                # App 2 → db_products.sqlite3
│   ├── models.py            # Product
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
└── templates/
    ├── base.html
    ├── users/
    └── products/
```

---

## Quick Start

```bash
# 1. Create & activate virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations (both databases)
python manage.py migrate --database=default
python manage.py migrate --database=products_db

# 4. (Optional) Create superuser
python manage.py createsuperuser

# 5. Start server
python manage.py runserver
```

Visit http://127.0.0.1:8000

---

## Demo Accounts (pre-seeded)

| Role | Email | Password |
|---|---|---|
| User | alice@tradexa.com | demo1234 |
| User | bob@tradexa.com | demo1234 |
| Admin | admin@tradexa.com | admin1234 |

---

## Key Design Decisions

### 1. Custom User Model
Extends `AbstractBaseUser` + `PermissionsMixin`. Authentication uses **email** (not username). The `UserManager` provides `create_user` and `create_superuser`.

### 2. Application-Level Foreign Key
```python
# users/models.py
user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    db_constraint=False,   # No DB-level constraint
)
```
The relationship is enforced in Python/Django, not by the database engine.

### 3. Dual Databases + Router
```python
# tradexa_project/routers.py
class ProductsRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'products':
            return 'products_db'
        return 'default'
    # ... write + migrate routing
```

### 4. Authenticated Post Creation
The `create_post` view is decorated with `@login_required`. The `PostCreateForm` exposes only `text` and `image`; `user` is set from `request.user` in the view.

---

## Routes

```
/users/register/           Registration
/users/login/              Login
/users/logout/             Logout
/users/feed/               Post feed (login required)
/users/post/new/           Create post (login required)
/users/post/<pk>/delete/   Delete own post
/users/profile/<username>/ User profile
/users/profile/edit/       Edit own profile
/products/                 Product listing
/products/<pk>/            Product detail
/products/new/             Add product (login required)
/products/<pk>/edit/       Edit product
/products/<pk>/delete/     Delete product
/admin/                    Django admin
```
