from django.urls import path
from . import views

urlpatterns = [
  path('place_order/', views.place_order, name='place_order'),
  path('payments/', views.payments, name='payments'),
  
  path("cash_on_delivery/<int:id>",views.cash_on_delivery,name='cash_on_delivery'),
  
  path("cancel_order/<int:id>",views.cancel_order,name='cancel_order'),
]