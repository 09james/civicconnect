# CivicConnect — Public Service Request System

A small Django portal for reporting and tracking local public-service issues.
Citizens can submit requests, while administrators review requests, update
statuses, and monitor service activity.

## Features

- Custom user model with Citizen and Admin roles.
- Citizen registration, login, and logout.
- Service request submission with category, location, description, and optional
  image upload.
- Citizen request history is scoped to the signed-in citizen.
- Role-protected administrator dashboard with search and status/category filters.
- Pending → In Progress → Resolved workflow with created, updated, and resolved
  timestamps.
- Open/resolved totals and request counts for each category.
- Responsive Bootstrap 5 templates and Django flash messages.
- Database migration seeds Street lighting, Water supply, and Garbage collection.

## Requirements

- Python 3.10+
- pip

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser. The account created with
`createsuperuser` is assigned the Admin role automatically. Use
`/django-admin/` for Django's built-in administration interface.

## Tests

```powershell
python manage.py test
```

## Image uploads and deployment

Development media is served from `MEDIA_ROOT` (`media/`) at `MEDIA_URL`
(`/media/`). Images are limited to 5 MB and allowed extensions are JPG, JPEG,
PNG, and WebP. In production, set a private `SECRET_KEY`, configure
`DEBUG=False` and `ALLOWED_HOSTS`, and serve uploaded media through a suitable
web server or object storage rather than Django's development media handler.

## Screenshots

Capture the landing page, citizen request list, and administrator dashboard
after running the project. Place the resulting images in `docs/screenshots/`
and embed them here, for example:

```markdown
![Landing page](docs/screenshots/home.png)
![Citizen requests](docs/screenshots/my-requests.png)
![Admin dashboard](docs/screenshots/admin-dashboard.png)
```
