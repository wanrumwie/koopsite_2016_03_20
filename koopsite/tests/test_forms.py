from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from flats.tests.test_base import DummyFlat
from folders.tests.test_base import DummyFolder
from koopsite.forms import UserFullForm, UserRegistrationForm, UserPersonDataForm, UserPermsFullForm, \
    UserPermsActivateForm, ProfileFullForm, ProfilePermForm, ProfilePersonDataForm, Human_Check, ProfileRegistrationForm
from koopsite.functions import has_group
from koopsite.models import UserProfile
from koopsite.tests.test_base import DummyUser


class UserFullFormTest(TestCase):

    def setUp(self):
        self.cls_form = UserFullForm
        self.cls_model = User
        # self.user = DummyUser().create_dummy_user(username='dummy_user')
        self.expected_meta_fields = ('username', 'password',
                  'first_name', 'last_name', 'email',
                  'date_joined', 'last_login',
                  'is_active', 'is_staff',
                  'groups',
                 )
        self.expected_form_fields = ('username', 'password',
                  'first_name', 'last_name', 'email',
                  'date_joined', 'last_login',
                  'is_active', 'is_staff',
                  'groups',
                 )
        self.initial_data = {
            'username': 'dummy_user',
            'password': 'secret',
            }
        self.empty_data = {}.fromkeys(self.expected_meta_fields)

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'declared_fields').keys())
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(sorted(form_fields), sorted(self.expected_form_fields))

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertIn('Логін', form.as_p())
        self.assertIn("Ім&#39;я", form.as_p())
        self.assertIn("Прізвище", form.as_p())
        self.assertIn('Пароль', form.as_p())
        self.assertIn('e-mail', form.as_p())
        self.assertIn('Активний', form.as_p())
        self.assertIn('У штаті', form.as_p())
        self.assertIn('Дата створення', form.as_p())
        self.assertIn('Дата попер.входу', form.as_p())
        self.assertIn('Групи:', form.as_p())

    # def test_form_renders_values(self):
    #     form = self.cls_form(data=self.initial_data)
    #     self.assertIn('option value="1" selected="selected">dummy_root_folder', form.as_p())

    def test_form_validation_for_blank_fields(self):
        form = self.cls_form(data=self.empty_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ["Це поле обов'язкове."])
        self.assertEqual(form.errors['password'], ["Це поле обов'язкове."])

    def test_form_validation_for_duplicate_fields(self):
        DummyUser().create_dummy_user(username='dummy_user')
        # Передаємо у форму неунікальне значення поля:
        data = {'username': "dummy_user"}
        form = self.cls_form(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ["Користувач з таким логіном вже існує."])

    def test_form_save(self):
        # Передаємо у форму значення parent і name:
        data = self.initial_data
        form = self.cls_form(data=data)
        new_record = form.save()
        self.assertEqual(new_record, self.cls_model.objects.last())

class UserRegistrationFormTest(TestCase):

    def setUp(self):
        self.cls_form = UserRegistrationForm
        self.cls_model = User
        self.expected_meta_fields = ('username', 'password',
                  'first_name', 'last_name', 'email',
                 )
        self.expected_form_fields = ('username', 'password',
                  'first_name', 'last_name', 'email',
                 )

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'declared_fields').keys())
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(sorted(form_fields), sorted(self.expected_form_fields))

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertIn('Логін', form.as_p())
        self.assertIn("Ім&#39;я", form.as_p())
        self.assertIn("Прізвище", form.as_p())
        self.assertIn('Пароль', form.as_p())
        self.assertIn('e-mail', form.as_p())
        self.assertNotIn('Активний', form.as_p())
        self.assertNotIn('У штаті', form.as_p())
        self.assertNotIn('Дата створення', form.as_p())
        self.assertNotIn('Дата попер.входу', form.as_p())
        self.assertNotIn('Групи:', form.as_p())


