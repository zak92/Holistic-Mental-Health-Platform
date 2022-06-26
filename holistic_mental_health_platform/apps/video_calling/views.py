from django.shortcuts import render

from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import  VideoConferenceRoomMember
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def lobby(request):
    return render(request, 'video_calling/lobby.html')


def conferenceRoom(request):
    return render(request, 'video_calling/conference_room.html')

# automatically generate token
def getToken(request):
    # App ID issued to you by Agora
    appId = '1df3328931ef4dd0bbd7267def7befbb'
    # Certificate of the application that you registered in the Agora Dashboard
    appCertificate = 'd45ecf78e18e4d1d9a4b93dee7da2825'
    # Unique channel name for the AgoraRTC session in the string format 
    channelName = request.GET.get('channel') 
    # User ID. A 32-bit unsigned integer with a value ranging from 1 to (232-1).
    uid = random.randint(1, 231)
    # token expires within 24 hours
    expirationTimeInSeconds = 3600 * 24 
    # get current timestamp
    currentTimeStamp = int(time.time()) 
    # date when the token gets expired
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds 
    role = 1 
    # Build token with uid
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)

@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    # get or create a room member in the database
    member, created =  VideoConferenceRoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    
    return JsonResponse({'name':data['name']}, safe=False)

# retrieve member data from database
def getMember(request):
    # GET request - get channel name and uid from URL
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')
    # retrieve member from database
    member =  VideoConferenceRoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

# delete member data from database after video call ends
@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member =  VideoConferenceRoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)