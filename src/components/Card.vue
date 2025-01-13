<script>
export default {
  props: {
    name: String,
    author: String,
    series: Array,
    tags: Array,
    stars: Number,
    forks: Number,
    chipLimit: {
      type: Number,
      default: 5
    },
  }
}

</script>

<template>
  <router-link class="w-full block rounded-lg border border-gray-200 p-2 hover:bg-gray-50 hover:cursor-pointer"
  :to="`/module?author=${author}&name=${name}`">
    <h5 class="text-lg pl-1 font-bold break-all">{{ name }}</h5>
    <div class="flex mt-1">
      <div class="flex gap-1 rounded-lg border border-gray-200 p-1 pr-1.5 h-8 break-keep bg-white" title="Author">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>Author</title><path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" /></svg>
        <span>{{ author }}</span>
      </div>
    </div>
    <div class="flex gap-1 mt-1 text-sm flex-wrap">
      <template v-for="serie in ([...series].sort((a, b) => b - a).slice(0, chipLimit).concat(series.length > chipLimit ? '...' : []))">
        <div class="rounded-lg border border-gray-200 p-1 bg-white" title="Serie">
            <span v-if="serie !== '...' && serie !== 'N/A'">{{ serie }}</span>
            <span v-else>{{ serie }}</span>
        </div>
      </template>
      <template v-for="tag in ([...tags].sort((a, b) => b - a).slice(0, chipLimit).concat(tags.length > chipLimit ? '...' : []))">
        <div class="rounded-lg border border-gray-200 p-1 uppercase italic" title="Tag">
            <span>{{ tag }}</span>
        </div>
      </template>
    </div>
    <div class="flex gap-1 mt-1 text-sm">
      <div class="flex gap-1 rounded-lg border border-gray-200 p-1 pr-1.5 bg-white">
        <svg class="h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>Stars</title><path d="M12,15.39L8.24,17.66L9.23,13.38L5.91,10.5L10.29,10.13L12,6.09L13.71,10.13L18.09,10.5L14.77,13.38L15.76,17.66M22,9.24L14.81,8.63L12,2L9.19,8.63L2,9.24L7.45,13.97L5.82,21L12,17.27L18.18,21L16.54,13.97L22,9.24Z" /></svg>
        <span>{{ stars }}</span>
      </div>
      <div class="flex gap-1 rounded-lg border border-gray-200 p-1 pr-1.5 bg-white">
        <svg class="h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>Forks</title><path d="M6,2A3,3 0 0,1 9,5C9,6.28 8.19,7.38 7.06,7.81C7.15,8.27 7.39,8.83 8,9.63C9,10.92 11,12.83 12,14.17C13,12.83 15,10.92 16,9.63C16.61,8.83 16.85,8.27 16.94,7.81C15.81,7.38 15,6.28 15,5A3,3 0 0,1 18,2A3,3 0 0,1 21,5C21,6.32 20.14,7.45 18.95,7.85C18.87,8.37 18.64,9 18,9.83C17,11.17 15,13.08 14,14.38C13.39,15.17 13.15,15.73 13.06,16.19C14.19,16.62 15,17.72 15,19A3,3 0 0,1 12,22A3,3 0 0,1 9,19C9,17.72 9.81,16.62 10.94,16.19C10.85,15.73 10.61,15.17 10,14.38C9,13.08 7,11.17 6,9.83C5.36,9 5.13,8.37 5.05,7.85C3.86,7.45 3,6.32 3,5A3,3 0 0,1 6,2M6,4A1,1 0 0,0 5,5A1,1 0 0,0 6,6A1,1 0 0,0 7,5A1,1 0 0,0 6,4M18,4A1,1 0 0,0 17,5A1,1 0 0,0 18,6A1,1 0 0,0 19,5A1,1 0 0,0 18,4M12,18A1,1 0 0,0 11,19A1,1 0 0,0 12,20A1,1 0 0,0 13,19A1,1 0 0,0 12,18Z" /></svg>
        <span>{{ forks }}</span>
      </div>
    </div>
  </router-link>
</template>

<style scoped>
</style>
