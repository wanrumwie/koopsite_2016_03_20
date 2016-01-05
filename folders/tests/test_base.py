from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from folders.models import Folder, Report


class DummyFolder():
    # Створення в базі додаткових даних, потрібних для конкретного класу тестів

    def create_dummy_root_folder(self, name="dummy_root_folder",
                            parent=None, created_on=None):
        # створюємо теку з id=1 для folders/1/contents/:
        folder = Folder(id=1, name=name, parent=parent, created_on=created_on)
        folder.save()
        # print('created folder:', folder)
        return folder

    def create_dummy_folder(self, name="dummy_folder",
                            parent=None, created_on=None):
        # створюємо теку:
        folder = Folder(name=name, parent=parent, created_on=created_on)
        folder.save()
        # print('created folder:', folder)
        return folder

    def create_children(self, parent, d, deep, wide, report):
        if d < deep:
            for w in range(wide):
                folder = self.create_dummy_folder(parent=parent,
                            name='%s_%s_%s' % (parent.name, d, w))
                if report:
                    self.create_dummy_report(parent=folder,
                            filename='%s_%s' % ('r', folder.name))
                self.create_children(folder, d+1, deep, wide, report)

    def create_dummy_catalogue(self, deep=2, wide=2, report=False):
        parent = self.create_dummy_root_folder(name="dum_f_0")
        self.create_children(parent, 0, deep, wide, report)

    def create_dummy_report(self, parent, file=None,
                            filename=None, uploaded_on=None):
        # створюємо документ:
        report = Report(parent=parent, file=file,
                        filename=filename, uploaded_on=uploaded_on)
        report.save()
        # print('created report:', report)
        return report



