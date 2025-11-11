from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache
import time

try:
    import requests
except Exception:
    requests = None


def home(request):
    return render(request, 'hotel/home.html')


def rooms(request):
    return render(request, 'hotel/rooms.html')


def facilities(request):
    return render(request, 'hotel/facilities.html')


def reviews(request):
    """
    Render reviews page. If GOOGLE_PLACES_API_KEY and GOOGLE_PLACE_ID are set in Django settings,
    fetch live reviews from Google Places Details API and cache the results for 10 minutes.

    Required settings (optional):
      - GOOGLE_PLACES_API_KEY
      - GOOGLE_PLACE_ID

    If unavailable, the template will fall back to static sample reviews.
    """
    google_data = cache.get('google_reviews_data')

    api_key = getattr(settings, 'GOOGLE_PLACES_API_KEY', None)
    place_id = getattr(settings, 'GOOGLE_PLACE_ID', None)

    if not google_data and api_key and place_id:
        # attempt to fetch from Google Places Details
        try:
            if requests is None:
                # fallback to urllib if requests isn't installed
                import urllib.request, urllib.parse, json
                url = (
                    'https://maps.googleapis.com/maps/api/place/details/json?'
                    + urllib.parse.urlencode({
                        'place_id': place_id,
                        'fields': 'rating,user_ratings_total,reviews',
                        'key': api_key,
                    })
                )
                with urllib.request.urlopen(url, timeout=6) as resp:
                    j = json.loads(resp.read().decode())
            else:
                url = 'https://maps.googleapis.com/maps/api/place/details/json'
                params = {
                    'place_id': place_id,
                    'fields': 'rating,user_ratings_total,reviews',
                    'key': api_key,
                }
                res = requests.get(url, params=params, timeout=6)
                j = res.json()

            if j.get('status') == 'OK':
                result = j.get('result', {})
                rating = result.get('rating')
                total = result.get('user_ratings_total')
                reviews_raw = result.get('reviews', [])
                reviews_list = []
                for r in reviews_raw:
                    # Google returns unix 'time' and sometimes 'relative_time_description'
                    reviews_list.append({
                        'author': r.get('author_name'),
                        'rating': r.get('rating'),
                        'text': r.get('text'),
                        'time': r.get('relative_time_description') or r.get('time'),
                        'profile_photo': r.get('profile_photo_url'),
                    })

                google_data = {
                    'rating': rating,
                    'total': total,
                    'reviews': reviews_list,
                    'fetched_at': int(time.time()),
                }
                # cache for 10 minutes
                cache.set('google_reviews_data', google_data, 60 * 10)
            else:
                google_data = {'error': 'Google API status: ' + str(j.get('status'))}
        except Exception as e:
            google_data = {'error': 'Fetch error: ' + str(e)}

    context = {'google_reviews': google_data}
    return render(request, 'hotel/reviews.html', context)


def contact(request):
    return render(request, 'hotel/contact.html')

