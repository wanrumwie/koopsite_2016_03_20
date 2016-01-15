from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from .models import Folder, Report


class FolderFormBase(forms.ModelForm):
    # Базова форма для роботи з теками
    required_css_class  = 'required'
    error_css_class     = 'error'

    # Трюк з полями readonly:
    READONLY_FIELDS = []

    def __init__(self, *args, **kwargs):
        super(FolderFormBase, self).__init__(*args, **kwargs)
        for field in self.READONLY_FIELDS:
            self.fields[field].widget.attrs['readonly'] = True
            self.fields[field].widget.attrs['disabled'] = True

    class Meta:
        model  = Folder
        fields = ('parent', 'name', 'created_on')


class FolderForm(FolderFormBase):
    # Форма для вводу тек
    class Meta:
        model  = Folder
        fields = ('parent', 'name', 'created_on')


class FolderFormInFolder(FolderFormBase):
    # Форма для створення теки у материнській теці
    READONLY_FIELDS = ('parent',)

    class Meta:
        model  = Folder
        fields = ('parent', 'name',)


class FolderDeleteForm(FolderFormBase):
    # Форма для видалення теки
    READONLY_FIELDS = ('parent', 'name', 'created_on')


class ReportForm(forms.ModelForm):
    # Форма для вводу даних про файл
    required_css_class  = 'required'
    error_css_class     = 'error'

    class Meta:
        model = Report
        fields = ('parent', 'file')


class ReportFormInFolder(forms.ModelForm):
    # Форма для вводу даних про файл у відомій теці
    required_css_class  = 'required'
    error_css_class     = 'error'

    # Трюк з полями readonly:
    READONLY_FIELDS = ('parent',)

    def __init__(self, *args, **kwargs):
        super(ReportFormInFolder, self).__init__(*args, **kwargs)
        for field in self.READONLY_FIELDS:
            self.fields[field].widget.attrs['readonly'] = True
            self.fields[field].widget.attrs['disabled'] = True

    class Meta:
        model = Report
        fields = ('parent', 'file',)


class ReportUpdateForm(forms.ModelForm):
    # Форма для редагування даних про файл
    required_css_class  = 'required'
    error_css_class     = 'error'

    class Meta:
        model = Report
        fields = ('parent', 'filename', 'file')


#---------------- Кінець коду, охопленого тестуванням ------------------
