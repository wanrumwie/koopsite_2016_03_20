from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from koopsite.functions import trace_print
from koopsite.models import UserProfile


class DummyUser():
    # Створення в тестовій базі даних користувача і профілю

    def create_dummy_user(self,
                              username='dummy_user',
                              password='top_secret',
                              last_name="",
                              first_name="",
                              id=None
                            ):
        User = get_user_model()
        User.objects.create_user(username=username, password=password,
                                first_name=first_name, last_name=last_name,
                                id=id)
        user = authenticate(username=username, password=password)
        user.save()
        self.dummy_user = user
        trace_print('created user:', user)
        return user

    def add_dummy_permission(self, user, codename='activate_account', model=None):
        perms = Permission.objects.all()
        if model:
            content_type =  ContentType.objects.get(model=model)
            permission = Permission.objects.get(codename=codename, content_type=content_type)
        else:
            permission = Permission.objects.get(codename=codename)
        user.user_permissions.add(permission)
        user.save()
        trace_print('added permission:', permission, 'for user:', user)
        return permission

    def create_dummy_group(self, group_name):
        group = Group(name=group_name)
        group.save()
        return group

    def add_dummy_group(self, user, group_name):
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        return group

    def create_dummy_profile(self, user, id=None, flat=None, picture=None,
                             picture_path=None,
                             is_recognized=None):
        if picture_path and not picture:
            # створимо picture з файла на диску:
            with open(picture_path, 'rb') as file:
                picture = SimpleUploadedFile(picture_path, file.read())
        profile = UserProfile(user=user, id=id, flat=flat, picture=picture,
                              is_recognized=is_recognized)
        profile.save()
        trace_print('created profile:', profile, 'for user:', user)
        return profile


