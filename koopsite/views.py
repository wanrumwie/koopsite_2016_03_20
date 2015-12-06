import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from flats.models import Flat
from koopsite.forms import UserPermsFullForm, ProfileRegistrationForm, \
                            UserPermsActivateForm, \
                            ProfilePersonDataForm, user_verbose_names_uk, ProfilePermForm
from koopsite.settings import BASE_DIR
from .models import User, UserProfile
from .forms import UserRegistrationForm, UserPersonDataForm


def context_per_page(obj_key,  context, page=1, per_page=12):
    # Функція зміни контексту з доп. Paginator
    # З цілого списку в контекст поступає лише частина, відповідно до page
    paginator = Paginator(context[obj_key], per_page=per_page)
    context['paginator']    = paginator
    context['is_paginated'] = True
    pp                      = paginator.page(page)
    context['page_obj']     = pp
    context[obj_key]        = pp.object_list # частина списку в межах page
    return context


class AllDetailView(DetailView):
    # CBV для виводу всіх полів одного запису моделі
    keylist = []            # Список полів, які буде виведено.
                            # Якщо пустий, то список полів буде __dict__
    namedict = {}           # Словник укр.назв полів, які буде виведено.
                            # Якщо пустий, то назви будуть взяті з keylist
    valfunction = round     # Функція обробки значення поля (напр. round)
    fargs = (2,)            # список аргументів функції f(v, *fargs)
    fkwargs = {}            # словник аргументів функції f(v, **fkwargs)
    url_name = ''           # параметр name в url(), який є основним для
                            # даного DetailView (ще без сторінок)
    # Наступні змінні будуть визначені в наслідуваному класі:
    # model = Report
    # template_name = 'folders/report_detail.html'
    # per_page = 12

    def get_context_data(self, **kwargs):
        context = super(AllDetailView, self).get_context_data(**kwargs)
        obj = context['object']
        # url_prefix - повна адреса для даного pk ще без сторінок
        url_prefix=reverse(self.url_name, kwargs={'pk': obj.pk})
        context['url_prefix'] = url_prefix + 'page'
        # href="{{ url_prefix }}{{ page_obj.previous_page_number }}" => "/flats/page43"
        obj_details = []
        keylist = self.keylist or obj.__dict__
        for k in keylist:
            try:    n = self.namedict[k]
            except: n = k
            v = getattr(obj,k)
            if self.valfunction:
                try:    v = self.valfunction(v, *self.fargs, **self.fkwargs)
                        # Замість v = round(v,2) або v = round(v,ndigits=2)
                except: pass
            if v == 0: v = ""
            obj_details.append((n, v))
        context['obj_details']  = obj_details    # весь список
        # Наступний фрагмент додано,
        # бо DetailView не має вбудованого paginator'a
        if self.per_page > 0:
            page = self.kwargs.get('page') or 1 # ОТРИМАННЯ даних з URLconf
            # зміна контексту для відображення одної сторінки
            context = context_per_page('obj_details', context, page, self.per_page)
        return context


class AllRecordDetailView(ListView):
    # CBV для виводу всіх полів всіх записів моделі
    # ПОТРІБНО універсалізувати: замість Flat поставити б-я модель
    model = Flat
    per_page = 15
    template_name = 'flats/flat_table.html'
    url_name = 'flat-table' # параметр name в url(), який є основним для
                            # даного DetailView (ще без сторінок)

    def get_context_data(self, **kwargs):
        context = super(AllRecordDetailView, self).get_context_data(**kwargs)
        # url_prefix - повна адреса для даного pk ще без сторінок
        url_prefix=reverse(self.url_name)
        context['url_prefix'] = url_prefix + 'page'
        field_name = []
        field_val  = []
        firstiter  = True
        for flat in Flat.objects.order_by('flat_99'):
            flatval  = []
            for k in flat.fieldsList:
                if firstiter:
                    n = flat.mdbFields[k]
                    field_name.append(n)
                v = getattr(flat,k)
                try:
                    v = round(v,2)
                except:
                    pass
                if v == 0: v = ""
                flatval.append(v)
            field_val.append(flatval)
            firstiter = False
        context['field_name'] = field_name    # наззви полів
        context['field_val']  = field_val     # весь список
        # Наступний фрагмент додано,
        # бо вбудований в ListView paginator опрацьовує object_list,
        # а не 2D масив, який передається в шаблон
        if self.per_page > 0:
            page = self.kwargs.get('page') or 1 # ОТРИМАННЯ даних з URLconf
            # зміна контексту для відображення одної сторінки
            context = context_per_page('field_val', context, page, self.per_page)
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

