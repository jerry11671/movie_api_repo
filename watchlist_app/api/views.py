from django.shortcuts import get_object_or_404

from watchlist_app.models import WatchList, StreamPlatform, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets

from rest_framework.exceptions import ValidationError

from rest_framework.permissions import IsAuthenticated
# from rest_framework.throttling import ScopedRateThrottle

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from watchlist_app.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
# from watchlist_app.throttling import ReviewDetailThrottle, ReviewListThrottle


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        username = self.kwargs['username']
        # username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)
    
class IndReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = []
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'reviews'

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    

class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = []
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'reviews'

    
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        user = self.request.user
        
        review_queryset = Review.objects.filter(watchlist=movie, review_user=user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!!")
        
        if movie.avg_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = float((movie.avg_rating + serializer.validated_data['rating']) / 2)
            
        movie.num_rating = movie.num_rating + 1
        movie.save()
        
        serializer.save(watchlist=movie, review_user=user)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    # throttle_classes = [ReviewDetailThrottle]

# class ReviewList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class ReviewDetail(generics.GenericAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    

class WatchlistGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [filters.OrderingFilter]
    # filterset_fields = ['title', 'platform__name']
    # search_fields = ['title', 'avg_rating']
    ordering_fields = ['-title']

class WatchListAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    # throttle_classes = [ReviewListThrottle]

    def get(self, request):
        try:
            movies = WatchList.objects.all()
        except WatchList.DoesNotExist:
            return Response({'error':'List does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        
class WatchDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)  
    
    def put(self, request, pk):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response("Item successfully deleted!")
    
    
# class StreamPlatformVS(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors)

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
                    

# class StreamPlatformListAPIView(APIView):
    
#     def get(self, request):
#         platforms = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
# class StreamingPlatformDetailAPIView(APIView):
    
#     def get(self, request, pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(platform, context={'request': request})
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     def delete(self, request, pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         try:
#             movies = Movie.objects.all()
#         except Movie.DoesNotExist:
#             return Response({'error':'List does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, pk):
#     if request.method == 'GET':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response("Item successfully deleted!")
        