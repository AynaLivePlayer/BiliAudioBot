<template>
  <div>
    <div>
      <img v-bind:src='current.cover'>
      <h2>{{ current.title }} - {{current.artist}} - {{current.username}}</h2>
    </div>
    <div>
      <ol>
        <li v-for="item in playlist">
          <h2>#{{playlist.indexOf(item)}} - {{ item.title }} - {{item.artist}} - {{item.username}}</h2>
        </li>
      </ol>
    </div>
  </div>
</template>

<script>
  import AudioBotWs from '../api/AudioBotWS'

  export default {
    name: 'TextInfo',
    data() {
      return {
        current: {
          title: '',
          artist: '',
          cover: '',
          username: ''
        },
        playlist: []
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
        this.playlist = data
        // data.forEach(function (item) {
        //   this.playlist.push(item)
        // })
      },
      onAudiobotPlay(data) {
        this.current = data
      }
    }
  }
</script>

<style scoped>
  body {
    overflow:hidden;
  }
  img {
    width: 100px;
    height: 100px;
  }
  li {
    list-style:none;
  }
</style>
