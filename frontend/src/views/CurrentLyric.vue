<template>
  <PlayingLyric v-bind:lyric="lyric"></PlayingLyric>
</template>

<script>
import AudioBotWs from "../api/AudioBotWS";
import PlayingLyric from "../components/PlayingLyric"

export default {
  name: "CurrentPlaying",
  components: {PlayingLyric},
  data() {
    return {
      lyric: ""
    }
  },
  mounted() {
    this.initWSClient()
  },
  methods: {
    initWSClient() {
      this.audio_bot_client = new AudioBotWs()
      this.audio_bot_client.onLyricUpdate = this.onLyricUpdate
      this.audio_bot_client.start()
    },
    onLyricUpdate(data) {
      this.lyric = data["lyric"]
    }
  }
}
</script>

<style scoped>

</style>
