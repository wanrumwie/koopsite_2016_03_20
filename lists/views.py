from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
    template_name = 'home.html'
    all = List.objects.all()
    print('home_page(request):-----------')
    print('List.objects.all() =', all)
    for l in all: print('list_ =', l)
    return render(request, template_name)

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    data = {
            'list': list_,
            'items': items,
            }
    return render(request, 'list.html', data)

def new_list(request):
    # list_ = List().save()
    list_ = List.objects.create()
    item_text = request.POST.get('item_text', '')
    Item.objects.create(text=item_text, list=list_)
    return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    item_text = request.POST.get('item_text', '')
    Item.objects.create(text=item_text, list=list_)
    return redirect('/lists/%d/' % (list_.id,))
