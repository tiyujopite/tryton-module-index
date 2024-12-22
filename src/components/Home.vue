<script>
import { modules } from '../assets/modules-lock.json'
import Card from './Card.vue'

export default {
  components: {
    Card
  },
  data() {
    return {
      modules: Object.values(modules)
    }
  },
  computed: {
    mostStarred() {
      return [...this.modules].sort((a, b) => b.stars - a.stars).slice(0, 5)
    },
    random() {
      return [...this.modules].sort(() => Math.random() - 0.5).slice(0, 5)
    },
    lastAdded() {
      return [...this.modules].sort((a, b) => new Date(b.added_at) - new Date(a.added_at)).slice(0, 5)
    },
  }
}
</script>

<template>
  <div class="w-full mx-auto grid max-w-6xl grid-cols-12 gap-4 p-2">
    <div class="col-span-12 rounded-lg border border-gray-200 p-2 sm:col-span-8 sm:col-start-3 md:col-span-6 lg:col-span-4">
      <h4 class="text-2xl font-bold text-center mb-2">MOST STARRED</h4>
      <div class="flex flex-col gap-2">
        <template v-for="module in mostStarred" :key="`most_starred-${module.author}/${module.name}`">
          <Card
          :name="module.name"
          :author="module.author"
          :stars="module.stars"
          :forks="module.forks"
          :series="module.series"
          :tags="module.tags"
          />
        </template>
        <button class="more-btn w-full text-white font-bold pt-2 pb-2 pl-4 pr-4 rounded-lg hover:underline"
        @click="$router.push('/modules?order=Stars,%20DESC')"
        >SHOW MORE</button>
    </div>
    </div>
    <div class="col-span-12 rounded-lg border border-gray-200 p-2 sm:col-span-8 sm:col-start-3 md:col-span-6 lg:col-span-4">
      <h4 class="text-2xl font-bold text-center mb-2">RANDOM</h4>
      <div class="flex flex-col gap-2">
        <template v-for="module in random" :key="`random-${module.author}/${module.name}`">
          <Card
          :name="module.name"
          :author="module.author"
          :stars="module.stars"
          :forks="module.forks"
          :series="module.series"
          :tags="module.tags"
          />
        </template>
        <button class="more-btn w-full text-white font-bold pt-2 pb-2 pl-4 pr-4 rounded-lg hover:underline"
        @click="$router.push('/modules')"
        >SHOW ALL</button>
    </div>
    </div>
    <div class="col-span-12 rounded-lg border border-gray-200 p-2 sm:col-span-8 sm:col-start-3 md:col-span-6 lg:col-span-4">
      <h4 class="text-2xl font-bold text-center mb-2">LAST ADDED</h4>
      <div class="flex flex-col gap-2">
        <template v-for="module in lastAdded" :key="`last_added-${module.author}/${module.name}`">
          <Card
          :name="module.name"
          :author="module.author"
          :stars="module.stars"
          :forks="module.forks"
          :series="module.series"
          :tags="module.tags"
          />
        </template>
        <button class="more-btn w-full text-white font-bold pt-2 pb-2 pl-4 pr-4 rounded-lg hover:underline"
        @click="$router.push('/modules?order=Added%20at,%20DESC')"
        >SHOW MORE</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.more-btn {
  background-color: var(--bg-color);
}
</style>
