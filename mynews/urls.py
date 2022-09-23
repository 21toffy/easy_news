from django.urls import path
from .views import (
    ItemDetailView,
    ItemList,
)
urlpatterns = [
    path('items-list', ItemList.as_view(), name='item_list'),
    path('<uuid:pk>', ItemDetailView.as_view(), name = 'item-detail') ,
]
