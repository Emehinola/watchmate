from django.shortcuts import render
from .models import WatchList, StreamPlatform, Review
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializer import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from .permissions import IsAdminOrReadOnly, IsOwner
from .throttling import WatchlistThrottle


# Create your views here.


# class based views

class ReviewDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwner]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ReviewListCreate(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        reviews = Review.objects.filter(watchlist=self.kwargs.get('pk'))

        return reviews  # Response(data=serializer.data) # self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            movie = WatchList.objects.get(pk=self.kwargs.get('pk'))
        except WatchList.DoesNotExist:
            raise ValidationError("Movie does not exist")
        
        user = User.objects.get(id=self.request.user.id)

        return serializer.save(watchlist=movie, user=user)

    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# using view set
class StreamPlatformView(viewsets.ViewSet):

    permission_classes = [IsAdminOrReadOnly]
    
    def list(self, request):
        streams = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(streams, many=True, context={'request': request})

        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all() # gets all streams
        stream = get_object_or_404(queryset, pk=pk) # gets stream by pk(id) or return 404 where not found

        serializer = StreamPlatformSerializer(stream, context={'request': request})

        return Response(serializer.data)
    
    def create(self, request):
        serializer = StreamPlatformSerializer(data=request.data, context={'request': request})

        if(serializer.is_valid()):
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def update(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data, context={'request': request})

        if(serializer.is_valid()):
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlaformList(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platforms = StreamPlatform.objects.all()

        serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})

        return Response(data=serializer.data)

    def post(self, request):
        
        serializer = StreamPlatformSerializer(data=request.data, context={'request': request})

        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatformDetail(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Platform not found'})

        serializer = StreamPlatformSerializer(platform, context={'request': request})

        return Response(data=serializer.data)

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Platform not found'})

        serializer = StreamPlatformSerializer(platform, data=request.data)

        if (serializer.is_valid()):
            serializer.save()

            return Response(data=serializer.data)

        return Response(serializer.errors)

    def delete(request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Platform not found'})

        serializer = StreamPlatformSerializer(platform)

        serializer.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)



class WatchListView(APIView):

    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [WatchlistThrottle]  # [ScopedRateThrottle]
    # throttle_scope = 'watchlist'

    def get(self, request):
        movies = WatchList.objects.all()

        serializer = WatchListSerializer(movies, many=True)

        return Response(data=serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)

        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchListDetail(APIView):

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):

        try:
            movie = WatchList.objects.get(pk=pk)

        except WatchList.DoesNotExist:
            return Response({'error': "WatchList not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie)

        return Response(data=serializer.data)

    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)

        except WatchList.DoesNotExist:
            return Response({'error': "WatchList not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie, data=request.data)

        if (serializer.is_valid()):
            serializer.save()

            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)

        except WatchList.DoesNotExist:
            return Response({'error': "WatchList not found"}, status=status.HTTP_404_NOT_FOUND)

        watchlist.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# function based views

@api_view(['GET', 'POST', ])
@permission_classes((IsAdminOrReadOnly,))
def movies_list(request):
    if (request.method == 'GET'):
        movies = WatchList.objects.all()

        serializer = WatchListSerializer(movies, many=True)

        return Response(data=serializer.data)

    elif request.method == 'POST':  # POST request
        serializer = WatchListSerializer(data=request.data)

        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    return Response(data={'errors': 'Something went wrong'})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAdminOrReadOnly,))
def WatchList_details(request, pk):
    try:
        movie = WatchList.objects.get(pk=pk)

    except WatchList.DoesNotExist:
        return Response({'error': "WatchList not found"}, status=status.HTTP_404_NOT_FOUND)

    if (request.method == 'GET'):

        serializer = WatchListSerializer(movie)

        return Response(data=serializer.data)

    elif request.method == 'PUT':
        serializer = WatchListSerializer(movie, data=request.data)

        if (serializer.is_valid()):
            serializer.save()

            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)

    elif request.method == 'DELETE':
        WatchList.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(data={'errors': 'Something went wrong'})
