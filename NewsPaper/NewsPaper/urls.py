from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('accounts/', include('allauth.urls')),
   # path('appointments/', include(('appointment.urls', 'appointments'), namespace='appointments')),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('', include('news.urls')),
   path('sign/', include('sign.urls'))
]
