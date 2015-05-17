from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.contrib import messages
import json
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from signups.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from signups.models import Incentive,Tag
from signups.serializers import IncentiveSerializer,UserSerializer
from rest_framework.decorators import detail_route
from rest_framework import renderers,permissions,status,generics, mixins
from signups.permissions import IsOwnerOrReadOnly
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from StringIO import StringIO
import urllib2,os,json,xmltodict
import xml.etree.ElementTree as ET
from rest_framework.authtoken.models import Token
import logging









# Create your views here.

from .forms import SignUpForm,IncentiveFrom


def home(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.save()
        messages.success(request,'We will be in touch')
        return HttpResponseRedirect('/thank-you/')
    return render_to_response("signups.html",locals(),context_instance=RequestContext(request)) 


def addIncentive(request):

    form = IncentiveFrom(request.POST or None)
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.save()
        messages.success(request,'Your Incentive Has been saved')
       # return HttpResponseRedirect('/thank-you/')
    return render_to_response("IncentiveForm.html",locals(),context_instance=RequestContext(request))



def thankyou(request):
    
    
    return render_to_response("thankyou.html",locals(),context_instance=RequestContext(request))


def wiki(request):


    return render_to_response("wiki.html",locals(),context_instance=RequestContext(request))


def aboutus(request):
    
    
    return render_to_response("aboutus.html",locals(),context_instance=RequestContext(request))


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        username=data[u'username']
        password=data[u'password']
        user=None
        try:
            user=User.objects.get(username=username)
        except:
            pass
        if user is not None and user.check_password(password):
            token=Token.objects.get_or_create(user=user)
            return JSONResponse("{'Token':'"+token[0].key+"'}")
    return JSONResponse("{'Token':'0'}")


from django.contrib.auth.models import User


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
import logging
logger = logging.getLogger(__name__)
    
class IncetiveViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Incentive.objects.all()
    serializer_class = IncentiveSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)


    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        incentive = self.get_object()
        return Response(incentive.highlighted)

    # def perform_create(self, serializer):
    #         serializer.save()
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def incetive_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        #incentive = Incentive.objects.all()
        staa=request.GET
        tmp = dict(staa.lists())
        token = tmp[u'Token']
        t=str(token[0])
        testToken=None
        try:
            testToken=Token.objects.get(key=token[0])
        except:
            testToken=None
        incentive=None
        if (testToken is not None):
            for key in tmp:
                if key == 'tagID':
                    tags = Tag.objects.filter(tagID=tmp[key][0])
                    incentive=Incentive.objects.filter(tags=tags)
                if key == 'status':
                    incentive = Incentive.objects.filter(status=tmp[key])
                if key == 'groupIncentive':
                    incentive = Incentive.objects.filter(groupIncentive=tmp[key])
                if key == 'typeID':
                    incentive = Incentive.objects.filter(typeID =tmp[key][0])
                if key == 'schemeID':
                    incentive = Incentive.objects.filter(schemeID=tmp[key][0])
        if incentive is None:
            return JSONResponse("{err:Wrong Argument}", status=404)
        serializer = IncentiveSerializer(incentive, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = IncentiveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def incetive_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        incentive = Incentive.objects.get(pk=pk)
    except Incentive.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = IncentiveSerializer(incentive)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = IncentiveSerializer(incentive, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        incentive.delete()
        return HttpResponse(status=204)
    


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'incentive': reverse('incentive-list', request=request, format=format),
    })


class IncentiveHighlight(generics.GenericAPIView):
    queryset = Incentive.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        incentive = self.get_object()
        return Response(incentive.highlighted)
    
@api_view()
def xml(request):
    o="Fail-PATH: "
    o+=os.path.dirname(__file__)
    o+='/Text.xml'
    fileName=os.path.dirname(__file__)+'/Test.xml'
    if os.path.isfile(fileName):
        with open(fileName,'r') as f:
           str = f.read().replace('\n', '')
        o= xmltodict.parse(str)
    return Response(json.dumps(o))


@api_view()
def about(request):
    return Response({"Created_By": "Dor Amir"})

@api_view()
def incentiveTest(request):
    """
    Convert given text to uppercase
    (as a plain argument, or from a textfile's URL)
    Returns an indented JSON structure
    """

    # Store HTTP GET arguments
    plain_text   = request.GET.get('s'  , default=None)
    textfile_url = request.GET.get('URL', default=None)
    io = StringIO()
    if plain_text is None:
            return Response(json.dumps(
            {'incentive' : "Send Email"
             },
            indent=4))

    # Execute WebService specific task
    # here, converting a string to upper-casing
    if plain_text is not None:
        return Response(json.dumps(
            {'input' : plain_text,
             'result': plain_text.upper()
             },
            indent=4))

    elif textfile_url is not None:
        textfile = urllib2.urlopen(textfile_url).read()
        return Response(json.dumps(
            {'input' : textfile,
             'output': '\n'.join([line.upper() for line in textfile.split('\n')])
             },
            indent=4))


class IncentiveView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    queryset = Incentive.objects.all()
    serializer_class = IncentiveSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)


    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [incentive.status for incentive in Incentive.objects.all()]
        return Response(usernames)


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import Document
from forms import DocumentForm


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'],owner=request.user)
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('signups.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents=None
    if request.user.is_active:
        documents = Document.objects.filter(owner=request.user)

    # Render list page with the documents and the form
    return render_to_response('list.html', locals(), context_instance=RequestContext(request)
    )

from signups.runner import getTheBestForTheUser
from forms import getUserForm


def getUserID(request):
    # Handle file upload
    if request.method == 'POST':
        form = getUserForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = form.data[u'userID']
            BestIncentive=getTheBestForTheUser(request,newdoc).content
            # Redirect to the document list after POST
 # Render list page with the documents and the form
            return render_to_response('GetUser.html', locals(), context_instance=RequestContext(request))
    else:
        form = getUserForm() # A empty, unbound form

    return render_to_response('GetUser.html', locals(), context_instance=RequestContext(request)
    )


def userProfile(request):

    # Load documents for the list page
    incentivesList=[]
    incentives=None
    if request.user.is_active:
        incentives = Incentive.objects.filter(owner=request.user)
        for incentive in incentives:
             incentivesList.append(str(incentive.schemeID)+":"+incentive.schemeName)
        documents = Document.objects.filter(owner=request.user)
       # user=User.objects.get(username=request.user)

    return render_to_response(
        'profilePage.html',locals(),
        context_instance=RequestContext(request)
    )