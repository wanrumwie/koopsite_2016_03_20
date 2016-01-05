from django.test import TestCase
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from koopsite.urls import urlpatterns


class WalkURL():
    def __init__(self, urlpatterns, exclude_namespace=None):
        self.urlpatterns = urlpatterns
        if exclude_namespace:
            if isinstance(exclude_namespace, list):
                self.exclude_namespace = exclude_namespace
            else:
                self.exclude_namespace = [exclude_namespace]
        else:
            self.exclude_namespace = []
        print("WalkURL(exclude_namespace =", self.exclude_namespace)
        self.all_url_names = []
        self.get_all_url_names()

    def url_walk(self, urlpatterns, prefix='^', namespace=None):
        for u in urlpatterns:
            if type(u) == RegexURLPattern:
                s = u.regex.pattern
                s = prefix + s.lstrip('^')
                ns = ('%s:' % namespace) if namespace else ''
                # print('%-50s %-15s %s' % (s, ns, u.name))
                self.all_url_names.append((s, '%s%s' % (ns, u.name)))
            if type(u) == RegexURLResolver:
                ns = u.namespace or '--'
                if ns not in self.exclude_namespace:
                    self.url_walk(u.url_patterns, prefix=u.regex.pattern, namespace=u.namespace)

    def get_all_url_names(self):
        self.url_walk(self.urlpatterns, prefix='^', namespace=None)
        return self.all_url_names

def get_duplicates(lst):
    d = [x for x in lst if lst.count(x) > 1]
    return d

def get_duplicates_in_tuple_list(lst):
    u_list = []
    n_list = []
    for u, n in lst:
        u_list.append(u)
        n_list.append(n)
    du = []
    dn = []
    for u, n in lst:
        if u_list.count(u) > 1: du.append((u, n))
        if n_list.count(n) > 1: dn.append((u, n))
    return du, dn


class UrlNameSpaceTest(TestCase):

    def test_no_duplicate_urls(self):
        all_url = WalkURL(urlpatterns,
                          exclude_namespace=['js_tests']).all_url_names
        # print('all_urls:')
        # for u, n in sorted(all_url):
        #     print('%-60s %s' % (u, n))
        # print('-'*50)

        dupl_in_urls, dupl_in_name = get_duplicates_in_tuple_list(all_url)
        if dupl_in_urls:
            print('urls duplicates:')
            for u, n in dupl_in_urls:
                print('%-50s %s' % (u, n))
        if dupl_in_name:
            print('name duplicates:')
            for u, n in dupl_in_name:
                print('%-50s %s' % (u, n))
        self.assertEqual(len(dupl_in_name), 0, 'Виявлено дублікати в назвах url')
        self.assertEqual(len(dupl_in_urls), 0, 'Виявлено дублікати в шаблонах url')


