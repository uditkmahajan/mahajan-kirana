from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('itsmeudit/', admin.site.urls),
    path('api/user/', include('User.api.urls'), name = "adding all the urls of the User"),
    path('api/app/', include('app.api.urls'), name = "adding the urls of the app"),
    path('api/', include('product.api.urls'), name = "adding the urls for product"),
    path('api/', include('order.api.urls'), name = "adding the urls of the order"),
    # path('api/apniDukan/', include('dukandar.api.urls', name = 'adding the urls of dukandar')),
    # path('', views.index, name = 'main index file')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