class UserPersonDataFormTest(TestCase):

    def setUp(self):
        self.cls_form = UserPersonDataForm
        self.cls_model = User
        self.expected_meta_fields = (
                  'first_name', 'last_name', 'email',
                 )
        self.expected_form_fields = (
                  'first_name', 'last_name', 'email',
                 )

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'declared_fields').keys())
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(sorted(form_fields), sorted(self.expected_form_fields))

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertNotIn('Логін', form.as_p())
        self.assertIn("Ім&#39;я", form.as_p())
        self.assertIn("Прізвище", form.as_p())
        self.assertNotIn('Пароль', form.as_p())
        self.assertIn('e-mail', form.as_p())
        self.assertNotIn('Активний', form.as_p())
        self.assertNotIn('У штаті', form.as_p())
        self.assertNotIn('Дата створення', form.as_p())
        self.assertNotIn('Дата попер.входу', form.as_p())
        self.assertNotIn('Групи:', form.as_p())


class UserPermsFullFormTest(TestCase):

    def setUp(self):
        self.cls_form = UserPermsFullForm
        self.cls_model = User
        self.expected_meta_fields = (
                  'username',
                  'first_name', 'last_name',
                  'date_joined', 'last_login',
                  'is_active', 'is_staff',
                  'groups',
                 )
        self.expected_form_fields = (
                  'username',
                  'first_name', 'last_name',
                  'date_joined', 'last_login',
                  'is_active', 'is_staff',
                  'groups',
                 )

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'declared_fields').keys())
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.READONLY_FIELDS   , ('username', 'first_name', 'last_name'))
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(sorted(form_fields), sorted(self.expected_form_fields))

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertIn('Логін', form.as_p())
        self.assertIn("Ім&#39;я", form.as_p())
        self.assertIn("Прізвище", form.as_p())
        self.assertNotIn('Пароль', form.as_p())
        self.assertNotIn('e-mail', form.as_p())
        self.assertIn('Активний', form.as_p())
        self.assertIn('У штаті', form.as_p())
        self.assertIn('Дата створення', form.as_p())
        self.assertIn('Дата попер.входу', form.as_p())
        self.assertIn('Групи:', form.as_p())

    def test_init(self):
        form = self.cls_form()
        for field in form.READONLY_FIELDS:
            self.assertTrue(form.fields[field].widget.attrs['readonly'])
            self.assertTrue(form.fields[field].widget.attrs['disabled'])


class UserPermsActivateFormTest(TestCase):

    def setUp(self):
        self.cls_form = UserPermsActivateForm
        self.cls_model = User
        self.expected_meta_fields = (
                  'username',
                  'first_name', 'last_name',
                  'date_joined',
                  'is_active',
                 )
        self.expected_form_fields = (
                  'username',
                  'first_name', 'last_name',
                  'date_joined',
                  'is_active',
                  'has_perm_member',
                 )

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'declared_fields').keys())
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.READONLY_FIELDS   , ('username', 'first_name', 'last_name'))
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(sorted(form_fields), sorted(self.expected_form_fields))

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertIn('Логін', form.as_p())
        self.assertIn("Ім&#39;я", form.as_p())
        self.assertIn("Прізвище", form.as_p())
        self.assertNotIn('Пароль', form.as_p())
        self.assertNotIn('e-mail', form.as_p())
        self.assertIn('Активний', form.as_p())
        self.assertNotIn('У штаті', form.as_p())
        self.assertIn('Дата створення', form.as_p())
        self.assertNotIn('Дата попер.входу', form.as_p())
        self.assertNotIn('Групи:', form.as_p())
        self.assertIn('Доступ члена коопертиву', form.as_p())

    def test_init_and_get_is_member(self):
        form = self.cls_form()
        for field in form.READONLY_FIELDS:
            self.assertTrue(form.fields[field].widget.attrs['readonly'])
            self.assertTrue(form.fields[field].widget.attrs['disabled'])
        # empty form:
        self.assertFalse(form.is_member)
        self.assertFalse(form.fields['has_perm_member'].initial)

        dummy_user = DummyUser().create_dummy_user(username='dummy_user')

        # form with initial data
        initial_data = {
            'username': 'dummy_user',
            }
        form = self.cls_form(data=initial_data)
        self.assertFalse(form.is_member)
        self.assertFalse(form.fields['has_perm_member'].initial)

        # form with initial user instance:

        DummyUser().create_dummy_group(group_name='members')
        DummyUser().add_dummy_group(dummy_user, group_name='members')
        self.assertTrue(has_group(dummy_user, 'members'))
        form = self.cls_form(instance=dummy_user)
        self.assertTrue(form.is_member)
        self.assertEqual(form.fields['has_perm_member'].initial, form.is_member)

    def test_form_save(self):
        dummy_user = DummyUser().create_dummy_user(username='dummy_user')
        DummyUser().create_dummy_group(group_name='members')
        self.assertFalse(has_group(dummy_user, 'members'))

        # Створюємо форму з user + додаткові data
        data = {'username': 'dummy_user', 'has_perm_member': True}
        form = self.cls_form(instance=dummy_user, data=data)
        saved_user = form.save()
        # Чи збережено?
        self.assertEqual(saved_user, User.objects.last())
        # Чи змінилось значення поля?
        self.assertTrue(has_group(dummy_user, 'members'))

        # Створюємо форму з user + додаткові data
        data = {'username': 'dummy_user', 'has_perm_member': False}
        form = self.cls_form(instance=dummy_user, data=data)
        saved_user = form.save()
        # Чи збережено?
        self.assertEqual(saved_user, User.objects.last())
        # Чи змінилось значення поля?
        self.assertFalse(has_group(dummy_user, 'members'))


