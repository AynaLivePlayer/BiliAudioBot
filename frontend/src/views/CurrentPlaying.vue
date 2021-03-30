<template>
  <PlayingInfo v-bind='current'></PlayingInfo>
</template>

<script>
import AudioBotWs from "../api/AudioBotWS";
import PlayingInfo from "../components/PlayingInfo";


export default {
  name: "CurrentPlaying",
  components: {PlayingInfo},
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

</style>
