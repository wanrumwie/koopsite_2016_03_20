from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from folders.models import Folder, Report
from folders.tests.test_base import DummyData


class Response_for_download_Test(TestCase):

    def setUp(self):
        self.root = DummyData().create_dummy_root_folder()
        self.folder = DummyData().create_dummy_folder(parent=self.root)
        self.report = DummyData().create_dummy_report(parent=self.folder)

