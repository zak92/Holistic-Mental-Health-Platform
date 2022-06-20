from django.shortcuts import render

from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def lobby(request):
    return render(request, 'video_calling/lobby.html')


def conferenceRoom(request):
    return render(request, 'video_calling/conference_room.html')

# automatically generate token
def getToken(request):
    appId = '1df3328931ef4dd0bbd7267def7befbb'
    appCertificate = 'd45ecf78e18e4d1d9a4b93dee7da2825'
    channelName = request.GET.get('channel') # get channel name from url
    uid = random.randint(1, 230) # must be a number between 1 and 230
    expirationTimeInSeconds = 3600 * 24 # token expires within 24 hours
    currentTimeStamp = int(time.time()) # get current timestamp
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds # date when the token gets expired
    role = 1 # 1 - host , 2 - guest
    # build token
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)