
// The App ID of your Agora project.
const APP_ID = '1df3328931ef4dd0bbd7267def7befbb'
// The token generated at your server
const TOKEN = sessionStorage.getItem('token')
// Unique channel name for the AgoraRTC session in the string format 
const CHANNEL = sessionStorage.getItem('room')

/* UID is the ID of the local user.
 The value is undefined if the local user has not joined a channel. */
let UID = Number(sessionStorage.getItem('UID'))
// name of the user
let NAME = sessionStorage.getItem('name')


// 1. create a local client object
const client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'})

// stores local audio and video tracks
let localTracks = []
// stores local audio and video tracks for remote users that join a specific stream
let remoteUsers = {}

// 2. get users audio and video tracks and display this to the screen
let joinAndDisplayLocalStream = async () => {
  document.getElementById('room-name').innerText = CHANNEL // get room name

  //  a remote user publishes an audio or video track.
  client.on('user-published', handleUserJoined)
  // Occurs when a remote user becomes offline.
  client.on('user-left', handleUserLeft)

  try{
    // 3. the join method enables a user to join a specific channel
      UID = await client.join(APP_ID, CHANNEL, TOKEN, UID)
  }catch(error){
      // if an error occurs, a user will get redirected to another page
      console.error(error)
      window.open('/', '_self') 
  }
  
  // 4. Creates an audio track and a video track
  localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

  let member = await createMember()

  // Create a player for each user on the channel and display it in the DOM
  let player = `<div  class="video-container" id="user-container-${UID}">
                   <div class="video-player" id="user-${UID}"></div>
                   <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                </div>`
  
  document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

  // play the video track
  localTracks[1].play(`user-${UID}`) 

  // 7) Publishes local audio and video tracks to a channel and now in users 
  /// in that channel will have access to the tracks
  await client.publish([localTracks[0], localTracks[1]])
}

// this function subscribes to the audio and video tracks of remote users
// and plays their video and audio tracks
let handleUserJoined = async (user, mediaType) => {
  remoteUsers[user.uid] = user
  // Subscribes the local client to the audio and/or video tracks of a remote user
  await client.subscribe(user, mediaType)

  // if the media type is video, play the video track and display it in our DOM
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
  // if the media type is audio, play the audio track
  if (mediaType === 'audio'){
      user.audioTrack.play() // play audio
  }
}

// when a user leaves, their tracks are stopped and their player is removed from the DOM
let handleUserLeft = async (user) => {
  // remove user from remoteUsers
  delete remoteUsers[user.uid]
  document.getElementById(`user-container-${user.uid}`).remove()
}

// user presses the leave button - close all the tracks and leave the channel and then redirect the user to his/her profile page
let leaveAndRemoveLocalStream = async () => {
  for (let i=0; localTracks.length > i; i++){
      localTracks[i].stop() // stop track
      localTracks[i].close() // close track 
  }

  await client.leave() // leave the channel
  //This is somewhat of an issue because if user leaves without actually pressing leave button, it will not trigger
  deleteMember()
  window.open('/', '_self') // redirect to profile page
}

//  turn on or off camera
let toggleCamera = async (e) => {
   //  the setMuted function turns the camera on or off
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
  // the setMuted function mutes or un-mutes the audio
  if(localTracks[0].muted){ // // if audio is muted
      await localTracks[0].setMuted(false) // unmute audio
      e.target.style.backgroundColor = '#fff'
  }else{
      await localTracks[0].setMuted(true)
      e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
  }
}

// create a member - call this method when a user enters the video call
let createMember = async () => {
  // create a POST request
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

// gets a member
let getMember = async (user) => {
  // fetch channel name and UID
  let response = await fetch(`/video-calling/get_member/?UID=${user.uid}&room_name=${CHANNEL}`)
  let member = await response.json()
  return member
}

// deletes member - call this method when a user leaves the video call
let deleteMember = async () => {
  // create a POST request
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