class ProfileFullFormTest(TestCase):

    def setUp(self):
        self.cls_form = ProfileFullForm
        self.cls_model = UserProfile
        user = DummyUser().create_dummy_user(username='dummy_user')
        flat = DummyFlat().create_dummy_flat(id=1, flat_No='25')
        self.profile = DummyUser().create_dummy_profile(user, flat=flat, is_recognized=True)
        self.expected_meta_fields = ('is_recognized', 'flat', 'picture')
        self.expected_form_fields = ('is_recognized', )
        self.initial_data = {
            'flat': '1',
            }
        self.empty_data = {}.fromkeys(self.expected_meta_fields)

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'declared_fields').keys())
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(sorted(form_fields), sorted(self.expected_form_fields))

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertIn('Підтверджений', form.as_p())
        self.assertIn("Квартира", form.as_p())
        self.assertIn("Аватар", form.as_p())

    def test_form_renders_values(self):
        form = self.cls_form(instance=self.profile)
        self.assertIn('option value="1" selected="selected">25', form.as_p())

    def test_form_save(self):
        form = self.cls_form(instance=self.profile, data=self.initial_data)
        new_record = form.save()
        self.assertEqual(new_record, self.cls_model.objects.last())


class ProfilePermFormTest(TestCase):

    def setUp(self):
        self.cls_form = ProfilePermForm
        self.cls_model = UserProfile
        self.expected_meta_fields = ('is_recognized', 'flat')
        self.expected_form_fields = ('is_recognized', )

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'declared_fields').keys())
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        self.assertEqual(form.READONLY_FIELDS   , ('flat', ))
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(sorted(form_fields), sorted(self.expected_form_fields))

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertIn('Підтверджений', form.as_p())
        self.assertIn("Квартира", form.as_p())
        self.assertNotIn("Аватар", form.as_p())

    def test_init(self):
        form = self.cls_form()
        for field in form.READONLY_FIELDS:
            self.assertTrue(form.fields[field].widget.attrs['readonly'])
            self.assertTrue(form.fields[field].widget.attrs['disabled'])


class ProfilePersonDataFormTest(TestCase):

    def setUp(self):
        self.cls_form = ProfilePersonDataForm
        self.cls_model = UserProfile
        self.expected_meta_fields = ('flat', 'picture')
        self.expected_form_fields = ()

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'declared_fields').keys())
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        # self.assertEqual(form.READONLY_FIELDS   , ('flat', ))
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(sorted(form_fields), sorted(self.expected_form_fields))

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertNotIn('Підтверджений', form.as_p())
        self.assertIn("Квартира", form.as_p())
        self.assertIn("Аватар", form.as_p())


