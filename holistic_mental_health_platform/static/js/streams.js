const APP_ID = '1df3328931ef4dd0bbd7267def7befbb'
// const CHANNEL = 'main'
// // remember to generate a new token every 24hrs
// const TOKEN = '0061df3328931ef4dd0bbd7267def7befbbIADohnwJ3SkBN+daBIHMgFJAMDAWvRwbqPO5GkOwqHbwnWTNKL8AAAAAEAD2FHLc6HWwYgEAAQDodbBi'


// https://pypi.org/project/agora-token-builder/

const TOKEN = sessionStorage.getItem('token')
const CHANNEL = sessionStorage.getItem('room')
let UID = Number(sessionStorage.getItem('UID'))

let NAME = sessionStorage.getItem('name')
// create a local client object
const client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'})


let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async () => {
  document.getElementById('room-name').innerText = CHANNEL // get room name

  // user has joined our stream
  client.on('user-published', handleUserJoined)
  // user has left the stream
  client.on('user-left', handleUserLeft)

  // error cant join channel - get redirected
  try{
      UID = await client.join(APP_ID, CHANNEL, TOKEN, UID)
  }catch(error){
      console.error(error)
      window.open('/', '_self') //redirect to home page
  }
  
  // Creates an audio track and a video track
  localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

  let member = await createMember()

  let player = `<div  class="video-container" id="user-container-${UID}">
                   <div class="video-player" id="user-${UID}"></div>
                   <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                </div>`
  
  document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
  localTracks[1].play(`user-${UID}`) // play video
  // Publishes local audio and/or video tracks to a channel.
  await client.publish([localTracks[0], localTracks[1]])
}

let handleUserJoined = async (user, mediaType) => {
  remoteUsers[user.uid] = user
  await client.subscribe(user, mediaType)

  if (mediaType === 'video'){
    
      let player = document.getElementById(`user-container-${user.uid}`)
      // if player exists
      if (player != null){
          player.remove()
      }

      let member = await getMember(user)

      player = `<div  class="video-container" id="user-container-${user.uid}">
          <div class="video-player" id="user-${user.uid}"></div>
          <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
      </div>`

      document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
      user.videoTrack.play(`user-${user.uid}`)
  }

  if (mediaType === 'audio'){
      user.audioTrack.play() // play audio
  }
}

let handleUserLeft = async (user) => {
  // remove user from remoteUsers
  delete remoteUsers[user.uid]
  document.getElementById(`user-container-${user.uid}`).remove()
}

// close all the tracks and leave the channel and then redirect the user to his/her profile page
let leaveAndRemoveLocalStream = async () => {
  for (let i=0; localTracks.length > i; i++){
      localTracks[i].stop() // stop track
      localTracks[i].close() // close track 
  }

  await client.leave() // leave the channel
  //This is somewhat of an issue because if user leaves without actaull pressing leave button, it will not trigger
  deleteMember()
  window.open('/', '_self') // redirect to profile page
}

// turn on or off camera
let toggleCamera = async (e) => {
  console.log('TOGGLE CAMERA TRIGGERED')
  if(localTracks[1].muted){ // if camera is off
      await localTracks[1].setMuted(false) // turn on camera
      e.target.style.backgroundColor = '#fff'
  }else{
      await localTracks[1].setMuted(true) // change camera status
      e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)' // change button color
  }
}

// turn on or off microphone
let toggleMic = async (e) => {
  console.log('TOGGLE MIC TRIGGERED')
  if(localTracks[0].muted){
      await localTracks[0].setMuted(false)
      e.target.style.backgroundColor = '#fff'
  }else{
      await localTracks[0].setMuted(true)
      e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
  }
}

let createMember = async () => {
  let response = await fetch('/video-calling/create_member/', {
      method:'POST',
      headers: {
          'Content-Type':'application/json'
      },
      body:JSON.stringify({'name':NAME, 'room_name':CHANNEL, 'UID':UID})
  })
  let member = await response.json()
  return member
}


let getMember = async (user) => {
  let response = await fetch(`/video-calling/get_member/?UID=${user.uid}&room_name=${CHANNEL}`)
  let member = await response.json()
  return member
}

let deleteMember = async () => {
  let response = await fetch('/video-calling/delete_member/', {
      method:'POST',
      headers: {
          'Content-Type':'application/json'
      },
      body:JSON.stringify({'name':NAME, 'room_name':CHANNEL, 'UID':UID})
  })
  let member = await response.json()
}

window.addEventListener("beforeunload",deleteMember);

joinAndDisplayLocalStream()

document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream)
document.getElementById('camera-btn').addEventListener('click', toggleCamera)
document.getElementById('mic-btn').addEventListener('click', toggleMic)

