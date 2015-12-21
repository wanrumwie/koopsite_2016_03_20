from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.http import *
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from folders.functions import response_for_download, response_for_download_zip
from koopsite.views import AllFieldsView
from .models import Folder, Report, \
                    get_subfolders, get_subreports
from .forms import FolderForm, ReportForm, \
                    FolderFormInFolder, ReportFormInFolder


class FolderList(ListView):
    model = Folder
    paginate_by = 5
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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReportPreview, self).dispatch(request, *args, **kwargs)


class FolderCreate(CreateView):
    model = Folder
    form_class = FolderForm
    template_name = 'folders/folder_create.html'

    @method_decorator(permission_required('folders.add_folder'))
    def dispatch(self, *args, **kwargs):
        return super(FolderCreate, self).dispatch(*args, **kwargs)


class FolderCreateInFolder(CreateView):
    # Створюємо теку у відомій материнській теці
    model = Folder
    form_class = FolderFormInFolder
    template_name = 'folders/folder_create.html'

    @method_decorator(permission_required('folders.add_folder'))
    def dispatch(self, *args, **kwargs):
        self.kwargs.update({'parent': kwargs.get('parent') or 1}) # ОТРИМАННЯ даних з URLconf
        return super(FolderCreateInFolder, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        # return reverse('folder-contents', kwargs={'pk': self.parent_id})
        return reverse('folders:folder-contents', kwargs={'pk': self.kwargs.get('parent')})

    def form_valid(self, form):
        folder = form.save(commit=False)    # збережений ще "сирий" примірник
        parent = Folder.objects.get(id=self.kwargs.get('parent'))
        folder.parent = parent              # foreignkey
        folder.created_on = datetime.now()  # не використовуємо auto_now
        folder.save()                       # остаточне збереження
        print('form saved')
        return HttpResponseRedirect(self.get_success_url())


class ReportDelete(DeleteView):
    model = Report
    form_class = ReportForm
    template_name = 'folders/report_delete.html'

    def get_success_url(self):
        return reverse('report-list')

    @method_decorator(permission_required('folders.delete_report'))
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object)
        self.object.file.delete()
        print('file deleted')
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class FolderDelete(DeleteView):
    model = Folder
    form_class = FolderForm
    template_name = 'folders/folder_delete.html'

    def get_success_url(self):
        return reverse('folder-list')

    @method_decorator(permission_required('folders.delete_folder'))
    def delete(self, request, *args, **kwargs):
        folder = self.get_object()
        print(folder)
        if get_subfolders(folder) or get_subreports(folder):
            return HttpResponseRedirect('folder_not_empty')
        else:
            folder.delete()
            print('file deleted')
            return HttpResponseRedirect(self.get_success_url())


class FolderUpdate(UpdateView):
    model = Folder
    form_class = FolderForm
    template_name = 'folders/folder_update.html'

    @method_decorator(permission_required('folders.add_folder'))
    def dispatch(self, *args, **kwargs):
        self.parent_id = kwargs.get('parent') or 1 # ОТРИМАННЯ даних з URLconf
        return super(FolderUpdate, self).dispatch(*args, **kwargs)


class ReportUpdate(UpdateView):
    model = Report
    # form_class = ReportForm
    fields = ('parent', 'filename', 'file')
    template_name = 'folders/report_update.html'

    @method_decorator(permission_required('folders.change_report'))
    def dispatch(self, *args, **kwargs):
        print('     kwargs =', kwargs)
        print('self.kwargs =', kwargs)
        self.parent_id = kwargs.get('parent') or 1 # ОТРИМАННЯ даних з URLconf
        return super(ReportUpdate, self).dispatch(*args, **kwargs)


class ReportUpload(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'folders/report_upload.html'

    @method_decorator(permission_required('folders.add_report'))
    def dispatch(self, *args, **kwargs):
        self.parent_id = kwargs.get('parent') or 1 # ОТРИМАННЯ даних з URLconf
        return super(ReportUpload, self).dispatch(*args, **kwargs)


class ReportUploadInFolder(CreateView):
    # Завантажуємо файл у відому материнську теку
    model = Report
    form_class = ReportFormInFolder
    template_name = 'folders/report_upload.html'

    def get_success_url(self):
        return reverse('folder-contents', kwargs={'pk': self.parent_id})

    @method_decorator(permission_required('folders.add_report'))
    def dispatch(self, *args, **kwargs):
        self.parent_id = kwargs.get('parent') or 1  # ОТРИМАННЯ даних з URLconf
        return super(ReportUploadInFolder, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        report = form.save(commit=False)    # збережений ще "сирий" примірник, щоб отримати id
        parent = Folder.objects.get(id=self.parent_id)
        report.parent = parent              # foreignkey
        report.save()                       # остаточне збереження
        return HttpResponseRedirect(self.get_success_url())


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
    response = response_for_download(report)
    return response

# def success(request):
#     if request.method == 'POST':
#         pass
#     else:
#         return render(request, 'folders/folder_success.html')


class FolderParentList(ListView):
    # Перегляд тек, які не є дочірніми (тобто, кореневих тек)
    queryset = Folder.objects.filter(parent=None)
    # paginate_by = 20
    template_name = 'folders/folder_parents.html'


