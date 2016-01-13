import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
from django.test import TestCase
from koopsite.models import UserProfile
from koopsite.tests.test_base import DummyUser


class UserProfileModelTest(TestCase):

    def test_Meta(self):
        self.assertEqual(UserProfile._meta.verbose_name, ('профіль користувача'))
        self.assertEqual(UserProfile._meta.verbose_name_plural, ('профілі користувачів'))
        self.assertEqual(UserProfile._meta.permissions, (
                        ('activate_account', 'Can activate/deactivate account'),
                        ))

    def test_empty_user_gives_error(self):
        p = UserProfile()
        with self.assertRaises(IntegrityError):
            p.save()

    def test_saving_and_retrieving_files(self):
        user = DummyUser().create_dummy_user()
        file = SimpleUploadedFile("file.txt", b"file_content")
        expected = file.read()
        DummyUser().create_dummy_profile(user, picture=file)
        saved_profile = UserProfile.objects.first()
        # Вмісти збереженого файда і первинного співпадають?
        self.assertEqual(saved_profile.picture.read(), expected)
        # Чи правильний фактичний шлях до файла
        basename = os.path.basename(saved_profile.picture.path)
        self.assertEqual(basename, "1.jpg")
        # Видляємо з диска (бо файл по-чесному записався в /media/profile_images/1.jpg)
        saved_profile.picture.delete()





