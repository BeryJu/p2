import hashlib

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

UPLOAD_TYPES = (
    (0, 'Picture'),
)

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

def save_from_post(content):
    """
    Takes a file from post, calculates sha512, saves it to media dir and returns path
    """
    sha512 = hashlib.sha512()
    sha512.update(content)
    hash = sha512.hexdigest()
    filename = '%s/%s' % (settings.MEDIA_ROOT, hash)
    with open(filename, 'wb') as out_file:
        out_file.write(content)
    return filename

class Upload(models.Model):
    file = models.FileField(max_length=512)
    type = models.IntegerField(choices=UPLOAD_TYPES)
    user = models.ForeignKey(User, default=1)
    md5 = models.CharField(max_length=32, blank=True)
    sha256 = models.CharField(max_length=64, blank=True)
    sha512 = models.CharField(max_length=128, blank=True)

    def update_hashes(self):
        """
        Update hash properties
        """
        md5 = hashlib.md5()
        sha256 = hashlib.sha256()
        sha512 = hashlib.sha512()

        with open(self.file.path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
                sha256.update(data)
                sha512.update(data)
        self.md5 = md5.hexdigest()
        self.sha256 = sha256.hexdigest()
        self.sha512 = sha512.hexdigest()

    def save(self, *args, **kwargs):
        self.update_hashes()
        return super(Upload, self).save(*args, **kwargs)

    @property
    def get_initial_view(self):
        """
        Returns the initial view
        """
        return UploadView.objects.filter(upload=self).earliest()

    @property
    def filename(self):
        """
        Return a filename
        """
        return self.sha512

    def __str__(self):
        return self.sha512

class UploadView(models.Model):
    upload = models.ForeignKey(Upload)
    viewee = models.ForeignKey(User, blank=True, default=1)
    viewee_ip = models.GenericIPAddressField(blank=True, null=True)
    viewee_dns = models.TextField(blank=True)
    viewee_date = models.DateTimeField(auto_now_add=True)
    viewee_user_agent = models.TextField(blank=True)
