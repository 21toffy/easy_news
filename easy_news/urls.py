
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('item/', include('mynews.urls')),
    path('api/', include('mynews.apis.urls')),
]
