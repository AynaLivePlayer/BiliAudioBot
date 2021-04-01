<template>
  <div>
    <div>
      <PlayingCover v-bind='current'></PlayingCover>
      <PlayingInfo v-bind="current"></PlayingInfo>
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
  import PlayingInfo from "../components/PlayingInfo";
  import PlayingCover from "../components/PlayingCover";

  export default {
    name: 'TextInfo',
    components: {PlayingCover, PlayingInfo},
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
  .playing-cover {
    width: 100px;
    height: 100px;
  }
  li {
    list-style:none;
  }
</style>
