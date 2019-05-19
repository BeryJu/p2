"""Test image component"""
import os
import pathlib

from django.test import TestCase

from p2.components.image.constants import (EXIF_MODEL, EXIF_SOFTWARE,
                                           TAG_IMAGE_EXIF_TAGS)
from p2.components.image.controller import ImageController
from p2.core.models import Blob, Component, Volume
from p2.core.tests.utils import get_test_storage
from p2.lib.reflection import class_to_path


class ImageComponentTests(TestCase):
    """Test Image EXIF extraction. Example file by
    https://github.com/ianare/exif-samples/blob/master/jpg/Canon_DIGITAL_IXUS_400.jpg"""

    def setUp(self):
        self.storage = get_test_storage()
        self.volume = Volume.objects.create(
            name='test-volume',
            storage=self.storage)
        self.image_component = Component.objects.create(
            volume=self.volume,
            controller_path=class_to_path(ImageController),
            tags={
                TAG_IMAGE_EXIF_TAGS: [EXIF_MODEL]
            })

    def test_extract_exif(self):
        """Test EXIF extraction"""
        path = pathlib.Path(__file__).parent / 'Canon_DIGITAL_IXUS_400.jpg'
        with open(path, 'rb') as _example:
            blob = Blob(
                path='/test-image',
                volume=self.volume,
                attributes={
                    'blob.p2.io/exif/%s' % EXIF_MODEL: 'invalid model'
                })
            blob.write(_example.read())
            blob.save()
        blob.refresh_from_db()
        self.assertEqual(blob.attributes['blob.p2.io/exif/%s' % EXIF_MODEL],
                         'Canon DIGITAL IXUS 400')
        # Make sure we've only added the specified field
        self.assertNotIn('blob.p2.io/exif/%s' % EXIF_SOFTWARE, blob.attributes)

    def test_non_image(self):
        """Test non-image file"""
        blob = Blob.objects.create(
            path='/test-non-image.png',
            volume=self.volume)
        blob.write(os.urandom(2048))
        blob.save()
        blob.refresh_from_db()
        self.assertNotIn('blob.p2.io/exif/%s' % EXIF_MODEL, blob.attributes)
