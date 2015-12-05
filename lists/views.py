from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request):
    template_name = 'home.html'
    return render(request, template_name, {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list': list_, 'error': error})


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
    return redirect(list_)

