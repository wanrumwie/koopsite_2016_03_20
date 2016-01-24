from django import forms
from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView, MultipleObjectMixin
from koopsite.decorators import author_or_permission_required
from koopsite.forms import UserPermsFullForm, ProfileRegistrationForm, \
                    UserPermsActivateForm, ProfilePersonDataForm, \
                    user_verbose_names_uk, ProfilePermForm, \
                    UserRegistrationForm, UserPersonDataForm
from koopsite.functions import AllFieldsMixin
from koopsite.models import UserProfile


class AllFieldsView(AllFieldsMixin, MultipleObjectMixin, DetailView):
    """
    Базовий CBV для відображення ВСІХ полів одного запису моделі.
    Від AllFieldsMixin успадковано методи отримання списків значень
    і назв всіх полів будь-якого запису моделі.
    Успадкування від DetailView дозволяє отримати pk з url_conf
    і сам об'єкт, який передасться у складі контексту у шаблон
    під іменем object .
    Успадкування від MultipleObjectMixin дозволяє використати
    розбиття на сторінки списку. Сам список object_list формується
    методом get_label_value_list(self, obj) і охоплює всі поля моделі
    у заданому порядку.
    Ідентифікатори object та object_list можна продублювати цікавішими
    іменами, задавши значення атрибутам відповідно
    context_self_object_name та context_object_name
    """
    # Змінні, успадковані від AllFieldsMixin
    # model = None
    # fields  = ()        # Поля, які будуть виведені. Якщо порожній, то всі.
    # exclude = ('id',)   # Поля, які виключаються із списку виводу.
    # Наступні змінні будуть визначені в наслідуваному класі, наприклад:
    # per_page = 12
    # template_name = 'folders/report_detail.html'
    context_self_object_name = None # додатковий ідентифікатор для об'єкта self.object
    context_object_name = None # додатковий ідентифікатор для списку self.object_list

    def get_context_data(self, **kwargs):
        key_list, verbname_list = self.get_field_keys_verbnames()
        value_list = self.get_value_list(self.object, key_list)
        self.object_list = self.get_label_value_list(verbname_list, value_list)
        # self.object_list = self.get_label_value_list(self.object)
        context = super(AllFieldsView, self).get_context_data(**kwargs)
        if self.context_self_object_name:
            context[self.context_self_object_name] = self.object
        return context


class AllRecordsAllFieldsView(AllFieldsMixin, ListView):
    """
    Базовий CBV для відображення ВСІХ полів всіх записів моделі.
    Від AllFieldsMixin успадковано методи отримання списків значень
    і назв всіх полів будь-якого запису моделі.
    Успадкування від ListView:
      - get_queryset() - формує власне список записів,
        кожним елементом якого є список значень полів;
        під іменем objects_list цей список йде у шаблон
      - get_context_data() - доповнює контекст назвами полів;
      - context_object_name - можна заміними object_list
        на будь-що зручне для шаблону;
      - використовується розбиття на сторінки списку.
    Атрибут context_verbose_list_name = "field_name"  - ідентифікатор
        для списку назв полів.
    """
    # Змінні, успадковані від AllFieldsMixin
    # model = None
    # fields  = ()        # Поля, які будуть виведені. Якщо порожній, то всі.
    # exclude = ('id',)   # Поля, які виключаються із списку виводу.
    # Наступні змінні будуть визначені в наслідуваному класі, наприклад:
    # per_page = 12
    # template_name = 'folders/report_detail.html'
    # context_object_name = "field_val" # додатковий ідентифікатор для об'єкта self.object_list
    context_verbose_list_name = "field_names" # ідентифікатор для списку назв полів

    def get_queryset(self):
        key_list, verbname_list = self.get_field_keys_verbnames()
        records = self.model.objects.all()
        queryset = []
        for record in records:
            value_list = self.get_value_list(record, key_list)
            queryset.append(value_list)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllRecordsAllFieldsView, self).get_context_data(**kwargs)
        context[self.context_verbose_list_name] = self.get_field_keys_verbnames()[1] # назви полів
        return context



