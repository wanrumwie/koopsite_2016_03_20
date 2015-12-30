from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from folders.functions import response_for_download, response_for_download_zip, get_folders_tree_HTML, wrap_li, wrap_ul, \
    get_recursive_path, get_parents, get_subfolders, get_subreports, get_full_named_path
from folders.models import Folder
from folders.tests.test_base import DummyFolder
from bs4 import BeautifulSoup


class DifferentFunctionsTest(TestCase):

    def test_get_recursive_path(self):
        root = DummyFolder().create_dummy_root_folder()
        f2 = DummyFolder().create_dummy_folder(parent=root)
        f3 = DummyFolder().create_dummy_folder(parent=f2)
        report = DummyFolder().create_dummy_report(parent=f3)
        expected = '%s\\%s\\%s\\' % (root.id, f2.id, f3.id)
        self.assertEqual(get_recursive_path(report), expected)

    def test_get_parents(self):
        root = DummyFolder().create_dummy_root_folder()
        f2 = DummyFolder().create_dummy_folder(parent=root)
        f3 = DummyFolder().create_dummy_folder(parent=f2)
        r1 = DummyFolder().create_dummy_report(parent=root)
        r2 = DummyFolder().create_dummy_report(parent=f2)
        r3 = DummyFolder().create_dummy_report(parent=f3)
        self.assertEqual(get_parents(root), [])
        self.assertEqual(get_parents(f2), [root])
        self.assertEqual(get_parents(f3), [root, f2])
        self.assertEqual(get_parents(r1), [root])
        self.assertEqual(get_parents(r2), [root, f2])
        self.assertEqual(get_parents(r3), [root, f2, f3])

    def test_get_full_named_path(self):
        root = DummyFolder().create_dummy_root_folder()
        f2 = DummyFolder().create_dummy_folder(parent=root)
        f3 = DummyFolder().create_dummy_folder(parent=f2)
        r0 = DummyFolder().create_dummy_report(parent=root)
        r1 = DummyFolder().create_dummy_report(parent=root, filename="r1")
        r2 = DummyFolder().create_dummy_report(parent=f2, filename="r2")
        r3 = DummyFolder().create_dummy_report(parent=f3, filename="r3")
        self.assertEqual(get_full_named_path(root), "dummy_root_folder")
        self.assertEqual(get_full_named_path(f2), "dummy_root_folder/dummy_folder")
        self.assertEqual(get_full_named_path(f3), "dummy_root_folder/dummy_folder/dummy_folder")
        self.assertEqual(get_full_named_path(r0), "dummy_root_folder/--no-name--")
        self.assertEqual(get_full_named_path(r1), "dummy_root_folder/r1")
        self.assertEqual(get_full_named_path(r2), "dummy_root_folder/dummy_folder/r2")
        self.assertEqual(get_full_named_path(r3), "dummy_root_folder/dummy_folder/dummy_folder/r3")

    def test_get_subfolders(self):
        root = DummyFolder().create_dummy_root_folder()
        f2 = DummyFolder().create_dummy_folder(parent=root)
        f3 = DummyFolder().create_dummy_folder(parent=f2)
        f4 = DummyFolder().create_dummy_folder(parent=f2, name='f4')
        self.assertEqual(list(get_subfolders(root)), [f2])
        self.assertEqual(list(get_subfolders(f2)), [f3, f4])
        self.assertEqual(list(get_subfolders(f3)), [])

    def test_get_subreports(self):
        root = DummyFolder().create_dummy_root_folder()
        f2 = DummyFolder().create_dummy_folder(parent=root)
        f3 = DummyFolder().create_dummy_folder(parent=f2)
        r2 = DummyFolder().create_dummy_report(parent=f2)
        r3 = DummyFolder().create_dummy_report(parent=f3)
        r4 = DummyFolder().create_dummy_report(parent=f3)
        self.assertEqual(list(get_subreports(root)), [])
        self.assertEqual(list(get_subreports(f2)), [r2])
        self.assertEqual(list(get_subreports(f3)), [r3, r4])


