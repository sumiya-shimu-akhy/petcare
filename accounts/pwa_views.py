from django.http import HttpResponse, JsonResponse
from django.templatetags.static import static


def manifest(request):
    data = {
        'name': 'Pet Care Finder',
        'short_name': 'PetCare',
        'description': 'Find and book trusted vets, groomers, pet sitters and trainers.',
        'start_url': '/',
        'scope': '/',
        'display': 'standalone',
        'background_color': '#ffffff',
        'theme_color': '#4f46e5',
        'icons': [
            {'src': static('accounts/icons/icon-192.png'), 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
            {'src': static('accounts/icons/icon-512.png'), 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'},
            {'src': static('accounts/icons/icon-maskable-512.png'), 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
        ],
    }
    return JsonResponse(data, content_type='application/manifest+json')


SERVICE_WORKER = """
self.addEventListener('install', function (event) { self.skipWaiting(); });
self.addEventListener('activate', function (event) { event.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', function (event) {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(function () {
        return new Response(
          '<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1">' +
          '<body style="font-family:sans-serif;text-align:center;padding:2rem">' +
          '<h2>Pet Care Finder</h2><p>You are offline. Please check your internet and try again.</p></body>',
          {headers: {'Content-Type': 'text/html'}});
      })
    );
  }
});
"""


def service_worker(request):
    response = HttpResponse(SERVICE_WORKER, content_type='application/javascript')
    response['Cache-Control'] = 'no-cache'
    return response