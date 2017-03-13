from rest_framework import serializers
from .models import *




#http://stackoverflow.com/questions/18517438/django-rest-framework-make-onetoone-relation-ship-feel-like-it-is-one-model

"""
    host = models.CharField(max_length=200)
    github = models.URLField(max_length=400)
    bio = models.CharField(max_length=1000)

 """
#class UserSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = User
#        fields = ('url', 'username', 'first_name', 'last_name', 'email',)


#class authorSerializer(serializers.HyperlinkedModelSerializer):



class authorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='authorid')
    
    class Meta:
        model = author
        fields = ('id','url','host','displayName','github',)

class categorySerializer(serializers.ModelSerializer):

    class Meta:
        model = category
        fields = ('categoryname',)






#http://stackoverflow.com/questions/17280007/retrieving-a-foreign-key-value-with-django-rest-framework-serializers
class commentSerializer(serializers.ModelSerializer):
    author = authorSerializer(source='author.authorid',read_only=True)
    postid = serializers.PrimaryKeyRelatedField(many=False, read_only=True)


    contentType = serializers.ChoiceField(choices=contentchoices)
    class Meta:
        model = comment
        fields = ('author', 'postid', 'published','content','commentid','contentType',)


#http://stackoverflow.com/questions/37828358/manytomany-with-django-rest-framework


class postSerializer(serializers.ModelSerializer):
    author = authorSerializer(source='authorid',read_only=True )
    contentType = serializers.ChoiceField(choices=contentchoices)
    visibility = serializers.ChoiceField(choices=post.vischoices)
    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='categoryname'
     )

    comments = commentSerializer(many=True)
    visibleTo = authorSerializer(many=True)

    class Meta:
        model = post
        fields = ('title','source','origin','source','description','contentType','content','author','categories','visibility','comments','published','postid','visibleTo','unlisted',)





class friendSerializer(serializers.ModelSerializer):
    author1 = serializers.URLField(source='authorid1.url',read_only=True)
    author2 = serializers.URLField(source='authorid2.url',read_only=True)
    class Meta:
        model = friend
        fields =('author1','author2')
        #fields = "__all__"