class Human_CheckTest(TestCase):

    def setUp(self):
        self.expected_taskPattern = "Видаліть із цієї стрічки %s слово"
        self.expected_numerals = {
           -1: "останнє",
            0: "перше",
            1: "друге",
            2: "третє",
            3: "четверте",
            4: "п'яте",
            5: "шосте",
        }

    def test_attributes(self):
        self.assertEqual(Human_Check.taskPattern, self.expected_taskPattern)
        self.assertEqual(Human_Check.numerals, self.expected_numerals)

    def test_init(self):
        # Випадкові значення:
        for i in range(100):
            hc = Human_Check()
            self.assertEqual(hc.task, hc.taskPattern % hc.numerals[hc.taskNo])
            self.assertIn(hc.taskNo, list(range(-1, 6)))

        # Фіксовані значення:
        for i in range(-1, 6):
            hc = Human_Check(i)
            self.assertEqual(hc.task, hc.taskPattern % hc.numerals[hc.taskNo])
            self.assertEqual(hc.taskNo, i)

    def test_validator(self):
        # Фіксовані значення:
        # Готуємо правильну відповідь:
        for i in range(-1, 6):
            hc = Human_Check(i)
            twords = hc.task.split()
            twords.pop(hc.taskNo)
            answer = ' '.join(twords)
            hc.validator(answer)    # помилки не повинно бути

        # Різні варіанти неправильної відповіді:
        # без змін:
        for i in range(-1, 6):
            hc = Human_Check(i)
            answer = hc.task
            with self.assertRaises(ValidationError):
                hc.validator(answer)

        # неправильні зміни:
        for i in range(-1, 6):
            hc = Human_Check(i)
            twords = hc.task.split()
            n = i + 1
            if n > 5: n = 0
            twords.pop(n)
            answer = ' '.join(twords)
            with self.assertRaises(ValidationError):
                hc.validator(answer)

        # порожній рядок:
        for i in range(-1, 6):
            hc = Human_Check(i)
            answer = ''
            with self.assertRaises(ValidationError):
                hc.validator(answer)

        # абракадабра:
        for i in range(-1, 6):
            hc = Human_Check(i)
            answer = 'абракадабра'
            with self.assertRaises(ValidationError):
                hc.validator(answer)

#---------------- Кінець коду, охопленого тестуванням ------------------

class ProfileRegistrationFormTest(TestCase):

    def setUp(self):
        self.cls_form = ProfileRegistrationForm
        self.cls_model = UserProfile
        self.expected_meta_fields = ('flat', 'picture')
        self.expected_form_fields = ('human_check',)

    def test_form_attributes(self):
        form = self.cls_form
        form_fields = tuple(getattr(form, 'declared_fields').keys())
        self.assertEqual(form.required_css_class, 'required')
        self.assertEqual(form.error_css_class   , 'error')
        # self.assertEqual(form.READONLY_FIELDS   , ('flat', ))
        self.assertIsInstance(form.hc, Human_Check)
        self.assertEqual(form.Meta.model, self.cls_model)
        self.assertEqual(form.Meta.fields, self.expected_meta_fields)
        self.assertEqual(sorted(form_fields), sorted(self.expected_form_fields))

    def test_form_renders_blank(self):
        form = self.cls_form()
        self.assertNotIn('Підтверджений', form.as_p())
        self.assertIn("Квартира", form.as_p())
        self.assertIn("Аватар", form.as_p())
        self.assertIn("Доведіть, що Ви - людина", form.as_p())

    def test_form_validation_for_blank_fields(self):
        form = self.cls_form(data={'human_check': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['human_check'], ["Це поле обов'язкове."])

    def test_form_validation_for_non_human(self):
        form = self.cls_form(data={'human_check': 'abrakadabra'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['human_check'], ["Помилка!"])



