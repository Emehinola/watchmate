from rest_framework import serializers
from . models import StreamPlatform, WatchList, Review

def validate_length(value):
    if len(value) < 5:
        raise serializers.ValidationError("Name is too short")

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class WatchListSerializer(serializers.ModelSerializer):
    length_of_title = serializers.SerializerMethodField()
    platform_name = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = '__all__'  #['id', 'name', 'description',] # exclude active field

    def get_length_of_title(self, instance):
        length = len(instance.title)

        return length

    def get_platform_name(self, instance):
        platform = StreamPlatform.objects.get(id=instance.platform.id)

        return platform.name

    # create movie
    def create(self, validated_date):
        return WatchList.objects.create(**validated_date)

    # update
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
 
        instance.save() # saves
        return instance
    
    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError("Name and description can't have the same value")
        
        return data

    # def validate_name(self, data):
    #     if len(data) < 5:
    #         raise serializers.ValidationError("Name is too short")
    #     else:
    #         return data


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie_details'
    # )


    class Meta:
        model = StreamPlatform
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'platform-details'}
        }
