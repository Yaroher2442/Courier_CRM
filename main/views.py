import zlib
import random
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .parser import Pars_Worker
from .models import Products, Couriers, Delivery
from .forms import add_courier, generate, search


def index(request):
    return render(request, 'main/admin/index.html')


@csrf_exempt
def products(request):
    if request.method == 'POST':
        form = search(request.POST)
        if form.is_valid():
            context = {'data': [Products.objects.get(hash=form.cleaned_data['hash'])]}
            return render(request, 'main/admin/products.html', context=context)
    else:
        context = {'data': Products.objects.all(), 'form': search()}
        return render(request, 'main/admin/products.html', context=context)


def delivery(request):
    context = {'data': Delivery.objects.all()}
    return render(request, 'main/admin/delivery.html', context=context)

def d_in_procces(request):
    context = {'data': Delivery.objects.filter(status='at_the_courier')}
    return render(request, 'main/admin/delivery.html', context=context)
def d_allready(request):
    context = {'data': Delivery.objects.filter(status='already_delivered')}
    return render(request, 'main/admin/delivery.html', context=context)

def delivery_dell(request,d_id):
    d=Delivery.objects.get(id=d_id).delete()
    return HttpResponseRedirect('/delivery')

@csrf_exempt
def generate_order(request):
    if request.method == 'POST':
        form = generate(request.POST)
        if form.is_valid():
            PR = Products.objects.all()
            prods=[]
            rang=random.randrange(6)
            for ran in range(rang):
                prods.append(Products.objects.get(id=random.randint(1, len(PR))).hash)
            Delivery(**form.cleaned_data, status='ready_for_delivery', products=prods).save()
            return HttpResponseRedirect('/delivery')
    else:
        context = {'generate': generate()}
        return render(request, 'main/admin/generate_order.html', context=context)


def couriers(request):
    context = {'data': Couriers.objects.all()}
    return render(request, 'main/admin/courier.html', context=context)


def busy(request):
    context = {'data': Couriers.objects.filter(is_busy=True)}
    return render(request, 'main/admin/courier.html', context=context)


def free(request):
    context = {'data': Couriers.objects.filter(is_busy=False)}
    return render(request, 'main/admin/courier.html', context=context)


@csrf_exempt
def couriers_add(request):
    if request.method == 'POST':
        form = add_courier(request.POST)
        if form.is_valid():
            Couriers(number=zlib.crc32(form.cleaned_data['name'].encode()),
                     **form.cleaned_data, is_busy=False, way='').save()
            return HttpResponseRedirect('/courier')
    else:
        context = {'add_courier': add_courier()}
        return render(request, 'main/admin/add_courier.html', context=context)


def cour(request, cour_id):
    context = {'cour_number': cour_id, 'data': Delivery.objects.filter(status='ready_for_delivery')}
    return render(request, 'main/courier_api/index.html', context=context)


def cour_take(request, cour_id, d_id):
    dell = Delivery.objects.get(id=d_id)
    dell.status = 'at_the_courier'
    dell.courier = cour_id
    cour = Couriers.objects.get(number=cour_id)
    cour.is_busy = True
    cour.way = dell.addres
    cour.save()
    dell.save()
    context = {'data': Delivery.objects.get(courier=cour_id, status='at_the_courier'),
               'cour_id': cour_id}
    return render(request, 'main/courier_api/procces.html', context=context)


def cour_already(request, cour_id, d_id):
    dell = Delivery.objects.get(id=d_id)
    dell.status = 'already_delivered'
    dell.save()
    cour = Couriers.objects.get(number=cour_id)
    cour.is_busy = False
    cour.way=''
    cour.save()
    return HttpResponseRedirect(f'/cour/{cour_id}')


def parsing(request):
    worker = Pars_Worker()
    worker.setDaemon(True)
    worker.start()
    return render(request, 'main/admin/index.html')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return HttpResponse("You're logged in.")
        else:
            return HttpResponse("Please enable cookies and try again.")
    request.session.set_test_cookie()
    return render(request, 'main/index.html')
