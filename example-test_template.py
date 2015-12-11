from django.template import Context
from django.template.base import TextNode
from django.template.defaulttags import IfNode
from django.template.loader import get_template
from django.template.loader_tags import BlockNode, ExtendsNode
'''
def _get_node(template, context=Context(), name='subject'):
    for node in template:
        if isinstance(node, BlockNode) and node.name == name:
            return node.render(context)
        elif isinstance(node, ExtendsNode):
            return _get_node(node.nodelist, context, name)
    raise Exception("Node '%s' could not be found in template." % name)
'''

def show_node(node, indent=0):
    print('   '*indent, type(node))


def list_node(template, indent=0):
    for node in template:
        show_node(node, indent)
        child_nodelists = []
        nodelists = []
        if hasattr(node, '__dict__'):
            for k in node.__dict__:
                print('   '*indent,' ', k)
        # else:
        #     print('   '*indent,' ', "object has no attribute '__dict__'")
        print('   '*indent,' ', '-'*40)
        if isinstance(node, str):
            s = str(node)
            s = s.replace(r'\n', " ")
            print('   '*indent,' ', s)
        if isinstance(node, TextNode):
            s = str(node.s)
            s = s.replace(r'\n', " ")
            print('   '*indent,' ', s)
            child_nodelists = node.child_nodelists
        if isinstance(node, BlockNode):
            nodelists = node.nodelist
            child_nodelists = node.child_nodelists
        if child_nodelists:
            print('   '*indent,' ', 'child_nodelist:', len(child_nodelists))
            # for child in child_nodelists:
            #     list_node(child, indent + 1)
            print('   '*indent,' ', '-'*40)
        if nodelists:
            print('   '*indent,' ', 'nodelist:')
            for child in nodelists:
                list_node(child, indent + 1)
        print('   '*indent, '-'*40)


# template_name = 'koop_index.html'
template_name = 'koop_base.html'
t = get_template(template_name).template

def example():
    ntypes = set()
    for node in t.nodelist:
        # print('-'*80)
        print(type(node))
        ntypes.add(type(node))
        # print(node)

    print('-'*40)
        # print(node.__dict__)
        # for k in node.__dict__:
        #     print(k)
        # print('-'*40)
        # for k in node.__dict__:
        #     print('-'*23)
        #     print('%-20s : %s' % (k, getattr(node, k)))
    for nt in ntypes:
        print(nt)

example()
# list_node(t)

