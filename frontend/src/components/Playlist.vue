<template>
  <ol>
    <li v-for="item in playlist">
      <h2 class="playlist-info">#{{ playlist.indexOf(item) }} - {{ item.title }} - {{ item.artist }} - {{ item.username }}</h2>
    </li>
  </ol>
</template>

<script>
export default {
  name: "Playlist",
  props: {
    playlist:  {
      type: Array,
      default: () => []
    },
  },
}
</script>

<style scoped>
.playlist-info {
}
li {
  list-style: none;
}
</style>
