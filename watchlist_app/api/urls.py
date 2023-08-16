from django.urls import path, include 
from . import views
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('', include(router.urls)),
    # path('list/', views.movie_list, name='movie-list'),
    # path('<str:pk>/', views.movie_detail, name='movie-detail'),
    # path('list/', views.WatchListAPIView.as_view(), name='movie-list'),
    
    # path('streams/', views.StreamPlatformListAPIView.as_view(), name='stream'),
    
    path('<str:pk>/', views.WatchDetailAPIView.as_view(), name='movie-detail'),
    # path('stream/<str:pk>/', views.StreamingPlatformDetailAPIView.as_view(), name='streamplatform-detail'),
    
    path('reviews/', views.ReviewList.as_view(), name='reviews-list'),
    # path('review/<int:pk>', views.ReviewDetail.as_view(), name='review_detail'),
    
    path('review/<str:username>/', views.UserReview.as_view(), name='user_review_list'),
    path('list', views.WatchlistGV.as_view(), name='list'),
    
    path('<int:pk>/review-create', views.ReviewCreate.as_view(), name='review_create'),
    path('review/<int:pk>', views.ReviewDetail.as_view(), name='review_detail'),
    path('<int:pk>/review/', views.ReviewList.as_view(), name='review_list')
]
