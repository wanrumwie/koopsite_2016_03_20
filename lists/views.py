from django.shortcuts import render, redirect
from lists.forms import ItemForm, ExistingListItemForm
from lists.models import Item, List


def home_page(request):
    template_name = 'home.html'
    return render(request, template_name, {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})


# lists = List.objects.all()
# items = Item.objects.all()
# print('lists:')
# for l in lists:
#     print('%5s  %s' % (l.id, l.list))
# print('items:')
# for i in items:
#     s = i.list_id or "-"
#     print('%5s %-40s %s' % (i.id, i.text, s))
#
# i = Item.objects.get(id=6)
# s = i.list_id or "-"
# print('%5s %-40s %s' % (i.id, i.text, s))
# i.delete()

