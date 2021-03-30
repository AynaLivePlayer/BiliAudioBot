<template>
<h2 class="playing-lyric">{{lyric}}</h2>
</template>

<script>
export default {
  name: "PlayingCover",
  props : {
    lyric:String
  }
}
</script>

<style scoped>
.playing-lyric {
}
</style>
