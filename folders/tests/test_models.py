from django.core.urlresolvers import reverse
from django.test import TestCase
from folders.models import Folder, Report


class FolderAndReportModelsTest(TestCase):

    def test_saving_and_retrieving_reports(self):
        folder = Folder()
        folder.save()

        first_report = Report()
        first_report.filename = 'The first (ever) folder report'
        first_report.parent = folder
        first_report.save()

        second_report = Report()
        second_report.filename = 'Report the second'
        second_report.parent = folder
        second_report.save()

        saved_folder = Folder.objects.first()
        self.assertEqual(saved_folder, folder)

        saved_reports = Report.objects.all()
        self.assertEqual(saved_reports.count(), 2)

        first_saved_report = saved_reports[0]
        second_saved_report = saved_reports[1]

        self.assertEqual(first_saved_report.filename, 'The first (ever) folder report')
        self.assertEqual(first_saved_report.parent, folder)
        self.assertEqual(second_saved_report.filename, 'Report the second')
        self.assertEqual(second_saved_report.parent, folder)

    # TODO-переробити цей тест для випадку відсутнього файла і назви
    # def test_cannot_save_empty_report(self):
    #     folder = Folder.objects.create()
    #     report = Report(parent=folder, filename='')
    #     with self.assertRaises(ValidationError):
    #         report.save()
    #         report.full_clean()   # Django не перевіряє порожніх текстових полів!
                                # full_clean заставить провести валідацію.

    def test_folder_get_absolute_url(self):
        folder = Folder.objects.create()
        expected = reverse('folder-contents', kwargs={'pk': folder.pk})
        self.assertEqual(folder.get_absolute_url(), expected)

    def test_report_get_absolute_url(self):
        folder = Folder.objects.create()
        report = Report(parent=folder)
        report.save()
        expected = reverse('report-detail', kwargs={'pk': report.pk})
        self.assertEqual(report.get_absolute_url(), expected)




