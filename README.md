# Anicare

Anicare is a Django web app that combines an **animal helpline** with a **pet-care storefront**. Citizens can report injured or stray animals with a photo and their GPS location; the report is stored and emailed to NGO volunteers with a Google Maps link. Alongside this, the site offers a pet-food shop and pet-care services pages.

## Features

- **Animal report form** – name, phone, description, photo upload, animal type (pet / stray) and priority (emergency / urgent / not urgent).
- **Automatic geolocation** – browser Geolocation API fills latitude/longitude on page load.
- **Instant NGO alerts** – each submission triggers an email (Gmail SMTP) with all report details and a `maps.google.com` link.
- **Admin dashboard** – reports are registered in Django admin (`list_display`: name, phone, location, type, priority, coordinates).
- **User accounts** – register / login / logout via Django's auth system; landing page greets the logged-in user.
- **Pet shop** – e-commerce landing page with categories, brands, and product cards.
- **Services page** – health care packages, doctor assistance, pet events, insurance and funerals.
- **Experimental ML script** – `send/ia3.py` is a scikit-learn (RandomForest) image-classifier scaffold; see [Notes](#notes).

## Tech Stack

| Layer     | Technology                                            |
| --------- | ----------------------------------------------------- |
| Backend   | Python, Django 5.0                                    |
| Database  | MySQL                                                 |
| Frontend  | Django templates, HTML/CSS/JS, Ionicons, Google Fonts |
| Email     | Django SMTP backend (Gmail)                           |
| ML (WIP)  | scikit-learn, NumPy, joblib                           |

## Project Structure

```
Anicare/
├── manage.py
├── notification/          # Django project (settings, root URLs, WSGI/ASGI)
├── send/                  # Main app
│   ├── models.py          # AnimalReport, UserSubmission, UploadFile
│   ├── views.py           # Pages, auth, report submission + email
│   ├── forms.py           # AnimalReportForm (ModelForm)
│   ├── urls.py
│   ├── admin.py
│   ├── ia3.py             # Image-classifier prototype
│   └── migrations/
├── templates/             # LandingPage, LoginPage, NGO-Form, EcommercePage, Services, admin, ...
├── static/                # CSS/JS and images (shop + landing)
├── media/                 # User-uploaded photos (created at runtime)
└── assests/               # collectstatic output (STATIC_ROOT)
```

## Routes

| URL                   | View                | Description                      |
| --------------------- | ------------------- | -------------------------------- |
| `/`                   | `landing_page`      | Home page                        |
| `/Login/`             | `UserLogin`         | Login                            |
| `/UserRegister/`      | `UserRegister`      | Sign up                          |
| `/NgoLink/`           | `NgoLink`           | Animal report form               |
| `/SubmitNgoForm/`     | `SubmitNgoForm`     | Form POST endpoint (JSON + email) |
| `/LoadEcommerce/`     | `LoadEcommerce`     | Pet shop                         |
| `/redirectToServices/`| `redirectToServices`| Services page                    |
| `/admin/`             | Django admin        | View and manage animal reports   |

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL 8+ running locally
- A Gmail account with an [App Password](https://support.google.com/accounts/answer/185833) for sending alerts

### Setup

```bash
# 1. Clone and enter the project
git clone <repo-url>
cd Anicare

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install django mysqlclient pillow
pip install scikit-learn numpy joblib   # only needed for send/ia3.py

# 4. Create the database
mysql -u root -p -e "CREATE DATABASE anicarengo CHARACTER SET utf8mb4;"

# 5. Configure settings (see below), then migrate
python manage.py migrate
python manage.py createsuperuser

# 6. Run
python manage.py runserver
```

Open http://127.0.0.1:8000/.

### Configuration

Edit `notification/settings.py` (preferably via environment variables rather than hard-coding):

| Setting                                  | Purpose                              |
| ---------------------------------------- | ------------------------------------ |
| `SECRET_KEY`                             | Django secret key                    |
| `DATABASES['default']` (NAME/USER/PASSWORD) | MySQL connection                  |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD`| Gmail address and app password       |
| `ALLOWED_HOSTS`, `DEBUG`                 | Set appropriately for production     |

The NGO recipient list and sender address are defined in `send/views.py` (`SubmitNgoForm`).

## Data Model

**AnimalReport**: `name`, `phone`, `location`, `description`, `photo`, `animal_type` (`pet`/`stray`), `priority` (`emergency`/`urgent`/`not_urgent`), `latitude`, `longitude`.

## Notes

- `send/ia3.py` is a prototype: `preprocess_image` currently returns random data rather than reading the image, so predictions are not meaningful. It is not wired into any view.
- Move all secrets (DB password, email app password, `SECRET_KEY`) out of source control and into environment variables before deploying.

## Roadmap

- Wire a real image-classification step into the report flow (animal type / injury triage).
- Surface reports on a map in the admin dashboard.
- Replace hard-coded NGO recipients with a configurable model.
- Add tests (`send/tests.py` is currently empty) and a `requirements.txt`.

## License

Add a license of your choice (e.g. MIT).
