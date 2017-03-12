"""
Definition of models.
"""

from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.


#https://docs.python.org/2/tutorial/classes.html
class author(object):
   
    def __init__(self,userid,displayname,host,github):
        self.uuid=userid
        self.displayname=display
        self.host=host
        self.url=self.url+'/author/'+self.id()
        self.github=github


    def update_displayname(self,newname):
        self.displayname = newname

    def update_github(self,newgithub):
        self.displayname = newgithub

class permission(object):
    #securitylevel
    # 1 only I can read it
    # 2 another user with author_id can read it
    # 3 all my friends can read it
    # 4 all my friends of friends can read it 
    # 5 only friends on my host can read it
    # 6 everyone can read it
    def __init__(self):
        self.securitylevel = 1

    def update_securitylevel(imonanewlevel):
        self.secuirtylevel = imonanewlevel
    

class posts(object):
    def __init__(self):
        self.title = ''
        self.source = ''
        self.origin = ''
        self.description = ''
        self.contentType=''
        self.securitylevel=''

        