#################################################################
# Абстрактні суперкласи для двох моделей, пов'язаних OneToOne:
#     OneToOneCreate
#     OneToOneUpdate
#     OneToOneDetailShow
#
# Ці абстрактні класи є основою CBV для роботи з записами
# двох моделей, пов'язаних між собою через OneToOne.
# Моделі через свої форми виводяться в ЄДИНИЙ шаблон.
# Поля, які редагуються, визначаються у відповідних формах.
#
# Атрибути, які повинні бути означені в підмішуваному класі
# (як приклад: пара User-UserProfile - клас UserProfileOneToOne):
# ModelOne = User
# ModelTwo = UserProfile
# rel_name = 'userprofile'    # userprofile - reverse name to User model
# oto_name = 'user'           # user = models.OneToOneField(User) in UserProfile
# FormOne  = UserForm
# FormTwo  = ProfileForm
# capital_name  = 'username' # поле моделі one, яке буде виведене в заголовку шаблона
#
# Атрибути, які повинні бути означені в дочірньому класі:
# template_name = 'koop_user_prof_create.html'
#
#################################################################

class OneToOneBase:
    """
    Абстрактний клас - основа CBV для двох моделей,
    пов'язаних між собою через OneToOne.
    Означує лише атрибути. Вся логіка буде означена при змішуванні
    з класами CreateView тощо.
    """
    # render_variant = "as_ul"
    # render_variant = "as_p"
    render_variant  = "as_table"
    form_one_name   = 'form_one'  # назви форм у шаблоні: {{ form_one }}
    form_two_name   = 'form_two'
    finished        = False       # прапорець успішного завершення
    rel_name        = ''          # userprofile - reverse name to User model
    oto_name        = ''          # user = models.OneToOneField(User) in UserProfile
    capital_name    = ''          # поле моделі one, яке буде виведене в заголовку шаблона

    FormOne         = forms.ModelForm
    FormTwo         = forms.ModelForm
    ModelTwo        = models.Model
    ModelOne        = models.Model

    one_fields      = None
    two_fields      = None
    one_img_fields  = None
    two_img_fields  = None


    def get_one(self, request, *args, **kwargs):
        one_id = kwargs.get('pk') # ОТРИМАННЯ даних з URLconf
        one = self.ModelOne.objects.get(id=one_id)
        return one

    def get_two(self, one):
        try:
            two = getattr(one, self.rel_name)
        except:
            two = self.ModelTwo()
            setattr(two, self.oto_name, one)
        return two

    def set_one_outform_fields(self, one):
        """
        Встановлення значень полям моделі one, які не були присутні у формі
        Ця ф-ція має бути означена у дочірньому класі.
        """
        assert False, 'Клас OneToOneBase: потрібно означити метод: set_one_outform_fields'

    def set_two_outform_fields(self, two):
        """
        Встановлення значень полям моделі two, які не були присутні у формі
        Ця ф-ція має бути означена у дочірньому класі.
        """
        assert False, 'Клас OneToOneBase: потрібно означити метод: set_two_outform_fields'

#---------------- Кінець коду, охопленого тестуванням ------------------
# Наступні класи тестуються автоматично при тестуванні їх дочірніх класів:

class OneToOneCreate(OneToOneBase, CreateView):
    """
    Абстрактний клас - основа CBV для створення двох моделей,
    пов'язаних між собою через OneToOne.
    """
    def get(self, request, *args, **kwargs):
        form_one = self.FormOne()
        form_two = self.FormTwo()
        data = {self.form_one_name  : form_one,
                self.form_two_name  : form_two,
                'render_variant'    : self.render_variant,
                'finished'          : self.finished,
                }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        form_one = self.FormOne(data=request.POST, files=request.FILES)
        form_two = self.FormTwo(data=request.POST, files=request.FILES)
        capital = ""
        if form_one.is_valid() and form_two.is_valid():
            one = form_one.save()    # одночасно в базі зберігається примірник моделі
            one = self.set_one_outform_fields(one)
            one.save()
            two = form_two.save(commit=False)
            setattr(two, self.oto_name, one)
            two = self.set_two_outform_fields(two)
            two.save()
            capital = getattr(one, self.capital_name, '')
            self.finished = True            # редагування успішно завершене
        else:
            pass
            # print('ERRORS:', form_one.errors, form_two.errors)
        data = {self.form_one_name  : form_one,
                self.form_two_name  : form_two,
                'capital'           : capital,
                'render_variant'    : self.render_variant,
                'finished'          : self.finished,
                }
        return render(request, self.template_name, data)


