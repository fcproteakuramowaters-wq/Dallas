Render / Deployment notes

## Environment Variables

Set these environment variables in your Render service dashboard:

- **DEBUG**: Set to `False` (do NOT use True in production)
- **SECRET_KEY**: A strong random secret key (use Django's `get_random_secret_key()` or a UUID)
- **ALLOWED_HOSTS**: Comma-separated list of allowed hosts (e.g., `dallas-owo3.onrender.com,www.example.com`)
- **GOOGLE_PLACES_API_KEY**: Your Google Places API key (for reviews feature)
- **GOOGLE_PLACE_ID**: Your Google Place ID (for reviews feature)
- **DATABASE_URL**: If using a hosted database (PostGreSQL on Render, etc.)

Example setup in Render dashboard:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=dallas-owo3.onrender.com
GOOGLE_PLACES_API_KEY=AIza...
GOOGLE_PLACE_ID=ChIJ...
```

## Build Command

In your Render service, set the build command to:

```bash
bash ./build.sh
```

This script will:
1. Install Python dependencies from requirements.txt
2. Run `collectstatic` to gather static files
3. Run migrations (if DATABASE_URL is set)

## Start Command

Use:

```bash
gunicorn dallas.wsgi
```

Or if running on a custom port (Render uses 10000 by default):

```bash
gunicorn -b 0.0.0.0:10000 dallas.wsgi
```

## Static Files

- WhiteNoise middleware is configured to serve static files efficiently.
- `collectstatic` runs during the build process and places files in `staticfiles/`.
- No additional static file hosting required.

## Security Settings

When DEBUG=False in production:
- SECURE_SSL_REDIRECT is enabled (forces HTTPS)
- SESSION_COOKIE_SECURE is enabled
- CSRF_COOKIE_SECURE is enabled
- HSTS is enabled with a 1-year max-age

## Key Points

1. **ALLOWED_HOSTS**: Must include your Render domain (e.g., `dallas-owo3.onrender.com`). Do NOT include `https://` prefix.
2. **Static files**: The build script collects static files automatically. No manual action needed.
3. **Migrations**: If using a database, ensure migrations run during build or via Render's pre-deploy hooks.
4. **Secrets**: Store sensitive keys (SECRET_KEY, API keys) as environment variables in Render, never in git.

## Local Testing

To test locally with production settings:

```bash
DEBUG=False SECRET_KEY=test-secret ALLOWED_HOSTS=localhost,127.0.0.1 python manage.py runserver
```

Or copy `.env.example` to `.env` and fill in values for local development.

## Troubleshooting

- **DisallowedHost error**: Ensure ALLOWED_HOSTS includes your Render domain without `https://` prefix.
- **Static files not loading**: Verify `STATIC_ROOT` is set and `collectstatic` ran during build.
- **500 Internal Server Error**: Check Render logs for specific errors. Ensure `DEBUG=False` doesn't hide errors—check logs.
