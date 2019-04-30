"""p2 local storage tests"""
from shutil import rmtree

from django.test import TestCase

from p2.core.models import Blob, Storage, Volume
from p2.lib.reflection import class_to_path
from p2.storage.local.constants import TAG_ROOT_PATH
from p2.storage.local.controller import LocalStorageController


class LocalFileStorageTests(TestCase):
    """Test LocalFileStorage"""

    def setUp(self):
        self.storage_path = './storage/local-unittest/'
        self.storage = Storage.objects.create(
            name='local-storage-1',
            controller_path=class_to_path(LocalStorageController),
            tags={
                TAG_ROOT_PATH: self.storage_path
            })
        self.volume = Volume.objects.create(
            name='local-volume-1',
            storage=self.storage)

    def tearDown(self):
        rmtree(self.storage_path)

    def test_simple_create_retrieve(self):
        """Test simple creation of blob and retrival of data"""
        test_content = b'test'
        Blob.objects.create(
            path='/test1',
            payload=test_content,
            volume=self.volume)
        new_blob = Blob.objects.filter(path='/test1').first()
        self.assertEqual(new_blob.payload, test_content)

    def test_update(self):
        """Test Update of blob"""
        test_content = b'test'
        updated_content = b'test2'
        Blob.objects.create(
            path='/test1',
            payload=test_content,
            volume=self.volume)
        new_blob = Blob.objects.filter(path='/test1').first()
        self.assertEqual(new_blob.payload, test_content)
        new_blob.payload = updated_content
        new_blob.save()
        self.assertEqual(Blob.objects.filter(path='/test1').first().payload, updated_content)

    def test_delete(self):
        """Test deletion of blob"""
        test_content = b'test'
        Blob.objects.create(
            path='/test1',
            payload=test_content,
            volume=self.volume)
        Blob.objects.filter(path='/test1').delete()
