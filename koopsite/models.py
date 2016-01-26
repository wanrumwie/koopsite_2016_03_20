import os
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from flats.models import Flat


class UserProfile(models.Model):
    def get_file_path(instance, filename):
        # Ця ф-ція призначена для динамічної зміни значення
        # параметра upload_to -  шляху збереження
        # файлів моделі (поля ImageField, FileField)
        # Оскільки значення параметра upload_to є функцією (callable),
        # то вона автоматично приймає своїми параметрами instance і filename
        # з чого генерує стрічку - шлях збереження файлів:
        # upload_to=profile_images/<user.id>.img
        # Але id визначається базою даних при збереженні, тому
        # для новоствореного запису id=None
        fn = "%s.jpg" % (instance.user_id)
        file_path = os.path.join('profile_images', fn)
        return file_path

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_file = self.picture
            self.picture = None
            super().save(*args, **kwargs)
            self.picture = saved_file
        super().save(*args, **kwargs)

    user = models.OneToOneField(User)
    # Додаткові поля для профілю користувача:
    flat    = models.ForeignKey(Flat,
                            verbose_name='Квартира',
                            # default=None,
                            blank=True,
                            null=True,
                            related_name='userprofiles',
                            )
    picture = models.ImageField(
                            verbose_name='Аватар',
                            # help_text="Зображення, яке слід вивантажити у профіль.",
                            upload_to=get_file_path,
                            blank=True,
                            null=True,
                            )
    is_recognized = models.NullBooleanField(
        # Поле для використання адміністратором, або тим хто
        # має право на активацію користувача.
        # Можливі значення is_recognized ("Чи визнається користувач"):
        # none  - при реєстрації новий користувач ще не підтверджений,
        #         активація акаунту можлива
        #         в індивідуальному порядку без попереднього
        #         встановлення is_recognized=True;
        # False - користувач не підтверджений,
        #         заборонено активувати акаунт
        #         (буде заблоковано спробу встановити is_active-True);
        # True  - користувач підтверджений, його акаунт можна
        #         активувати як індивідуально, так і "скопом".
        # Під "активацією акаунту" мається на увазі
        # встановлення прапорця is_active -> True,
        # що дасть можливість авторизуватися.
                            verbose_name='Підтверджений',
                            # help_text="Чи визнаємо за користувачем право на авторизацію.",
                            blank=True,
                            null=True,
                            default=None,
                            )

    def __str__(self):
        return self.user.username + ' (профіль)'

    def get_absolute_url(self):
        url_name = 'adm-users-profile'
        user_pk = self.user.id
        return reverse(url_name, kwargs={'pk': user_pk})

    class Meta:
        verbose_name = ('профіль користувача')
        verbose_name_plural = ('профілі користувачів')
        permissions = (
                        ('activate_account', 'Can activate/deactivate account'),
                        ('view_userprofile', 'Can view user profile'),
        )

#---------------- Кінець коду, охопленого тестуванням ------------------
