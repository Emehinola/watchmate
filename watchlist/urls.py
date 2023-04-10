from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import StreamPlatformView

router = DefaultRouter()
router.register('stream', StreamPlatformView, basename='streamplatform',)

urlpatterns = [
    path('list/', views.WatchListView.as_view(), name='movies-list'),
    path('list-filter/', views.SearchMoviewList.as_view(), name='movies-list-filter'),
    path('<int:pk>/', views.WatchListDetail.as_view(), name='movie_details'),
    path('', include(router.urls)),
    # path('stream/', views.StreamPlaformList.as_view(), name='stream-list'),
    # path('stream/<int:pk>/', views.StreamPlatformDetail.as_view(), name='stream-details'),
    path('<int:pk>/reviews/', views.ReviewListCreate.as_view(), name='reviews-by-stream'),
    path('reviews/', views.ReviewListCreate.as_view(), name='reviews'),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),
    path('reviews-filter/', views.FilterReview.as_view(), name='review-filter')
]