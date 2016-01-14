from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from .models import Folder, Report


class FolderForm(forms.ModelForm):
    # Форма для вводу тек
    required_css_class  = 'required'
    error_css_class     = 'error'
    class Meta:
        model  = Folder
        fields = ('parent', 'name', 'created_on')


class FolderFormInFolder(forms.ModelForm):
    # Форма для створення теки у материнській теці
    required_css_class  = 'required'
    error_css_class     = 'error'

    # Трюк з полями readonly:
    READONLY_FIELDS = ('parent',)

    def __init__(self, *args, **kwargs):
        super(FolderFormInFolder, self).__init__(*args, **kwargs)
        for field in self.READONLY_FIELDS:
            self.fields[field].widget.attrs['readonly'] = True
            self.fields[field].widget.attrs['disabled'] = True

    class Meta:
        model  = Folder
        fields = ('parent', 'name',)


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
