"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
import uuid

# Create your models here.
#https://docs.python.org/2/tutorial/classes.html


text_markdown = "text/markdown"
text_plain = "text/plain"
binary = "application/base64"
png = "image/png;base64"
jpeg = "image/jpeg;base64"

contentchoices = (
        (text_markdown, 'text/markdown'),
        (text_plain, 'text/plain'),
        (binary,'application/base64'),
        (png, 'image/png;base64'),
        (jpeg, 'image/jpeg;base64'),

    )


class author(models.Model):
    #https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    user = models.OneToOneField(User)
    profilepic = models.ImageField(verbose_name="Images",upload_to="upload",null=True,blank=True)
    displayName = models.CharField(max_length=200,null=True, blank=True,editable=False)
    host = models.CharField(max_length=200,null=True, blank=True)
    url = models.URLField(max_length=400,null=True, blank=True)
    github = models.URLField(max_length=400,null=True, blank=True)
    bio = models.CharField(max_length=1000,null=True, blank=True)
    authorid = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)


    #https://docs.djangoproject.com/en/1.10/ref/models/fields/
    #http://stackoverflow.com/questions/1110153/what-is-the-most-efficent-way-to-store-a-list-in-the-django-models

    def __unicode__(self):
       return str(self.user.url)

    def save(self, *args, **kwargs):

        #http://stackoverflow.com/questions/892997/how-do-i-get-the-server-name-in-django-for-a-complete-url
        self.url = str(Site.objects.get_current().domain) +"/authors/"+str(self.authorid)
        self.host = str(Site.objects.get_current().domain)
        self.displayName = str(self.user.first_name + ' ' + self.user.last_name)

        """
        automatically generate URL for all registered users
        this will need to be changed for project part 2
                
        """


        super(author, self).save(*args, **kwargs)









class category(models.Model):
    categoryname=models.CharField(max_length=200,unique=True)
    def __unicode__(self):
       return str(self.categoryname)

        


class comment(models.Model):
    #https://docs.djangoproject.com/en/1.10/topics/db/examples/many_to_one/
    authorid= models.ForeignKey(author, on_delete=models.CASCADE)
    #http://stackoverflow.com/questions/17658641/django-says-my-model-is-not-defined
    postid= models.ForeignKey('post', on_delete=models.CASCADE)
    published = models.DateTimeField()
    content= models.BinaryField(max_length=10000,null=True,blank=True)
    commentid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    contentType= models.CharField(
        max_length=50,
        choices=contentchoices,
        default=text_plain,
    )


#http://stackoverflow.com/questions/16925129/generate-unique-id-in-django-from-a-model-field
class post(models.Model):
    title = models.CharField(max_length=200)
    source = models.URLField(max_length=400,null=True,blank=True)
    origin = models.URLField(max_length=400,null=True,blank=True)
    description = models.CharField(max_length=1000)
    contentType = models.CharField(
        max_length=50,
        choices=contentchoices,
        default=text_plain,
    )

    content = models.BinaryField(max_length=10000,null=True,blank=True)
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

    authorid = models.ForeignKey(author,related_name="post_author", on_delete=models.CASCADE)
    #https://docs.djangoproject.com/en/1.10/topics/db/examples/many_to_many/
    categories = models.ManyToManyField(category)
    comments = models.ManyToManyField(comment,blank=True)
    published = models.DateTimeField()
    postid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    visibleTo = models.ManyToManyField(author,related_name="allowed_author",blank=True)
    unlisted = models.BooleanField()
    
    def __unicode__(self):
       return str(self.title)

    def save(self, *args, **kwargs):

        #http://stackoverflow.com/questions/892997/how-do-i-get-the-server-name-in-django-for-a-complete-url
        self.origin = str(Site.objects.get_current().domain) +"/posts/"+str(self.pk)

        """
        automatically generate URL for all registered users
        this will need to be changed for project part 2
                
        """


        super(post, self).save(*args, **kwargs)



class friend(models.Model):
    authorid1 = models.ForeignKey(author,related_name="sender", on_delete=models.CASCADE)   
    authorid2 = models.ForeignKey(author,related_name="receiver", on_delete=models.CASCADE)  


    class Meta:
        unique_together = ('authorid1', 'authorid2',)

    def clean(self, *args, **kwargs):
       if self.authorid1 == self.authorid2:
           raise ValidationError("you can't befriend yourself, even if you wanted")
       try:
            duplicates = friend.objects.get(authorid2=self.authorid1,authorid1=self.authorid2)
            duplicates = friend.objects.get(authorid1=self.authorid2,authorid2=self.authorid1)
            raise ValidationError("you guys are already friends")
       except friend.DoesNotExist:
            pass


       
       super(friend, self).clean(*args, **kwargs)
    def __unicode__(self):
       return str(self.authorid1.user.username) + "<>" + str(self.authorid2.user.username)