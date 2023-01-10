from django.shortcuts import render
from .models import WatchList, StreamPlatform, Review
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from . serializer import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.views import APIView
from rest_framework import mixins, generics
# Create your views here.



# class based views

class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class ReviewListCreate(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class StreamPlaformList(APIView):
    def get(self, request):
        platforms = StreamPlatform.objects.all()

        serializer = StreamPlatformSerializer(platforms, many=True, context = {'request': request})

        return Response(data=serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data, context = {'request': request})

        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetail(APIView):
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Platform not found'})

        serializer = StreamPlatformSerializer(platform, context = {'request': request})

        return Response(data=serializer.data)

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Platform not found'})

        serializer = StreamPlatformSerializer(platform, data=request.data)

        if(serializer.is_valid()):
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

    def get(self, request):
        movies = WatchList.objects.all()

        serializer = WatchListSerializer(movies, many=True)

        return Response(data=serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)

        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchListDetail(APIView):
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

        serializer = WatchListSerializer(movie,data=request.data)

        if(serializer.is_valid()):
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

@api_view(['GET', 'POST',])
def movies_list(request):
    if(request.method == 'GET'):
        movies = WatchList.objects.all()

        serializer = WatchListSerializer(movies, many=True)

        return Response(data=serializer.data)

    elif request.method == 'POST': # POST request
        serializer = WatchListSerializer(data=request.data)

        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    return Response(data={'errors': 'Something went wrong'})


@api_view(['GET' ,'PUT', 'DELETE'])
def WatchList_details(request, pk):

    try:
        movie = WatchList.objects.get(pk=pk)
    
    except WatchList.DoesNotExist:
        return Response({'error': "WatchList not found"}, status=status.HTTP_404_NOT_FOUND)

    if(request.method == 'GET'):

        serializer = WatchListSerializer(movie)

        return Response(data=serializer.data)

    elif request.method == 'PUT':
        serializer = WatchListSerializer(movie,data=request.data)

        if(serializer.is_valid()):
            serializer.save()

            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)
        
    elif request.method == 'DELETE':
        WatchList.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(data={'errors': 'Something went wrong'})