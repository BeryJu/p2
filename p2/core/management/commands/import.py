"""p2 Import management command"""
import hashlib
import logging
import os
from glob import glob

from django.core.management.base import BaseCommand

from p2.core.models import Blob, Volume

BUF_SIZE = 65536
LOGGER = logging.getLogger(__name__)

class Command(BaseCommand):
    """Import Images"""

    help = "Import Blobs"

    def add_arguments(self, parser):
        parser.add_argument('import', type=str, nargs='+',
                            help='Path(s) to files which should be imported')
        parser.add_argument('--volume', type=str,
                            help='Name of Volume to import Blobs into.')
        parser.add_argument('--recursive', action='store_true',
                            help='Recursively import (default: import files in folder)')
        parser.add_argument('--duplicate-check', action='store_true',
                            help='Prevent duplicate Blobs by checking SHA512 sums.')

    @staticmethod
    def get_sha512(file_handle):
        """Simple boilerplate to get SHA512 of file"""
        sha512 = hashlib.sha512()
        sha512.update(file_handle.read())
        return sha512.hexdigest()

    def handle_file(self, path, volume, duplicate_check=False, base=None):
        """Handle single file"""
        # Use relative path if entire folder is imported, otherwise root path
        virtual_path = os.path.basename(path)
        if base:
            virtual_path = os.path.relpath(path, base)
        with open(path, 'rb') as _file:
            if duplicate_check:
                file_sha512 = Command.get_sha512(_file)
                matching_files = Blob.objects.filter(attributes__sha512=file_sha512)
                _file.seek(0)
                if matching_files.exists():
                    matching = matching_files.first()
                    LOGGER.warning("File '%s' exists already as %s, skipping.", path, matching.uuid)
                    return
            Blob.objects.create(
                path='/%s' % virtual_path,
                volume=volume,
                payload=_file.read(),
                attributes={
                    'stat:ctime': os.path.getctime(path),
                    'stat:mtime': os.path.getmtime(path)
                })
            LOGGER.info("Imported blob '%s'", path)

    def handle(self, *args, **options):
        volume_name = options.get('volume')
        volume = Volume.objects.filter(name=volume_name).first()
        for path in options.get('import'):
            if os.path.isfile(path):
                self.handle_file(path, volume=volume,
                                 duplicate_check=options.get('duplicate_check'))
            if os.path.isdir(path):
                if options.get('recursive'):
                    for file in glob(path + os.path.sep + '**', recursive=True):
                        if os.path.isdir(file):
                            continue
                        self.handle_file(file, volume=volume,
                                         duplicate_check=options.get('duplicate_check'),
                                         base=path)
        return 0