class OneToOneCreate(CreateView):
    """
    Абстрактний клас - основа CBV для створення нових записів
    двох моделей, пов'язаних між собою через OneToOne.
    """
    #
    # Атрибути, які можна залишити в успадкованому класі:
    render_variant = "as_table"
    # render_variant = "as_ul"
    # render_variant = "as_p"
    form_one_name = 'form_one'     # назви форм у шаблоні: {{ form_one }}
    form_two_name = 'form_two'
    finished = False                # прапорець успішного завершення

    def set_one_outform_fields(self, one):
        """
        Встановлення значень полям моделі one, які не були присутні у формі
        Ця ф-ція має бути означена у дочірньому класі.
        """
        assert False, 'Клас OneToOneCreate: потрібно означити метод: set_one_outform_fields'

    def set_two_outform_fields(self, two):
        """
        Встановлення значень полям моделі two, які не були присутні у формі
        Ця ф-ція має бути означена у дочірньому класі.
        """
        assert False, 'Клас OneToOneCreate: потрібно означити метод: set_two_outform_fields'

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
            print('ERRORS:', form_one.errors, form_two.errors)
        data = {self.form_one_name  : form_one,
                self.form_two_name  : form_two,
                'capital'           : capital,
                'render_variant'    : self.render_variant,
                'finished'          : self.finished,
                }
        return render(request, self.template_name, data)


class OneToOneUpdate(UpdateView):
    """
    Абстрактний клас - основа CBV для редагування двох моделей,
    пов'язаних між собою через OneToOne.
    """
    #
    # Атрибути, які можна залишити в успадкованому класі:
    render_variant = "as_table"
    # render_variant = "as_ul"
    # render_variant = "as_p"
    form_one_name = 'form_one'     # назви форм у шаблоні
    form_two_name = 'form_two'
    finished = False                # прапорець успішного завершення

    def get_one(self, request, *args, **kwargs):
        one_id = self.kwargs.get('pk') # ОТРИМАННЯ даних з URLconf
        one = self.ModelOne.objects.get(id=one_id)
        return one

    def get_two(self, one):
        try:
            two = getattr(one, self.rel_name)
        except:
            two = self.ModelTwo()
            setattr(two, self.oto_name, one)
        return two

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
        # print('form_one =', form_one)
        # print('form_two =', form_two)
        if form_one.is_valid() and form_two.is_valid():
            one = form_one.save()    # одночасно в базі зберігається примірник моделі
            two = form_two.save()
            self.finished = True            # редагування успішно завершене
        else:
            # Invalid form or forms - mistakes or something else?
            print('ERRORS:', form_one.errors, form_two.errors)
        data = {self.form_one_name  : form_one,
                self.form_two_name  : form_two,
                'one_id'            : getattr(one, 'id'),
                'capital'           : getattr(one, self.capital_name),
                'render_variant'    : self.render_variant,
                'finished'          : self.finished,
                }
        return render(request, self.template_name, data)


class OneToOneDetailShow(DetailView):
    """
    Абстрактний клас - основа CBV для ПЕРЕГЛЯДУ двох моделей,
    пов'язаних між собою через OneToOne.
    """

    def get_one(self, request, *args, **kwargs):
        one_id = self.kwargs.get('pk') # ОТРИМАННЯ даних з URLconf
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
        print('data =', data)
        return render(request, self.template_name, data)


#################################################################
# CBV на базі абстрактних суперкласів для моделей User і UserProfile,
# пов'язаних OneToOne.
# Надалі назва UserProfile у назві View або Form означає
# поєднання обох моделей - User і UserProfile,
# тоді як назва просто Profile означає тільки модель UserProfile.
#################################################################

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
    # FormOne  = UserPermsFullForm
    # FormTwo  = ProfileFullForm
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

    # TODO-додати право доступу для ВЛАСНИКА профілю
    # TODO-для правління прибрати можливість зміни персональних даних, а тільки - is_active i is_recognized
    # TODO-вилучити з форми можливість зміни ДОСТУПУ
    @method_decorator(permission_required('koopsite.change_userprofile'))
    def dispatch(self, request, *args, **kwargs):
        return super(UserProfilePersonDataUpdate, self).dispatch(request, *args, **kwargs)


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

    # TODO-додати право доступу для ВЛАСНИКА профілю
    # TODO-для правління прибрати можливість зміни персональних даних, а тільки - is_active i is_recognized
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(OwnProfileUpdate, self).dispatch(request, *args, **kwargs)

    def get_one(self, request, *args, **kwargs):
        one_id = request.user.id # залогінений користувач
        one = self.ModelOne.objects.get(id=one_id)
        # print_user_permissions(one)
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

def qunit_page(request):
    template_name = 'js_tests/js_tests.html'
    # template_name = os.path.join(BASE_DIR, "static/koopsite", "js_tests", "js_tests.html")
    if request.method == 'POST':
        pass
    else:
        return render(request, template_name, {})


