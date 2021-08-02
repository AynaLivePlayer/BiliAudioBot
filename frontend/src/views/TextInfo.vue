<template>
  <div>
    <div>
      <PlayingCover v-bind='current'></PlayingCover>
      <PlayingInfo v-bind="current"></PlayingInfo>
    </div>
    <div>
      <Playlist v-bind="playlist"></Playlist>
    </div>
  </div>
</template>

<script>
import AudioBotWs from '../api/AudioBotWS'
import PlayingInfo from "../components/PlayingInfo";
import PlayingCover from "../components/PlayingCover";
import Playlist from "../components/Playlist";

export default {
  name: 'TextInfo',
  components: {Playlist, PlayingCover, PlayingInfo},
  data() {
    return {
      current: {
        title: '',
        artist: '',
        cover: '',
        username: ''
      },
      playlist: {
        playlist:[]}
    }
  },
  mounted() {
    this.initWSClient()
  },
  methods: {
    initWSClient() {
      this.audio_bot_client = new AudioBotWs()
      this.audio_bot_client.onPlaylistUpdate = this.onPlaylistUpdate
      this.audio_bot_client.onAudiobotPlay = this.onAudiobotPlay
      this.audio_bot_client.start()
    },
    onPlaylistUpdate(data) {
      // this.playlist.splice(0,this.playlist.length)
      // var pl = this.playlist
      // data.forEach(function (item) {
      //   pl.push(item)
      // })
      this.playlist = {playlist: data}
    },
    onAudiobotPlay(data) {
      this.current = data
    }
  }
}
</script>

<style scoped>
body {
  overflow: hidden;
}

.playing-cover {
  width: 100px;
  height: 100px;
}
</style>