class OneToOneUpdate(OneToOneBase, UpdateView):
    """
    Абстрактний клас - основа CBV для редагування двох моделей,
    пов'язаних між собою через OneToOne.
    """
    def get(self, request, *args, **kwargs):
        one = self.get_one(request, *args, **kwargs)
        two = self.get_two(one)
        form_one = self.FormOne(instance=one)
        form_two = self.FormTwo(instance=two)
        data = {self.form_one_name  : form_one,
                self.form_two_name  : form_two,
                'capital'           : getattr(one, self.capital_name),
                'one_id'            : getattr(one, 'id'),
                'render_variant'    : self.render_variant,
                'finished'          : self.finished,
                }
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        one = self.get_one(request, *args, **kwargs)
        two = self.get_two(one)
        form_one = self.FormOne(data=request.POST, files=request.FILES, instance=one)
        form_two = self.FormTwo(data=request.POST, files=request.FILES, instance=two)
        # print('form_one =', form_one.as_p())
        # print('form_two =', form_two.as_p())
        if form_one.is_valid() and form_two.is_valid():
            one = form_one.save()    # одночасно в базі зберігається примірник моделі
            two = form_two.save()
            self.finished = True            # редагування успішно завершене
        else:
            # Invalid form or forms - mistakes or something else?
            pass
            # print('ERRORS:', form_one.errors, form_two.errors)
        data = {self.form_one_name  : form_one,
                self.form_two_name  : form_two,
                'one_id'            : getattr(one, 'id'),
                'capital'           : getattr(one, self.capital_name),
                'render_variant'    : self.render_variant,
                'finished'          : self.finished,
                }
        return render(request, self.template_name, data)


class OneToOneDetailShow(OneToOneBase, DetailView):
    """
    Абстрактний клас - основа CBV для ПЕРЕГЛЯДУ двох моделей,
    пов'язаних між собою через OneToOne.
    """
    def get_one(self, request, *args, **kwargs):
        one_id = kwargs.get('pk') # ОТРИМАННЯ даних з URLconf
        one = self.ModelOne.objects.get(id=one_id)
        return one

    def get_two(self, one):
        try:
            two = getattr(one, self.rel_name)
        except:
            two = self.ModelTwo()
            setattr(two, self.oto_name, one)
        return two

    def get_obj(self, instance, fields):
        obj = []
        for k in fields:
            n = instance._meta.get_field(k).verbose_name
            v = getattr(instance, k)
            obj.append((k, n, v))
        return obj

    def get(self, request, *args, **kwargs):
        one = self.get_one(request, *args, **kwargs)
        two = self.get_two(one)
        obj_one = self.get_obj(one, self.one_fields)
        obj_two = self.get_obj(two, self.two_fields)
        data = {'obj_one' : obj_one,
                'obj_two' : obj_two,
                'one_img_fields' : self.one_img_fields,
                'two_img_fields' : self.two_img_fields,
                'capital'        : getattr(one, self.capital_name),
                'one_id'         : getattr(one, 'id'),
                }
        return render(request, self.template_name, data)


#################################################################
# CBV на базі абстрактних суперкласів для моделей User і UserProfile,
# пов'язаних OneToOne.
# Надалі назва UserProfile у назві View або Form означає
# поєднання обох моделей - User і UserProfile,
# тоді як назва просто Profile означає тільки модель UserProfile.
#################################################################

