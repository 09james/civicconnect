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
PNG, and WebP.

### Render deployment preparation

Production settings are read from environment variables. Local development
continues to use SQLite and `DEBUG=True` by default. In production, the app
requires a secret key and PostgreSQL URL instead of silently falling back to
the development key or local SQLite.

1. Push these changes to the `main` branch of your GitHub repository.
2. On Render, create a PostgreSQL database and a Web Service connected to that
   repository.
3. Set the service's **Build Command** to:

   ```text
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```

4. Set its **Pre-Deploy Command** to:

   ```text
   python manage.py migrate
   ```

   If the service plan does not provide a Pre-Deploy Command, run migrations
   from the Render Shell after deployment and before using the app.

5. Set its **Start Command** to:

   ```text
   gunicorn service_portal.wsgi:application
   ```

6. Add these environment variables to the Render web service:

   | Name | Value |
   | --- | --- |
   | `DJANGO_DEBUG` | `false` |
   | `DJANGO_SECRET_KEY` | Generate a long, random secret; keep it out of GitHub |
   | `DJANGO_ALLOWED_HOSTS` | Your Render hostname, e.g. `civicconnect.onrender.com` |
   | `DATABASE_URL` | The database's **internal** connection URL from Render |
   | `MEDIA_ROOT` | `/var/data/media` if using the persistent disk described below |

   `RENDER_EXTERNAL_HOSTNAME` is also recognized automatically for Django's
   allowed hosts and CSRF trusted origins. If using a custom domain, add it to
   `DJANGO_ALLOWED_HOSTS` and add its HTTPS origin to
   `DJANGO_CSRF_TRUSTED_ORIGINS` (comma-separated if there is more than one).
   Do not commit production environment values to the repository.

7. After the first successful deploy and database migration, open the Render
   Shell and run `python manage.py createsuperuser`. Your admin account can
   then sign in at `/accounts/login/`; Django admin is at `/django-admin/`.

#### Persistent image uploads

The uploaded images use filesystem storage. Cloud hosts may discard files
written to the app's ordinary filesystem when instances restart or redeploy.
For Render, attach a persistent disk to the web service, mount it at
`/var/data`, and set `MEDIA_ROOT=/var/data/media`. Persistent disks are a
paid-plan feature and generally limit scaling to one service instance. For
multi-instance deployments, use object storage instead. Keep user-uploaded
media on persistent storage; WhiteNoise is configured for static assets, not
citizen uploads.

## Screenshots

Capture the landing page, citizen request list, and administrator dashboard
after running the project. Place the resulting images in `docs/screenshots/`
and embed them here, for example:

```markdown
![Landing page](docs/screenshots/home.png)
![Citizen requests](docs/screenshots/my-requests.png)
![Admin dashboard](docs/screenshots/admin-dashboard.png)
```
