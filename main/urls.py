from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('products', views.products),
    path('courier', views.couriers),
    path('courier/busy', views.busy),
    path('courier/free', views.free),
    path('courier/add', views.couriers_add),
    path('delivery', views.delivery),
    path('delivery/in_procces', views.d_in_procces),
    path('delivery/allready', views.d_allready),
    path('delivery/dell/<str:d_id>', views.delivery_dell),
    path('parser', views.parsing),
    path('generate_order', views.generate_order),
    path('cour/<str:cour_id>', views.cour),
    path('cour/<str:cour_id>/<str:d_id>', views.cour_take),
    path('cour/already/<str:cour_id>/<str:d_id>', views.cour_already)
]