#---------------- ПОЧАТОК коду, охопленого тестуванням ------------------
# При тестуванні цих класів тестуються автоматично і їх суперкласи

class UserProfileOneToOne:
    """
    Клас для підмішування до абстрактного класу типу OneToOne...
    Основа CBV одночасно двох моделей:
    User і UserProfile
    """
    # Атрибути, потрібні абстрактному класу OneToOne...:
    ModelOne = User
    ModelTwo = UserProfile
    rel_name = 'userprofile'    # userprofile - reverse name to User model
    oto_name = 'user'           # user = models.OneToOneField(User) in UserProfile
    capital_name  = 'username' # поле моделі one, яке буде виведене в заголовку шаблона


class UserProfileCreate(UserProfileOneToOne, OneToOneCreate):
    """
    CBV для створення нового користувача і його профілю.
    Перевірка доступу не потрібна, оскільки анонімний користувач
    власне створює новий запис в моделі User (і UserProfile).
    """
    FormOne  = UserRegistrationForm
    FormTwo  = ProfileRegistrationForm
    template_name = 'koop_user_prof_create.html'

    def set_one_outform_fields(self, one):
        one.is_active = False  # Забороняємо авторизацію новоствореному
                                # користувачу поки адміністратор не
                                # встановить True
        one.set_password(one.password) # Хешуємо пароль методом set_password
        return one

    def set_two_outform_fields(self, two):
        return two


