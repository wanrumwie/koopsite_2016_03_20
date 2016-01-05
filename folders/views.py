from itertools import chain
from django.contrib.auth.decorators import login_required, permission_required
from django.http import *
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from folders.forms import ReportUpdateForm, FolderForm, FolderFormInFolder, ReportForm, ReportFormInFolder
from folders.functions import response_for_download, \
    response_for_download_zip, get_subfolders, get_subreports, \
    get_full_named_path
from folders.models import Folder, Report
from koopsite.views import AllFieldsView


class FolderList(ListView):
    model = Folder
    # paginate_by = 5
    ordering = 'name'
    template_name = 'folders/folder_list.html'


class FolderDetail(AllFieldsView):
    model = Folder
    template_name = 'folders/folder_detail.html'
    paginate_by = 12
    # exclude = ('id',)   # Поля, які виключаються із списку виводу.
    context_self_object_name = 'folder' # додатковий ідентифікатор для об'єкта self.object
    context_object_name = 'obj_details'  # додатковий ідентифікатор для списку self.object_list

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FolderDetail, self).dispatch(request, *args, **kwargs)


class ReportList(ListView):
    model = Report
    # paginate_by = 20
    ordering = 'filename'
    template_name = 'folders/report_list.html'


class ReportDetail(AllFieldsView):
    model = Report
    template_name = 'folders/report_detail.html'
    paginate_by = 12
    # exclude = ('id',)   # Поля, які виключаються із списку виводу.
    context_self_object_name = 'report'  # додатковий ідентифікатор для об'єкта self.object
    context_object_name = 'obj_details'  # додатковий ідентифікатор для списку self.object_list

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReportDetail, self).dispatch(request, *args, **kwargs)


class ReportPreview(DetailView):
    model = Report
    template_name = 'folders/report_preview.html'
    # url_name='report-preview'

    @method_decorator(permission_required('folders.view_report'))
    def dispatch(self, request, *args, **kwargs):
        return super(ReportPreview, self).dispatch(request, *args, **kwargs)


