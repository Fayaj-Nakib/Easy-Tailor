## EasyTailor

Simple tailor shop management app built with Django. It supports customer and tailor roles, a service catalog, order placement with measurements, and payments. This repo is ready for local development and can be deployed to services like Render/Railway/Heroku.

### Features
- **Authentication**: Register, login, logout, profile edit using a custom `CustomUser` model.
- **Roles**: `customer` and `tailor` with role-based access.
- **Service catalog**: Tailors can add and view `TailorService` items.
- **Orders**: Customers place orders, choose service type, quantity, delivery speed, and provide measurements (regular or custom).
- **Order management (tailor)**: Confirm, deny, cancel, toggle payment to paid, and apply discounts.
- **Payments**: Create a payment for an order; view your payments.

### Tech stack
- Django 4.2
- SQLite by default (PostgreSQL via `DATABASE_URL` supported)
- Crispy Forms (Bootstrap 4 pack)
- WhiteNoise for static files in production
- Gunicorn for production WSGI

### Project structure
```
easytailor/                  # Django project settings and root URLs
  templates/                 # Base and home templates
users/                       # Auth, custom user model, forms, views, seed command
services/                    # Tailor services CRUD (basic)
orders/                      # Orders and order items
payments/                    # Payments
manage.py                    # Django management entrypoint
requirements.txt             # Python dependencies
```

### Getting started (local)
1) Clone and enter the project directory:
```bash
git clone <your-fork-or-origin> easytailor
cd easytailor
```

2) Create a virtual environment and install dependencies:
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3) Apply migrations and create a superuser (optional):
```bash
python manage.py migrate
python manage.py createsuperuser  # optional
```

4) Seed demo data (recommended):
```bash
python manage.py seed
```

This creates two users you can use to try the app:
- Tailor: `tailor1` / `tailor123`
- Customer: `customer1` / `customer123`

5) Run the development server:
```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

### App URLs
- Home: `/` (name: `home`)
- Admin: `/admin/`
- Users: `/users/`
  - Register: `/users/register/`
  - Login: `/users/login/`
  - Profile: `/users/profile/`
  - Logout: `/users/logout/`
- Services (tailor-only): `/services/`
  - List: `/services/`
  - Add: `/services/add/`
  - Detail: `/services/<id>/`
- Orders:
  - List: `/orders/` (customers see their orders; tailors see all)
  - Create: `/orders/add/` (customers only)
  - Detail: `/orders/<id>/`
- Payments:
  - List: `/payments/`
  - Create: `/payments/add/`

### Roles and behavior
- After login, users land on `home`.
- `customer` can place orders and view/pay their orders.
- `tailor` sees all orders and can confirm/deny/cancel, toggle payment to Paid, and apply discounts.
- Service catalog management is restricted to the tailor role.

### Configuration
Key settings live in `easytailor/settings.py`.
- `AUTH_USER_MODEL = 'users.CustomUser'`
- Templates are loaded from `easytailor/templates` and app templates.
- SQLite is default. To use PostgreSQL, set `DATABASE_URL` (e.g. `postgres://...`) and it will override the default via `dj-database-url`.
- Static files served with WhiteNoise in production. Run `python manage.py collectstatic` on deploy.

Environment variables (optional):
- `DATABASE_URL`: PostgreSQL/other DB URL. If not set, falls back to SQLite (`db.sqlite3`).

### Running tests
No dedicated tests are included by default in this snapshot. You can add Django tests under each app’s `tests.py` and run:
```bash
python manage.py test
```

### Deployment notes
- Install deps from `requirements.txt` and set `DATABASE_URL` if using PostgreSQL.
- Ensure `DEBUG=False` and set `ALLOWED_HOSTS` appropriately.
- Collect static files:
```bash
python manage.py collectstatic --noinput
```
- Start with Gunicorn (Linux):
```bash
gunicorn easytailor.wsgi:application --bind 0.0.0.0:$PORT
```

### Landing Page

image.png



