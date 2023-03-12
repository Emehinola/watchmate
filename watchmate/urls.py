from django.contrib import admin
from django.urls import path, include
from watchlist import urls
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('watch/', include('watchlist.urls'),),
    path('account/', include('account.api.urls'),),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api-auth', include('rest_framework.urls'))
]
