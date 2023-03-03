from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.WatchListView.as_view(), name='movies-list'),
    path('<int:pk>', views.WatchListDetail.as_view(), name='movie_details'),

    path('list-platforms/', views.StreamPlaformList.as_view(), name='platforms-list'),
    path('stream/<int:pk>', views.StreamPlatformDetail.as_view(), name='stream-details'),
    path('stream/<int:pk>/reviews', views.ReviewListCreate.as_view(), name='reviews-by-stream'),
    # path('reviews/', views.ReviewListCreate.as_view(), name='reviews'),
    path('reviews/<int:pk>', views.ReviewDetail.as_view(), name='review-detail')
]