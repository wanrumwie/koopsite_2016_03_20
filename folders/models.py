import os
from django.db import models
from django.core.urlresolvers import reverse


def get_recursive_path(report):
    # Отримуємо шлях, який складається з вкладених каталогів:
    # "1/5/7/", де числа - це значення Folder.id починаючи з батьківського
    # Використовується ТІЛЬКИ для друку (напр. в  admin.py).
    id = report.parent.id
    path = ''
    # цикл починається з найглибшого каталога
    while id:
        path = os.path.join(str(id), path)
        # print('id = %2s   path = %s' % (id, path))
        folder = Folder.objects.get(id=id)
        if folder.parent:   id = folder.parent.id
        else:               break
    return path

'''
    Вирішено відмовитися від рекурсивних каталогів, оскільки
    1 - всі каталоги все одно мають унікальні назви, а саме  folder.id
    2 - зміна батьківського каталога для Report або Folder
        не потребуватиме фізичного переміщення каталогів і файлів,
        а означатиме лише зміни в базі даних моделей.
'''

def get_parents(folder):
    # Отримуємо список - ланцюжок тек,
    # батьківських відносно теки folder
    parents_list = []
    # цикл починається з теки, безпосередньо материнської до folder
    parent = folder.parent
    while parent:                   # якщо материнська тека існує,
        parents_list.append(parent) # додаємо її до списку
        parent = parent.parent      # і перевіряємо "бабусю"
    # print('parents_list=', parents_list)
    parents_list.reverse()
    return parents_list

def get_subfolders(parent):
    # Отримуємо список, який складається з тек,
    # безпосередньо дочірніх відносно parent
    queryset = Folder.objects.filter(parent=parent)
    return queryset

def get_subreports(parent):
    # Отримуємо список, який складається з файлів,
    # безпосередньо дочірніх відносно parent
    queryset = Report.objects.filter(parent=parent)
    return queryset


class Folder(models.Model):
    name        = models.CharField(max_length=256,
                                      verbose_name='Тека',
                                      # unique=True,
                                      error_messages={
                                         # інші помилки переозначені на поч. цього модуля
                                      'unique': "Така назва вже існує!"},
                                      )
    parent      = models.ForeignKey('self',
                                      verbose_name='Материнська тека',
                                      related_name='children',
                                      default=None,
                                      null=True,
                                      blank=True)
    created_on  = models.DateTimeField(verbose_name='Дата створення',
                                      # auto_now_add=True,
                                      null=True,
                                      blank=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('folders:folder-contents', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = ('тека')
        verbose_name_plural = ('теки')
        unique_together = (("parent", "name"),)
        permissions = (
                        ('view_folder', 'Can view folder'),
                        ('download_folder', 'Can download folder'),
        )


def get_report_path(report_id):
    # Повертає абс.шлях до файла (відносно MEDIA_ROOT)
    # Замість первісної назви файла використовується його id
    # Файли фізично записуються в теку з номером k = id // 512
    k = report_id // 512
    file_path = os.path.join('uploads',
                        'folders',      # підтека з назвою аплікації
                        str(k),         # тека для кожних 512 файлів
                        str(report_id)  # id файла
                        + ".data")       # фіктивне розширення файла
    # print('get_report_path:', report_id, k, file_path)
    return file_path


class Report(models.Model):
    def get_file_path(instance, filename):
        # Ця ф-ція призначена для динамічної зміни значення
        # параметра upload_to -  шляху збереження
        # файлів моделі (поля ImageField, FileFild)
        # Оскільки значення параметра upload_to є функцією (callable),
        # то вона автоматично приймає своїми параметрами instance і filename
        # з чого генерує стрічку - шлях збереження файлів:
        # upload_to=/uploads/folders/id/filename - СТАРИЙ ВАРІАНТ
        # upload_to=/uploads/folders/folder_id/file_id - НОВИЙ ВАРІАНТ
        # upload_to=/uploads/folders/k/file_id - НОВІШИЙ ВАРІАНТ,
        #   де k=id//512 - для кожних 512 файлів відкриватимемо нову теку
        # Але id визначається базою даних при збереженні, тому
        # для новоствореного запису id=None
        instance.filename = filename # в БД запишеться первинне ім'я файла
        file_path = get_report_path(instance.id)
        return file_path

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_file = self.file
            self.file = None
            super(Report, self).save(*args, **kwargs)
            self.file = saved_file
        super(Report, self).save(*args, **kwargs)

    parent   = models.ForeignKey(Folder,
                                      verbose_name='Тека',
                                      # null=True,
                                      # blank=True,
                                      related_name='reports',
                                      default=None)
    file     = models.FileField(verbose_name='Файл',
                                      upload_to=get_file_path,
                                      null=True,
                                      blank=True)
    filename = models.CharField(verbose_name='Назва файлу',
                                      max_length=512,
                                      # null=True,
                                      blank=True)
    uploaded_on  = models.DateTimeField(verbose_name='Дата заладування',
                                      auto_now_add=True,
                                      null=True,
                                      blank=True)
    def __str__(self):
        s = self.filename or ''
        return s
    def get_absolute_url(self):
        return reverse('folders:report-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = ('документ')
        verbose_name_plural = ('документи')
        permissions = (
                        ('view_report', 'Can view report'),
                        ('download_report', 'Can download report'),
        )



'''
@receiver(post_delete, sender=Report)
def report_postdelete(sender, instance, *args, **kwargs):
    instance.file.delete(save=False)
    def __str__(self):
        return self.filename


# Receive the pre_delete signal
# and delete the file associated with the model instance.
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=Report)
def report_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
'''
