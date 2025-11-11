Render / Deployment notes

1) Static files (important)
- For Render, set STATIC_ROOT in your Django settings and ensure collectstatic runs during deployment.
- Example settings:
  STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
  STATIC_URL = '/static/'
- On Render, add a build command that runs `python manage.py collectstatic --noinput`.

2) Tailwind
- Currently using Tailwind CDN (deferred) for quick styling. For production, consider compiling Tailwind locally and serving a bundled CSS file from static files to reduce external dependency and improve performance.

3) SEO files
- robots.txt and sitemap.xml are present at project root and will be served from the app root. Ensure your webserver serves these files at /robots.txt and /sitemap.xml.

4) Google Places
- The reviews view expects GOOGLE_PLACES_API_KEY and GOOGLE_PLACE_ID in Django settings. Add these as environment variables in the Render service.

5) Next steps (recommended)
- Add a dynamic sitemap view if you prefer generated URLs and lastmod timestamps.
- Add HTTPS and canonical host enforcement if you have a primary domain.
- Consider enabling GZIP/Brotli and proper caching headers for static assets.
