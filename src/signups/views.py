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
from signups.models import Incentive
from signups.serializers import IncentiveSerializer,UserSerializer
from rest_framework.decorators import detail_route
from rest_framework import renderers,permissions,status,generics, mixins
from signups.permissions import IsOwnerOrReadOnly
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


# Create your views here.

from .forms import SignUpForm

def home(request):
    
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.save()
        messages.success(request,'We will be in touch')
        return HttpResponseRedirect('/thank-you/')
    return render_to_response("signups.html",locals(),context_instance=RequestContext(request)) 

def thankyou(request):
    
    
    return render_to_response("thankyou.html",locals(),context_instance=RequestContext(request)) 

def aboutus(request):
    
    
    return render_to_response("aboutus.html",locals(),context_instance=RequestContext(request))


def fbview(request):
    data = {'foo': 'bar', 'hello': 'world'}
    return HttpResponse(json.dumps(data), content_type='application/json')

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    

    
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
        incetive = Incentive.objects.all()
        serializer = IncentiveSerializer(incetive, many=True)
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
        incetive = Incentive.objects.get(pk=pk)
    except Incentive.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = IncentiveSerializer(incetive)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = IncentiveSerializer(incetive, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        incetive.delete()
        return HttpResponse(status=204)
    


#class IncentiveList(APIView):
#    """
#    List all snippets, or create a new snippet.
#    """
#    def get(self, request, format=None):
#        incentive = Incentive.objects.all()
#        serializer = IncentiveSerializer(incentive, many=True)
#        return Response(serializer.data)
#
#    def post(self, request, format=None):
#        serializer = IncentiveSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#class IncentiveDetail(APIView):
#    """
#    Retrieve, update or delete a snippet instance.
#    """
#    def get_object(self, pk):
#        try:
#            return Incentive.objects.get(pk=pk)
#        except Incentive.DoesNotExist:
#            raise Http404
#
#    def get(self, request, pk, format=None):
#        incentive = self.get_object(pk)
#        serializer = IncentiveSerializer(incentive)
#        return Response(serializer.data)
#
#    def put(self, request, pk, format=None):
#        incentive = self.get_object(pk)
#        serializer = IncentiveSerializer(incentive, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    def delete(self, request, pk, format=None):
#        incentive = self.get_object(pk)
#        incentive.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
#
#class IncetiveList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#    queryset = Incentive.objects.all()
#    serializer_class = IncentiveSerializer
#
#    def get(self, request, *args, **kwargs):
#        return self.list(request, *args, **kwargs)
#
#    def post(self, request, *args, **kwargs):
#        return self.create(request, *args, **kwargs)
#    
#class IncentiveDetail(mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    generics.GenericAPIView):
#    queryset = Incentive.objects.all()
#    serializer_class = IncentiveSerializer
#
#    def get(self, request, *args, **kwargs):
#        return self.retrieve(request, *args, **kwargs)
#
#    def put(self, request, *args, **kwargs):
#        return self.update(request, *args, **kwargs)
#
#    def delete(self, request, *args, **kwargs):
#        return self.destroy(request, *args, **kwargs)
#    
#class IncetiveList(generics.ListCreateAPIView):
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#    queryset = Incentive.objects.all()
#    serializer_class = IncentiveSerializer
#    def perform_create(self, serializer):
#        serializer.save(owner=self.request.user)
#
#
#class IncentiveDetail(generics.RetrieveUpdateDestroyAPIView):
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                      IsOwnerOrReadOnly,)
#    queryset = Incentive.objects.all()
#    serializer_class = IncentiveSerializer
#    
#class UserList(generics.ListAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#
#
#class UserDetail(generics.RetrieveAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#    


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'incentive': reverse('incentive-list', request=request, format=format),
        'aboutus':reverse('about-list', request=request, format=format)
    })

class IncentiveHighlight(generics.GenericAPIView):
    queryset = Incentive.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        incentive = self.get_object()
        return Response(incentive.highlighted)
    
@api_view()
def about(request):
    return Response({"Created_By": "Dor Amir"})