from django.contrib import admin
from django.urls import path, include
from watchlist import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('watch/', include('watchlist.urls'),),
    path('account/', include('account.api.urls'),),
    # path('api-auth', include('rest_framework.urls'))
]
