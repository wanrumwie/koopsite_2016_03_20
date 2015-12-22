from random import randrange
from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.forms.fields import Field
from koopsite.functions import has_group_member, add_group, remove_group
from .models import UserProfile

EMPTY_FIELD_ERROR = "Це поле обов'язкове:"
INVALID_FIELD_ERROR = "Невірне значення:"
# ця змінна використовується всіма аплікаціями
Field.default_error_messages = {
    'required'  : EMPTY_FIELD_ERROR,
    'invalid'   : INVALID_FIELD_ERROR,
}
'''
ДЛЯ ПЕРЕКЛАДУ:
Field.default_error_messages = {
    'required': ugettext_lazy("This field is mandatory."),
}
'''
# TODO-Запустити переклад verbose_name хоча б для моделі User
# Тимчасове рішення для перекладу назв полів моделі User:
user_verbose_names_uk = {
    'username'      : 'Логін',
    'first_name'    : "Ім'я",
    'last_name'     : "Прізвище",
    'password'      : 'Пароль',
    'email'         : 'e-mail',
    'is_active'     : 'Активний',
    'is_staff'      : 'У штаті',
    'date_joined'   : 'Дата створення',
    'last_login'    : 'Дата попер.входу',
    'groups'        : 'Групи:',
    }


class UserFullForm(forms.ModelForm):
    # Базова Форма для вводу користувача
    # Поля вказані тут для того, щоб описати label і т.д.,
    # оскільки модель User - специфічна і не згадується в models.py
    username = forms.CharField(
                            label='Логін',
                            error_messages={
                                # інші помилки переозначені на поч. цього модуля
                                'unique': "Користувач з таким логіном вже існує."},
                             )
    first_name = forms.CharField(
                            label="Ім'я",
                            required=False,
                             )
    last_name = forms.CharField(
                            label="Прізвище",
                            required=False,
                             )
    password = forms.CharField(
                            label='Пароль',
                            widget=forms.PasswordInput(),
                            )
    email    = forms.CharField(
                            label='e-mail',
                            required=False,
                            )
    is_active   = forms.BooleanField(
                            label='Активний',
                            required=False, # інакше поле не зможе прийняти значення False
                            )
    is_staff    = forms.BooleanField(
                            label='У штаті',
                            required=False, # інакше поле не зможе прийняти значення False
                            )
    date_joined = forms.DateField(
                            widget=forms.DateInput(attrs={"readonly": "readonly"}),
                            label='Дата створення',
                            required=False,
                            )
    last_login  = forms.DateField(
                            widget=forms.DateInput(attrs={"readonly": "readonly"}),
                            label='Дата попер.входу',
                            required=False,
                            )
    groups  = forms.ModelMultipleChoiceField(
                            queryset=Group.objects.all(),
                            label='Групи:',
                            required=False,
                            )

    class Meta:
        model = User
        fields = ('username', 'password',
                  'first_name', 'last_name', 'email',
                  'date_joined', 'last_login',
                  'is_active', 'is_staff',
                  'groups',
                 )


class UserRegistrationForm(UserFullForm):
    # Форма для реєстрації користувача
    # У формі в тегах буде додано назву відповідного класу CSS:
    required_css_class  = 'required'
    error_css_class     = 'error'
    # Декларативно видаляємо деякі успадковані поля:
    date_joined = None
    last_login  = None
    is_active   = None
    is_staff    = None
    groups      = None
    has_perm_member = None

    class Meta:
        model = User
        fields = ('username', 'password',
                  'first_name', 'last_name', 'email')


class UserPersonDataForm(UserRegistrationForm):
    # Коротка Форма для вводу користувача.
    # Декларативно видаляємо деякі успадковані поля:
    username = None
    password = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserPermsFullForm(UserFullForm):
    # Форма для вводу користувача
    # Модифікуємо деякі успадковані поля:
    # username = forms.CharField(
    #                 label='Логін',
    #                 widget=forms.TextInput(attrs={"readonly": "readonly"}),
    #                 )
    # first_name = forms.CharField(
    #                 label="Ім'я",
    #                 widget=forms.TextInput(attrs={"readonly": "readonly"}),
    #                 )
    # last_name =  forms.CharField(
    #                 label="Прізвище",
    #                 widget=forms.TextInput(attrs={"readonly": "readonly"}),
    #                 )
    # Декларативно видаляємо деякі успадковані поля:
    password = None
    email    = None
    # Додаємо поля, яких немає в батьківській формі:

    # Трюк з полями readonly:
    READONLY_FIELDS = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserPermsFullForm, self).__init__(*args, **kwargs)
        for field in self.READONLY_FIELDS:
            self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = (
                  'username',
                  'first_name', 'last_name',
                  'date_joined', 'last_login',
                  'is_active', 'is_staff',
                  'groups',
                )


