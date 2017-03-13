from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from linknot_services import *
from django.contrib.auth.models import User
from rest_framework import permissions,authentication
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import *
from linknot_security import *
from datetime import datetime
from django.db.models import Q
import json
from collections import OrderedDict














class custom(LimitOffsetPagination):
    limit_query_param = 'size'
    offset_query_param = 'page'


#http://www.django-rest-framework.org/api-guide/pagination/#custom-pagination-styles

def register(request):
    """ registers new user"""
    assert isinstance(request,HttpRequest)
    return render(request,
        'register.html',
        {
            'title':'Please Register',
            'message':'You need to register before using our service',
            'year':datetime.now().year,
        })



def linknothome(request):
    """ homepage of linknot"""
    assert isinstance(request,HttpRequest)
    if not request.user.is_authenticated:
       return redirect('/login/')
    else:
       return render(request,
        'linknot_home.html',
        {
            'title':'Welcome',
            'username':request.user.username,
            'message':'Your Feed',
            'year':datetime.now().year,
        })

def login_user(request):
    """login for users"""
    #todo check csrf token
    assert isinstance(request,HttpRequest)
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    #http://cheng.logdown.com/posts/2016/01/06/django-create-and-login-user-manually



    if user is not None:
    # A backend authenticated the credentials
        login(request, user)
        return redirect('/')
    else:
        return render(request,
                      'login.html',
                      {
                      'title':'login',
                      'message':'Login please',
                      'year':datetime.now().year,
                      })

#http://stackoverflow.com/questions/38301628/attributeerror-object-has-no-attribute-page-drf-pagination


class singlepost(GenericAPIView):

    
     serializer_class = postSerializer
     permission_classes = (specialpermission,)
     queryset = post.objects.all()



     def get(self, request,pk, format=None):
        try:
            spost = post.objects.get(pk=pk)
        except spost.DoesNotExist:
            return HttpResponse(status=404)
        


        serializer = postSerializer(spost)

        return JsonResponse(serializer.data)

        #print(str(spost.authorid))
     def get_object(self):
         obj = get_object_or_404(self.get_queryset())
         self.check_object_permissions(self.request, obj)
         return obj








class friendlist(GenericAPIView):

    
     serializer_class = friendSerializer
     queryset = friend.objects.all()


     #http://stackoverflow.com/questions/14190140/merge-querysets-in-django

     def get(self, request,pk, format=None):

        

            friendslist = friend.objects.filter(Q(authorid1__url__contains=pk) | Q(authorid2__url__contains=pk))

            serializer = friendSerializer(friendslist,many=True)

            print(str(friendslist))

            return JsonResponse(OrderedDict([('query', 'friends'),
            ('authors', serializer.data)]))

            #return JsonResponse(serializer.data)


class friends(GenericAPIView):

    
     serializer_class = friendSerializer
     queryset = friend.objects.all()


     #http://stackoverflow.com/questions/14190140/merge-querysets-in-django

     def get(self, request,pk1,pk2, format=None):

            author1 = author.object.get(authorid=pk1)
            author2 = author.object.get(authorid=pk2)

            friendslist = friend.objects.filter(Q(authorid1__url__contains=pk1) | Q(authorid2__url__contains=pk2))

            friendslist1 = friend.objects.filter(Q(authorid1__url__contains=pk2) | Q(authorid2__url__contains=pk1))

            allposibilities = list(chain(friendslist, friendslist1))

            serializer = friendSerializer(allposibilities,many=True)
            
            decision = False

            if(len(allposibilities) > 0):
                decision = True

           

            return JsonResponse(OrderedDict([('query', 'friends'),

            ('friends', {author1,author2})('friends',str(decision))]))

            #return JsonResponse(serializer.data)



class Listposts(APIView):
    
    
    pagination_class = LimitOffsetPagination
    queryset = post.objects.all()

    @csrf_exempt
    #http://stackoverflow.com/questions/21035273/drf-method-get-not-allowed
    def get(self, request):
        """
        List all code snippets, or create a new snippet.
        """
       
        posts = post.objects.filter(unlisted=False,visibility="PUBLIC")

        page = self.request.GET.get('page', 1)
        page_num = self.request.GET.get('size', 1000)
        
        paginator = custom()
        results = paginator.paginate_queryset(posts,request)
        serializer = postSerializer(results, many=True)
        #return JsonResponse(serializer.data,safe=False)
        #http://stackoverflow.com/questions/34798703/creating-utf-8-jsonresponse-in-django
        #return JsonResponse(json.dumps(serializer.data, ensure_ascii=False),
        #safe=False)


        return JsonResponse(OrderedDict([('count', paginator.count),
            ('current', page),
            ('next', paginator.get_next_link()),
            ('previous', paginator.get_previous_link()),
            ('size', page_num),
            ('posts', serializer.data)]))

      





            #data = JSONParser().parse(request)
            #serializer = postSerializer(data=data)
            #if serializer.is_valid():
             #   serializer.save()
              #  return JsonResponse(serializer.data, status=201)
        #return JsonResponse(serializer.errors, status=400)

#@csrf_exempt
#def post_detail(request, pk):
#   """
#    Retrieve, update or delete a code snippet.
#    """
#    try:
#        singlepost = post.objects.get(pk=pk)
#    except singlepost.DoesNotExist:
#        return HttpResponse(status=404)
#
#    if request.method == 'GET':
#        serializer = postSerializer(singlepost)
#        return JsonResponse(serializer.data)
#
#    elif request.method == 'PUT':
#        data = JSONParser().parse(request)
#        serializer = postSerializer(singlepost, data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data)
#        return JsonResponse(serializer.errors, status=400)
#
#    elif request.method == 'DELETE':
#        singlepost.delete()
#        return HttpResponse(status=204)


