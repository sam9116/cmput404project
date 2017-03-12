from rest_framework import serializers
from .models import *




#http://stackoverflow.com/questions/18517438/django-rest-framework-make-onetoone-relation-ship-feel-like-it-is-one-model

"""
    host = models.CharField(max_length=200)
    github = models.URLField(max_length=400)
    bio = models.CharField(max_length=1000)

 """
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email')

class authorSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.CharField(source='user.url')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = author
        fields = ('url', 'username', 'first_name', 'last_name', 'email', 'host','github','bio')



class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = {'categoryname'}


#http://stackoverflow.com/questions/17280007/retrieving-a-foreign-key-value-with-django-rest-framework-serializers
class commentSerializer(serializers.ModelSerializer):
    authorid = serializers.RelatedField(source='author')
    postid = serializers.RelatedField(source='posts')
    contentType = serializers.ChoiceField(choices=model.contentchoices)
    class Meta:
        model = comment
        fields = ('authorid', 'postid', 'published','content','contentType')


#http://stackoverflow.com/questions/37828358/manytomany-with-django-rest-framework

class postSerializer(serializers.ModelSerializer):
    authorid = serializers.RelatedField(source='author', )
    contentType = serializers.ChoiceField(choices=model.contentchoices)
    visibility = serializers.ChoiceField(choices=posts.vischoices)
    categories = categorySerializer(many=True)
    comments = commentSerializer(many=True)
    visibleTo = authorSerializer(many=True)

    class Meta:
        model = posts

        fields = {'title','source','origin','source','descriptions','contentType','visibility','authorid','categories','comments','published','visibleTo','unlisted'}



class friendSerializer(serializers.ModelSerializer):
    authors = authorSerializer(many=True)
    
    class Meta:
        model = posts
        fields ={'authors'}
