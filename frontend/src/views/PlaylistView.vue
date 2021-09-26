<template>
  <Playlist v-bind="playlist"></Playlist>
</template>

<script>
import AudioBotWs from '../api/AudioBotWS'
import PlayingInfo from "../components/PlayingInfo";
import PlayingCover from "../components/PlayingCover";
import Playlist from "../components/Playlist";

export default {
  name: 'PlaylistView',
  components: {Playlist, PlayingCover, PlayingInfo},
  data() {
    return {
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
      this.audio_bot_client.start()
    },
    onPlaylistUpdate(data) {
      this.playlist = {playlist: data}
    },
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
