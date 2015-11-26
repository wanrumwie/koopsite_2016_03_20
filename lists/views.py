from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
    template_name = 'home.html'
    return render(request, template_name)

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    list_ = List().save()
    # list_ = List.objects.create()
    item_text = request.POST.get('item_text', '')
    Item.objects.create(text=item_text, list=list_)
    return redirect('/lists/the-only-list-in-the-world/')

