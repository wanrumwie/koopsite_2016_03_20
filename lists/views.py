from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
    template_name = 'home.html'
    all = List.objects.all()
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
    list_ = List.objects.create()
    item_text = request.POST.get('item_text', '')
    item = Item.objects.create(text=item_text, list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    item_text = request.POST.get('item_text', '')
    Item.objects.create(text=item_text, list=list_)
    return redirect('/lists/%d/' % (list_.id,))
