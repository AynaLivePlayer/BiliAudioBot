<template>
<img referrer="no-referrer" class="playing-cover" v-bind:src='cover' alt="Cover"/>
</template>

<script>
export default {
  name: "PlayingCover",
  props : {
    cover:String
  }
}
</script>

<style scoped>
.playing-cover {
  width: 100%;
  height: 100%;
}
</style>
