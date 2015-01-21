__author__ = 'dor'
import Algorithem.Alg
from Algorithem.stupidAlg import StupidAlg
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
Alg=None

def startAlg(request):
    try:
        global Alg
        Alg = StupidAlg(request)
        Alg.init(request)
        return JSONResponse("{'Alg':'success'}")
    except:
        return JSONResponse("{'err':'Alg Problem'}")

def getRatedIncentives(request):
    try:
        global Alg
        incentives=Alg.getAllIncentiveRagted(request)
        jsonIncentive=json.dumps(incentives)
        return JSONResponse(jsonIncentive)
    except:
        return JSONResponse("{'err':'Alg Problem'}")


def getTheBestForTheUser(request, userID):
    global Alg
    try:
        incentive=Alg.getIncentiveForUser(Alg,request,userID)
        jsonIncentive=json.dumps(incentive)
        return JSONResponse(jsonIncentive)
    except:
        return JSONResponse("{'err':'Alg Problem'}")

def clear(request):
    global Alg
    Alg.clear(Alg,request)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)