class UserProfilePersonDataUpdate(UserProfileOneToOne, OneToOneUpdate):
    """
    CBV для редагування даних користувача і його профілю.
    """
    FormOne  = UserPersonDataForm
    FormTwo  = ProfilePersonDataForm
    template_name = 'koop_adm_user_prof_update.html'

    # TODO-для правління прибрати можливість зміни персональних даних, а тільки - is_active i is_recognized
    # TODO-вилучити з форми можливість зміни ДОСТУПУ
    # TODO-чи використовується це view автором?
    # TODO-перевірити з декоратором author_or_permission_required(UserProfile...)
    # @method_decorator(author_or_permission_required(UserProfile, 'koopsite.change_userprofile'))
    @method_decorator(permission_required('koopsite.change_userprofile'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfilePersonDataUpdate, self).dispatch(request, *args, **kwargs)


#---------------- Кінець коду, охопленого тестуванням ------------------
# ( крім того, протестовано ф-цію index() )

class UserPermsFullUpdate(UserProfileOneToOne, OneToOneUpdate):
    FormOne  = UserPermsFullForm
    FormTwo  = ProfilePermForm
    template_name = 'koop_adm_user_perm_update.html'

    @method_decorator(permission_required('auth.change_permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserPermsFullUpdate, self).dispatch(request, *args, **kwargs)


class UserPermsActivateUpdate(UserProfileOneToOne, OneToOneUpdate):
    FormOne  = UserPermsActivateForm
    FormTwo  = ProfilePermForm
    template_name = 'koop_adm_user_perm_update.html'

    @method_decorator(permission_required('koopsite.activate_account'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserPermsActivateUpdate, self).dispatch(request, *args, **kwargs)


class UserProfileDetailShow(UserProfileOneToOne, OneToOneDetailShow):
    one_fields = ('username', 'first_name', 'last_name', 'email')
    two_fields = ('flat', 'picture')
    one_img_fields = None
    two_img_fields = ('picture',)
    template_name = 'koop_adm_user_prof.html'
    kwargs = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfileDetailShow, self).dispatch(request, *args, **kwargs)

    def get_one(self, request, *args, **kwargs):
        one_id = self.kwargs.get('pk') # ОТРИМАННЯ даних з URLconf
        one = self.ModelOne.objects.get(id=one_id)
        return one

    def get_obj(self, instance, fields):
        obj = []
        for k in fields:
            t = instance._meta.get_field(k).get_internal_type()
            n = instance._meta.get_field(k).verbose_name
            if instance._meta.model_name == 'user':
                n = user_verbose_names_uk.get(k, n)
            v = getattr(instance, k)
            obj.append((k, n, v))
        return obj


class OwnProfileDetailShow(UserProfileOneToOne, OneToOneDetailShow):
    one_fields = ('username', 'first_name', 'last_name', 'email')
    two_fields = ('flat', 'picture')
    one_img_fields = None
    two_img_fields = ('picture',)
    template_name = 'koop_own_prof.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(OwnProfileDetailShow, self).dispatch(request, *args, **kwargs)

    def get_one(self, request, *args, **kwargs):
        one_id = request.user.id # залогінений користувач
        one = self.ModelOne.objects.get(id=one_id)
        return one

    def get_obj(self, instance, fields):
        obj = []
        for k in fields:
            t = instance._meta.get_field(k).get_internal_type()
            n = instance._meta.get_field(k).verbose_name
            if instance._meta.model_name == 'user':
                n = user_verbose_names_uk.get(k, n)
            v = getattr(instance, k)
            obj.append((k, n, v))
        return obj


class OwnProfileUpdate(UserProfileOneToOne, OneToOneUpdate):
    FormOne  = UserPersonDataForm
    FormTwo  = ProfilePersonDataForm
    template_name = 'koop_own_prof_update.html'

    # TODO-для правління прибрати можливість зміни персональних даних, а тільки - is_active i is_recognized
    @method_decorator(login_required)
    @method_decorator(author_or_permission_required(UserProfile, 'koopsite.change_userprofile'))
    def dispatch(self, request, *args, **kwargs):
        return super(OwnProfileUpdate, self).dispatch(request, *args, **kwargs)

    def get_one(self, request, *args, **kwargs):
        one_id = request.user.id # залогінений користувач
        one = self.ModelOne.objects.get(id=one_id)
        # user_permissions_print(one)
        return one


class UsersList(ListView):
    model = User
    ordering = 'username'
    # paginate_by = 20
    template_name = 'koop_adm_users_list.html'
    @method_decorator(permission_required('koopsite.activate_account'))
    def dispatch(self, request, *args, **kwargs):
        return super(UsersList, self).dispatch(request, *args, **kwargs)


def user_login(request):
    template_name = 'koop_login.html'
    finished = False  # змінна буде передана в шаблон
    bad_details = False
    disabled_account = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                finished = True       # авторизація успішно завершена
            else:
                # An inactive account was used - no logging in!
                disabled_account = True
        else:
            bad_details = True
            print("Invalid login details: {0}, {1}".format(username, password))
    return render(request, template_name,
                  {'finished': finished,
                   'bad_details': bad_details,
                   'disabled_account': disabled_account,
                   })

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/index/')

@login_required
def change_password(request):
    template_name = 'koop_own_change_password.html'
    finished = False  # змінна буде передана в шаблон
    bad_details = False
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # don't logout the user.
            finished = True
            messages.success(request, "Password changed.")
        else:
            bad_details = True
            print('bad_details=', bad_details)
    else:
        form = PasswordChangeForm(request.user)
    data = {
        'form': form,
        'finished': finished,
        'bad_details': bad_details,
    }
    return render(request, template_name, data)

def index(request):
    """
    Домашня сторінка
    """
    template_name = 'koop_index.html'
    if request.method == 'POST':
        pass
    else:
        return render(request, template_name, {})

# TODO-можливо зробити декоратор перевірки належності до групи?
@permission_required('koopsite.activate_account')
def adm_index(request):
    template_name = 'koop_adm_index.html'
    if request.method == 'POST':
        pass
    else:
        return render(request, template_name, {})

def noaccess(request):
    template_name = 'koop_noaccess.html'
    if request.method == 'POST':
        pass
    else:
        return render(request, template_name, {})

def success(request):
    template_name = 'koop_success.html'
    if request.method == 'POST':
        pass
    else:
        return render(request, template_name, {})

def page_not_ready(request):
    template_name = 'koop_page_not_ready.html'
    if request.method == 'POST':
        pass
    else:
        return render(request, template_name, {})

