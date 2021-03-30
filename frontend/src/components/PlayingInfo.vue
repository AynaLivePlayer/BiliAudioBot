<template>
  <h2 class="playing-info">{{ title }} - {{ artist }} - {{ username }}</h2>
</template>

<script>
export default {
  name: "PlayingInfo",
  props: {
    title: String,
    artist: String,
    username: String
  }
}
</script>

<style scoped>
.playing-info {
}
</style>