class FolderCreate(CreateView):
    model = Folder
    form_class = FolderForm
    template_name = 'folders/folder_create.html'

    @method_decorator(permission_required('folders.add_folder'))
    def dispatch(self, *args, **kwargs):
        return super(FolderCreate, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('folders:folder-list-all')


class FolderCreateInFolder(CreateView):
    # Створюємо теку у відомій материнській теці
    model = Folder
    form_class = FolderFormInFolder
    template_name = 'folders/folder_create.html'
    kwargs = {}

    @method_decorator(permission_required('folders.add_folder'))
    def dispatch(self, *args, **kwargs):
        self.kwargs.update({'parent': kwargs.get('parent') or 1}) # ОТРИМАННЯ даних з URLconf
        return super(FolderCreateInFolder, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('folders:folder-list')
        # return reverse('folders:folder-contents', kwargs={'pk': self.kwargs.get('parent')})

    def form_valid(self, form):
        folder = form.save(commit=False)    # збережений ще "сирий" примірник
        parent = Folder.objects.get(id=self.kwargs.get('parent'))
        folder.parent = parent              # foreignkey
        folder.created_on = timezone.now()  # не використовуємо auto_now
        folder.save()                       # остаточне збереження
        return HttpResponseRedirect(self.get_success_url())


class FolderDelete(DeleteView):
    model = Folder
    form_class = FolderForm
    template_name = 'folders/folder_delete.html'

    @method_decorator(permission_required('folders.delete_folder'))
    def dispatch(self, *args, **kwargs):
        return super(FolderDelete, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        folder = self.get_object()
        if get_subfolders(folder) or get_subreports(folder):
            return HttpResponseRedirect(reverse('folders:folder-not-empty'))
        else:
            folder.delete()
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('folders:folder-list')


class ReportDelete(DeleteView):
    model = Report
    form_class = ReportForm
    template_name = 'folders/report_delete.html'

    @method_decorator(permission_required('folders.delete_report'))
    def dispatch(self, *args, **kwargs):
        return super(ReportDelete, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.file.delete()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('folders:report-list')


class FolderUpdate(UpdateView):
    model = Folder
    form_class = FolderForm
    template_name = 'folders/folder_update.html'

    @method_decorator(permission_required('folders.change_folder'))
    def dispatch(self, *args, **kwargs):
        # self.parent_id = kwargs.get('parent') or 1 # ОТРИМАННЯ даних з URLconf
        return super(FolderUpdate, self).dispatch(*args, **kwargs)


class ReportUpdate(UpdateView):
    model = Report
    form_class = ReportUpdateForm
    # fields = ('parent', 'filename', 'file')
    template_name = 'folders/report_update.html'

    @method_decorator(permission_required('folders.change_report'))
    def dispatch(self, *args, **kwargs):
        # print('     kwargs =', kwargs)
        # print('self.kwargs =', kwargs)
        # self.parent_id = kwargs.get('parent') or 1 # ОТРИМАННЯ даних з URLconf
        return super(ReportUpdate, self).dispatch(*args, **kwargs)

    # TODO-2015 12 29 Впорядкувати success_url для різних views
    # Використати в шаблоні:
    # a href="{{ object.get_absolute_url }}">{{ object.name }}</a>

    def get_success_url(self):
        return reverse('folders:folder-list-all')


class ReportUpload(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'folders/report_upload.html'

    @method_decorator(permission_required('folders.add_report'))
    def dispatch(self, *args, **kwargs):
        return super(ReportUpload, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('folders:folder-list-all')


class ReportUploadInFolder(CreateView):
    # Завантажуємо файл у відому материнську теку
    model = Report
    form_class = ReportFormInFolder
    template_name = 'folders/report_upload.html'
    kwargs = {}

    @method_decorator(permission_required('folders.add_report'))
    def dispatch(self, *args, **kwargs):
        self.kwargs.update({'parent': kwargs.get('parent') or 1}) # ОТРИМАННЯ даних з URLconf
        # self.parent_id = kwargs.get('parent') or 1  # ОТРИМАННЯ даних з URLconf
        return super(ReportUploadInFolder, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        report = form.save(commit=False)    # збережений ще "сирий" примірник, щоб отримати id
        parent = Folder.objects.get(id=self.kwargs.get('parent'))
        report.parent = parent              # foreignkey
        report.save()                       # остаточне збереження
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('folders:report-list')
        # return reverse('folders:folder-contents', kwargs={'pk': self.kwargs.get('parent')})


@permission_required('folders.download_folder')
def folderDownload(request, pk):
    # Завантаження zip-файла, який складається з всіх файлів теки
    folder_id = pk
    folder = Folder.objects.get(id=folder_id)
    response, zipFilename, msg = response_for_download_zip(folder)
    return response

@permission_required('folders.download_report')
def reportDownload(request, pk):
    report_id = pk
    report = Report.objects.get(id=report_id)
    print('report=', report.id, report.filename, report.file)
    response = response_for_download(report)
    return response


class FolderParentList(ListView):
    # Перегляд тек, які не є дочірніми (тобто, кореневих тек)
    queryset = Folder.objects.filter(parent=None)
    # paginate_by = 20
    template_name = 'folders/folder_parents.html'


class FolderReportList(ListView):
    # paginate_by = 15
    template_name = 'folders/folder_list_all.html'
    # context_object_name = "all_list" # додатковий ідентифікатор для списку self.object_list

    def get_queryset(self):
        # Дочірні об'єкти:
        # два queryset з різних моделей об'єднується в один qs,
        # який обробляється в template як одне ціле
        fs = Folder.objects.all()
        rs = Report.objects.all()
        qs = list(chain(fs, rs))
        qs = sorted(qs, key=lambda x: get_full_named_path(x))
        return qs


