from django import forms
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
    class Meta:
        model  = Folder
        fields = ('name',)


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
    class Meta:
        model = Report
        fields = ('file',)

