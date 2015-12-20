from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Permission, Group
from koopsite.functions import trace_print
from koopsite.models import UserProfile


class DummyUser():
    # Створення в тестовій базі даних користувача і профілю

    def create_dummy_user(self,
                              username='dummy_user',
                              password='top_secret',
                              last_name="",
                              first_name=""
                            ):
        User = get_user_model()
        User.objects.create_user(username=username, password=password,
                                first_name=first_name, last_name=last_name)
        user = authenticate(username=username, password=password)
        user.save()
        self.dummy_user = user
        trace_print('created user:', user)
        return user

    def add_dummy_permission(self, user, name='Can activate/deactivate account'):
        permission = Permission.objects.get(name=name)
        user.user_permissions.add(permission)
        user.save()
        # print('-'*50)
        # print('permission =', permission)
        #
        # user.is_staff = True
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

    def create_dummy_profile(self, user, flat=None, picture=None,
                              is_recognized=None):
        profile = UserProfile(user=user, flat=flat, picture=picture,
                              is_recognized=is_recognized)
        profile.save()
        trace_print('created profile:', profile, 'for user:', user)
        return profile