class Response_for_download_Test(TestCase):

    def setUp(self):
        self.root = DummyFolder().create_dummy_root_folder()
        self.file = SimpleUploadedFile("file.txt", b"file_content")
        self.report = DummyFolder().create_dummy_report(self.root, file=self.file)

    def tearDown(self):
        self.report.file.delete()

    # response_for_download:

    def test_response_for_download_gives_error_if_no_file(self):
        rep0 = DummyFolder().create_dummy_report(parent=self.root)
        with self.assertRaises(AttributeError):
            response_for_download(rep0)

    def test_response_for_download_gives_proper_value(self):
        fn = '; filename="%s"' % self.report.filename
        md = '; modification-date="%s"' % self.report.uploaded_on
        expected_content_disposition = 'attachment' + fn + md

        resp = response_for_download(self.report)
        self.assertEqual(resp.get('Content-Disposition'), expected_content_disposition)
        self.assertEqual(resp.get('Content-Length'), '12')
        self.assertEqual(resp.get('Content-Type'), 'text/plain')
        self.assertEqual(resp.content, b'file_content')

    # response_for_download_zip:

    def test_response_for_download_zip_gives_error_if_no_file(self):
        DummyFolder().create_dummy_report(parent=self.root)
        with self.assertRaises(ValueError):
            response_for_download_zip(self.root)

    def test_response_for_download_zip_gives_proper_value(self):
        fn = '; filename="%s.zip"' % self.root.name
        expected_content_disposition = 'attachment' + fn

        resp, zipFilename, msg = response_for_download_zip(self.root)

        self.assertEqual(zipFilename, 'dummy_root_folder.zip')
        self.assertEqual(msg, "")
        self.assertEqual(resp.get('Content-Disposition'), expected_content_disposition)
        self.assertEqual(resp.get('Content-Length'), '162')
        self.assertEqual(resp.get('Content-Type'), 'application/zip')
        # TODO-перевірити response.content для zip
        # self.assertEqual(resp.content, b'file_content')

    def test_response_for_download_zip_gives_proper_value_2(self):
        file2 = SimpleUploadedFile("file2.txt", b"file_content")
        report2 = DummyFolder().create_dummy_report(self.root, file=file2)

        fn = '; filename="%s.zip"' % self.root.name
        expected_content_disposition = 'attachment' + fn

        resp, zipFilename, msg = response_for_download_zip(self.root)

        self.assertEqual(zipFilename, 'dummy_root_folder.zip')
        self.assertEqual(msg, "")
        self.assertEqual(resp.get('Content-Disposition'), expected_content_disposition)
        self.assertEqual(resp.get('Content-Length'), '304')
        self.assertEqual(resp.get('Content-Type'), 'application/zip')
        # self.assertEqual(resp.content, b'file_content')

        report2.file.delete()


    def test_response_for_download_zip_gives_proper_value_3(self):
        file2 = SimpleUploadedFile("file2.txt", b"file_content")
        report2 = DummyFolder().create_dummy_report(self.root, file=file2)

        fn = '; filename="%s.zip"' % self.root.name
        expected_content_disposition = 'attachment' + fn

        resp, zipFilename, msg = response_for_download_zip(self.root, 15)

        self.assertEqual(zipFilename, 'dummy_root_folder.zip')
        self.assertEqual(msg, 'Завеликий zip. Решту файлів відкинуто')
        self.assertEqual(resp.get('Content-Disposition'), expected_content_disposition)
        self.assertEqual(resp.get('Content-Length'), '162')
        self.assertEqual(resp.get('Content-Type'), 'application/zip')
        # self.assertEqual(resp.content, b'file_content')

        report2.file.delete()


class Get_folders_tree_HTML_Test(TestCase):

    def test_wrap_li(self):
        self.root = DummyFolder().create_dummy_root_folder()
        li = wrap_li(self.root, tab='')
        soup = BeautifulSoup(li, 'html.parser')
        self.assertEqual(soup.li['id'], "1")
        self.assertEqual(soup.li.string.strip(), "dummy_root_folder")

    def test_wrap_ul(self):
        self.root = DummyFolder().create_dummy_root_folder()
        qs = Folder.objects.all()
        ul = wrap_ul(qs, tab='')
        soup = BeautifulSoup(ul, 'html.parser')
        self.assertEqual(soup.li['id'], "1")
        self.assertEqual(soup.li.string.strip(), "dummy_root_folder")

    def test_get_folders_tree_HTML(self):
        expected ='''<ul>
<li id="1">dummy_folder_0
<ul>
<li id="2">dummy_folder_0_0_0
<ul>
<li id="3">dummy_folder_0_0_0_1_0
</li>
<li id="4">dummy_folder_0_0_0_1_1
</li>
</ul>
</li>
<li id="5">dummy_folder_0_0_1
<ul>
<li id="6">dummy_folder_0_0_1_1_0
</li>
<li id="7">dummy_folder_0_0_1_1_1
</li>
</ul>
</li>
</ul>
</li>
</ul>
'''
        DummyFolder().create_dummy_catalogue()
        html = get_folders_tree_HTML(tab='')
        self.assertEqual(html, expected)
        # print(html)
        # print(html.strip())
        # soup = BeautifulSoup(html, 'html.parser')
        # print(soup.li['id'])
        # print(soup.li.text)
        # print(soup.prettify())





