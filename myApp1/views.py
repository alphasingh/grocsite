from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .forms import BurgerForm
from .models import Type, Item


# Create your views here.
# books=[
#     {
#         'author': 'Usama',
#         'title':'Intro to Django',
#         'date':'March 01, 2022'
#     },
#     {
#         'author': 'Rahul',
#         'title':'Intro to Mental Strength',
#         'date':'March 01, 2022'
#     }
# ]
def index(request):
    # type_list = Type.objects.all().order_by('id')
    item_list = Item.objects.all().order_by('-price')[:7]
    response = HttpResponse()
    heading1 = '<p>' + 'Different Items (sorted by price, limited to top 7 most expensive items): ' + '</p>'
    response.write(heading1)
    for item in item_list:
        para = '<p> $' + str(item.price) + ' ' + str(item) + '</p>'
        response.write(para)
    return response


# def index(request):
#     context={
#         'books':books
#     }
#     #return HttpResponseBadRequest()
#     return render(request, 'dummy/index.html', context)

def about(request):
    # return HttpResponse('This is the about page')
    return render(request, 'myApp1/about.html')


def detail(request, type_no):
    type_with_id = get_object_or_404(Type, pk=type_no)
    # type_with_id = Type.objects.get(id=type_no)
    items_with_type = Item.objects.filter(type=type_with_id)
    response = HttpResponse()
    heading1 = '<p>' + 'Different Items with type: ' + str(type_with_id) + '</p>'
    response.write(heading1)
    for item in items_with_type:
        para = '<p>' + str(item.price) + ': ' + str(item) + '</p>'
        response.write(para)
    return response


def order(request):
    if request.method == 'POST':
        filled_form = BurgerForm(request.POST)
        note = 'Valid order' if filled_form.is_valid() else 'Invalid order'
        return render(request, 'myApp1/order.html', {'filled': BurgerForm(), 'note': note})
    else:
        form = BurgerForm()
        return render(request, 'myApp1/order.html', {'filled': form})
