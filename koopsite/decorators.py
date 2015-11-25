from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def ajax_login_required(view):
    print('view=',view)
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        print('wrapper: request.user=', request.user)
        if not request.user.is_authenticated():
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper

# def ajax_permission_required(perm):
#     # @wraps(view)
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_authenticated():
#             raise PermissionDenied
#         return view(request, *args, **kwargs)
#     return wrapper


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

'''
# Використання LoginRequiredMixin:
class MyView(LoginRequiredMixin, ...):
    # this is a generic view
    ...
'''

'''
# Декоратор для класу:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FolderCreate, self).dispatch(*args, **kwargs)
'''

'''
@group_required('admins','editors')
def myview(request, id):
...
'''

