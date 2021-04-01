<template>
  <PlayingCover v-bind="current"></PlayingCover>
</template>

<script>
import AudioBotWs from "../api/AudioBotWS";
import PlayingCover from "../components/PlayingCover";

export default {
  name: "CurrentCover",
  components: {PlayingCover},
  data() {
    return {
      current: {
        title: '',
        artist: '',
        cover: '',
        username: ''
      }
    }
  },
  mounted() {
    this.initWSClient()
  },
  methods: {
    initWSClient() {
      this.audio_bot_client = new AudioBotWs()
      this.audio_bot_client.onAudiobotPlay = this.onAudiobotPlay
      this.audio_bot_client.start()
    },
    onAudiobotPlay(data) {
      this.current = data
    }
  }
}
</script>

<style scoped>
.playing-cover {
  width: 100%;
  height: 100%;
}
</style>
