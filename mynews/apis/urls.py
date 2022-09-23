from django.urls import path

from .views import (
    ItemsListAPIView,
    ItemUpdateDeleteAPIView
)

urlpatterns = [
    path('v1/<int:pk>', ItemUpdateDeleteAPIView.as_view(), name='item_update_delete'),
    path("v1/list", ItemsListAPIView.as_view(), name="api_items_list"),
]
