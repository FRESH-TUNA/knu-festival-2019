from django.contrib import admin
from django.urls import path, include
import index.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.views.index, name='index'),
    path('index/', include('index.urls')),
    path('foodtruck/', include('foodtruck.urls'),),
    path('lostboard/', include('lostboard.urls')),
    path('friendboard/', include('friendboard.urls')),
    path('qnaknuch/', include('qnaknuch.urls')),
] 