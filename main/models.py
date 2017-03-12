"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# Create your models here.
#https://docs.python.org/2/tutorial/classes.html


text_markdown = "text/markdown"
text_plain = "text/plain"
binary = "application/base64"
png = "image/png;base64"
jpeg = "image/jpeg;base64 "

contentchoices = (
        (text_markdown, 'Public'),
        (text_plain, 'Friend of a Friend'),
        (binary,'Friends only'),
        (png, 'Private'),
        (jpeg, 'Server Only'),

    )


class author(models.Model):
    #https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    user = models.OneToOneField(User)
    host = models.CharField(max_length=200)
    url = models.URLField(max_length=400)
    github = models.URLField(max_length=400)
    bio = models.CharField(max_length=1000)

    #https://docs.djangoproject.com/en/1.10/ref/models/fields/
    #http://stackoverflow.com/questions/1110153/what-is-the-most-efficent-way-to-store-a-list-in-the-django-models






class category(models.Model):
    categoryname=models.CharField(max_length=200,unique=True)

        


class comment(models.Model):
    #https://docs.djangoproject.com/en/1.10/topics/db/examples/many_to_one/
    authorid= models.ForeignKey(author, on_delete=models.CASCADE)
    #http://stackoverflow.com/questions/17658641/django-says-my-model-is-not-defined
    postid= models.ForeignKey('posts', on_delete=models.CASCADE)
    published = models.DateTimeField()
    content= models.CharField(max_length=200)
    contentType= models.CharField(
        max_length=50,
        choices=contentchoices,
        default=text_plain,
    )


class posts(models.Model):
    title = models.CharField(max_length=200)
    source = models.URLField(max_length=400)
    origin = models.URLField(max_length=400)
    description = models.CharField(max_length=1000)
    contentType = models.CharField(
        max_length=50,
        choices=contentchoices,
        default=text_plain,
    )

    content = models.BinaryField(max_length=10000)
    # securitylevel
    # 5 another user with author_id can read it
    # 4 all my friends can read it
    # 3 all my friends of friends can read it 
    # 2 only friends on my host can read it
    # 1 everyone can read it
    #https://docs.djangoproject.com/en/1.10/ref/models/fields/
    pub = "PUBLIC"
    foaf = "FOAF"
    friends = "FRIENDS"
    private = "PRIVATE"
    servonly = "SERVERONLY"

    vischoices = (
        (pub, 'Public'),
        (foaf, 'Friend of a Friend'),
        (friends,'Friends only'),
        (private, 'Private'),
        (servonly, 'Server Only'),

    )
    visibility = models.CharField(
        max_length=50,
        choices=vischoices,
        default=friends,
    )

    authorid = models.UUIDField(max_length=400)
    #https://docs.djangoproject.com/en/1.10/topics/db/examples/many_to_many/
    categories = models.ManyToManyField(category)
    comments = models.ManyToManyField(comment)
    published = models.DateTimeField()
    visibleTo = models.ManyToManyField(author)
    unlisted = models.BooleanField()


class friends(models.Models):
    auth = models.ManytoManyField(author)       