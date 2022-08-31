from django.shortcuts import render
from app1.serializer import itemsserializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import items
import requests
import threading
import time
import concurrent.futures
import json


# Create your views here.
@api_view(['GET'])
def getdata(request):
    data = items.objects.all()
    serialized=itemsserializer(data,many=True)
    return Response({
        'message':'data found',
        'data':serialized.data
    })

@api_view(['POST'])
def insert(request):
    data=request.data
    serialized=itemsserializer(data=data)
    if serialized.is_valid():
        serialized.save()
    
    else:
        return Response(serialized.errors,status.HTTP_400_BAD_REQUEST)

    return Response({
        'message':'your data is added succesfully',
        'data':serialized.data
        })


TL = threading.local()

def session():
    if not hasattr(TL, "session"):
        TL.session = requests.Session()
    return TL.session


def read(url):
    ses = session()
    with ses.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def readall(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(read, sites)

def delay_time(request,delay_value):
    # print(delay)
    sites = [f"https://httpbin.org/delay/{delay_value}",
       f"https://httpbin.org/delay/{delay_value}",
       f"https://httpbin.org/delay/{delay_value}",
       f"https://httpbin.org/delay/{delay_value}",
       f"https://httpbin.org/delay/{delay_value}",
       ] 
    start_time = time.time() 
    readall(sites)
    duration = time.time() - start_time
    print(f"time take {duration} seconds")
    return JsonResponse({"time_taken":duration})

        