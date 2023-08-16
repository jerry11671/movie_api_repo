from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


# This is for the use of validators
# def length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name should exceed two characters!")

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ('watchlist',)
    
class WatchListSerializer(serializers.ModelSerializer):
    # len_name = serializers.SerializerMethodField()
    # description_style = serializers.SerializerMethodField()
    platform = serializers.CharField(source='platform.name')
    # reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = WatchList
        fields = '__all__'
        # exclude = ['id']
        
    # def validate_description(self, value):
    #     if not str(value).islower():
    #         raise serializers.ValidationError("Description should be lower case only!!")
    #     else:
    #         return value
        
    # def get_len_name(self, object):
    #     return len(object.name)
    
class StreamPlatformSerializer(serializers.ModelSerializer):
    # watchlist = serializers.StringRelatedField(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedIdentityField(
    #     many=True,
    #     read_only=True,
    #     view_name = 'streamplatform-detail',
    # )
    
    watchlist = WatchListSerializer(read_only=True, many=True)
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'
            

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#        return Movie.objects.create(**validated_data)
   
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     # def validate_name(self, value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name must exceed two characters!!")
#     #     else:
#     #         return value
        
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and description should be different!!")
#         else:
#             return data