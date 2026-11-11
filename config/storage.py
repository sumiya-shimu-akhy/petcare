import json
import os
import urllib.error
import urllib.request
import uuid

from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class CloudinaryStorage(Storage):
    """Saves uploaded images on Cloudinary using an unsigned upload preset."""

    def exists(self, name):
        return False

    def _save(self, name, content):
        content.seek(0)
        data = content.read()
        filename = os.path.basename(name).replace('"', '') or 'upload.jpg'
        boundary = uuid.uuid4().hex
        body = b''.join([
            ('--%s\r\nContent-Disposition: form-data; name="upload_preset"\r\n\r\n%s\r\n'
             % (boundary, settings.CLOUDINARY_UPLOAD_PRESET)).encode(),
            ('--%s\r\nContent-Disposition: form-data; name="file"; filename="%s"\r\n'
             'Content-Type: application/octet-stream\r\n\r\n' % (boundary, filename)).encode(),
            data,
            ('\r\n--%s--\r\n' % boundary).encode(),
        ])
        req = urllib.request.Request(
            'https://api.cloudinary.com/v1_1/%s/image/upload' % settings.CLOUDINARY_CLOUD_NAME,
            data=body, method='POST',
            headers={'Content-Type': 'multipart/form-data; boundary=' + boundary})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            detail = e.read().decode('utf-8', 'ignore')[:300]
            raise OSError('Cloudinary upload failed (%s): %s' % (e.code, detail))
        except Exception as e:
            raise OSError('Cloudinary upload failed: %s' % e)
        return '%s.%s' % (result['public_id'], result['format'])

    def url(self, name):
        if name.startswith('provider_photos/'):
            # older photos that were saved on this computer
            return settings.MEDIA_URL + name
        return 'https://res.cloudinary.com/%s/image/upload/%s' % (settings.CLOUDINARY_CLOUD_NAME, name)

    def delete(self, name):
        pass

    def _open(self, name, mode='rb'):
        raise NotImplementedError('Files are stored on Cloudinary.')