class UserPermsActivateForm(UserPermsFullForm):
    # Форма для вводу користувача
    # Модифікуємо деякі успадковані поля:
    # Декларативно видаляємо деякі успадковані поля:
    last_login  = None
    is_staff    = None
    groups      = None

    # Додаємо поля, яких немає в моделі:
    has_perm_member = forms.NullBooleanField(
                            label="Доступ члена коопертиву",
                            widget=forms.CheckboxInput(),
                            # initial=get_is_member,
                            required=False,
                            )
    def __init__(self, *args, **kwargs):
        super(UserPermsActivateForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        self.is_member = None
        if instance:
            self.is_member = has_group_member(instance)
            print('instance =', instance)
            print('self.is_member =', self.is_member)
            self.fields['has_perm_member'].initial = self.is_member

    def get_is_member(self):
        return self.is_member

    def save(self, commit=True):
        instance = super(UserPermsActivateForm, self).save(commit=False)
        if self.cleaned_data.get('has_perm_member'):
            add_group(instance, 'members')
        else:
            remove_group(instance, 'members')
        if commit:
            instance.save()
        return instance

    class Meta:
        model = User
        fields = (
                  'username',
                  'first_name', 'last_name',
                  'date_joined',
                  'is_active',
                )


class ProfileFullForm(forms.ModelForm):
    # Повна Форма для вводу профілю - ВСІХ додаткових даних користувача.
    # УВАГА! Використовувати лише для адміністратора!
    is_recognized = forms.NullBooleanField(
                            label="Підтверджений",
                            widget=forms.CheckboxInput(),
                            )

    class Meta:
        model = UserProfile
        fields = ('is_recognized', 'flat', 'picture')


class ProfilePermForm(ProfileFullForm):
    # Декларативно видаляємо деякі успадковані поля:
    picture = None

    # Трюк з полями readonly:
    READONLY_FIELDS = ('flat', )

    def __init__(self, *args, **kwargs):
        super(ProfilePermForm, self).__init__(*args, **kwargs)
        for field in self.READONLY_FIELDS:
            self.fields[field].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = UserProfile
        fields = ('is_recognized', 'flat')


class ProfilePersonDataForm(ProfileFullForm):
    # Декларативно видаляємо деякі успадковані поля:
    is_recognized = None

    class Meta:
        model = UserProfile
        fields = ('flat', 'picture')


class Human_Check:
    """
    Для перевірки, чи користувач є людиною.
    У простому реченні користувач повинен витерти одне із слів
    (номер слова обирається випадково).
    Перед відкриттям форми створюється примірник цього класу,
    а, отже, і речення-завдання, і потрібна відповідь.
    Речення-завдання task поступає у поле форми
    Метод validator цього класу присвоюється
    параметру validators поля форми.
    При неправильній відповіді у формі з'являється відповідне повідомлення.
    """
    # TODO-зробити, щоб після неправильної відповіді або генерувалося нове речення-завдання, або взагалі виходилося з форми.
    taskPattern = "Видаліть із цієї стрічки %s слово"
    numerals = {
       -1: "останнє",
        0: "перше",
        1: "друге",
        2: "третє",
        3: "четверте",
        4: "п'яте",
        5: "шосте",
    }
    def __init__(self, n=None):
        if n == None:
            self.taskNo = randrange(-1, 6)
        else:
            self.taskNo = n
        self.task = self.taskPattern % self.numerals[self.taskNo]

    def validator(self, answer):
        twords = self.task.split()
        twords.pop(self.taskNo)
        awords = answer.split()
        check = twords == awords
        if not check:
            # print('"%s" is not correct answer' % answer)
            raise ValidationError("Помилка!")
            # return HttpResponseRedirect('/index/')
        else:
            print('HumanCheck Ok')


class ProfileRegistrationForm(ProfileFullForm):
    # Форма для реєстрації користувача
    # Модифікуємо деякі успадковані поля:
    is_recognized = None
    # Декларативно видаляємо деякі успадковані поля:

    # Додаємо поля, яких немає в батьківській формі:
    hc = Human_Check()  # примірник класу перевірки на "людяність"
    human_check = forms.CharField(
                    label='Доведіть, що Ви - людина',
                    initial=hc.task,        # речення-завдання
                    required=False,
                    validators=[hc.validator],
                    )
    class Meta:
        model = UserProfile
        fields = ('flat', 'picture')

