const PlaylistUpdateEvent = 'playlist_update'
const AudiobotPlayEvent = 'audiobot_play'
const LyricUpdateEvent = 'lyric_update'

export default class AudioBotWs {
  constructor () {
    this.onPlaylistUpdate = null
    this.onAudiobotPlay = null
    this.onLyricUpdate = null

    this.websocket = null
    this.retryCount = 0
    this.isDestroying = false
  }

  start () {
    this.wsConnect()
  }

  stop () {
    this.isDestroying = true
    if (this.websocket) {
      this.websocket.close()
    }
  }

  wsConnect () {
    if (this.isDestroying) {
      return
    }
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
    // 开发时使用localhost:5000
    const host = process.env.NODE_ENV === 'development' ? 'localhost:5000' : window.location.host
    const url = `${protocol}://${host}/ws/audiobot`
    this.websocket = new WebSocket(url)
    this.websocket.onopen = this.onWsOpen.bind(this)
    this.websocket.onclose = this.onWsClose.bind(this)
    this.websocket.onmessage = this.onWsMessage.bind(this)
  }

  onWsOpen () {
    this.retryCount = 0
  }

  onWsClose () {
    this.websocket = null
    if (this.isDestroying) {
      return
    }
    window.console.log(`掉线重连中${++this.retryCount}`)
    window.setTimeout(this.wsConnect.bind(this), 1000)
  }

  onWsMessage (event) {
    let jsonData = JSON.parse(event.data)
    for (var eventName in jsonData) {
      switch (eventName) {
        case PlaylistUpdateEvent: {
          if (this.onPlaylistUpdate) {
            this.onPlaylistUpdate(jsonData[eventName])
          }
          break
        }
        case AudiobotPlayEvent: {
          if (this.onAudiobotPlay) {
            this.onAudiobotPlay(jsonData[eventName])
          }
          break
        }
        case LyricUpdateEvent: {
          if (this.onLyricUpdate) {
            this.onLyricUpdate(jsonData[eventName])
          }
          break
        }
      }
    }
  }
}
