<script>
import { modules } from '../assets/modules-lock.json'
import { authors } from '../assets/authors.json'
import { tags } from '../assets/tags.json'
import { series } from '../assets/series.json'
import Card from './Card.vue'

export default {
  components: {
    Card
  },
  data() {
    return {
      modulesAll: Object.values(modules),
      modules: [],
      tags: tags,
      authors: authors,
      series: series,
      orders: [
        'Name, ASC',
        'Name, DESC',
        'Stars, ASC',
        'Stars, DESC',
        'Created at, ASC',
        'Created at, DESC',
        'Updated at, ASC',
        'Updated at, DESC',
        'Added at, ASC',
        'Added at, DESC',
      ],
      search: '',
      tag: null,
      author: null,
      serie: null,
      order: 'Name, ASC',
    }
  },
  methods: {
    setFilters() {
      let url = '/modules'
      let params = []
      if (this.search && this.search.length > 0) {
        params.push(`search=${this.search}`)
      }
      if (this.tag) {
        params.push(`tag=${this.tag}`)
      }
      if (this.author) {
        params.push(`author=${this.author}`)
      }
      if (this.serie) {
        params.push(`serie=${this.serie}`)
      }
      if (this.order) {
        params.push(`order=${this.order.replace(' ', '%20')}`)
      }
      if (params.length > 0) {
        url += '?' + params.join('&')
      }
      this.$router.push(url)
      this.loadModules()
    },
    loadModules() {
      let modules = this.modulesAll
      if (this.tag) {
        modules = modules.filter(m => m.tags.includes(this.tag))
      }
      if (this.author) {
        modules = modules.filter(m => m.author === this.author)
      }
      if (this.serie) {
        modules = modules.filter(m => m.series.includes(this.serie))
      }
      if (this.search) {
        modules = modules.filter(m => m.name.toLowerCase().includes(this.search.toLowerCase()))
      }
      if (this.order) {
        let [field, order] = this.order.split(', ')
        field = field.toLowerCase().replace(' ', '_')
        modules = modules.sort((a, b) => {
          if (order === 'ASC') {
            if (field.includes('_at'))
              return new Date(a[field]) - new Date(b[field])
            else if (field === 'name') {
              if (a[field] > b[field])
                return 1
              else if (a[field] < b[field])
                return -1
              else
                return 0
            }
            else
              return a[field] - b[field]
          } else {
            if (field.includes('_at'))
              return new Date(b[field]) - new Date(a[field])
            else if (field === 'name') {
              if (b[field] > a[field])
                return 1
              else if (b[field] < a[field])
                return -1
              else
                return 0
            }
            else
              return b[field] - a[field]
          }
        })
      }
      this.modules = modules
    },
  },
  created() {
    if (this.$route.query.tag) {
      this.tag = this.$route.query.tag
    }
    if (this.$route.query.author) {
      this.author = this.$route.query.author
    }
    if (this.$route.query.serie) {
      this.serie = this.$route.query.serie
    }
    if (this.$route.query.search) {
      this.search = this.$route.query.search
    }
    if (this.$route.query.order) {
      this.order = this.$route.query.order.replace('%20', ' ')
    }
    this.loadModules()
  }
}
</script>

<template>
  <div class="m-2">
    <div class="w-full max-w-6xl ml-auto mr-auto rounded-lg flex flex-col gap-2 border border-gray-200 p-2 mb-2">
      <input type="text" class="h-8 w-full p-1 border border-gray-200 max-w-xl rounded-lg bg-white" placeholder="Search..." v-model="search"/>
      <div class="flex flex-col gap-2 md:flex-row md:flex-wrap">
        <div>
          <label for="author" class="p-1 w-16 inline-block md:w-auto md:inline">Author:</label>
          <select id="author" name="author" class="filter-select rounded-lg border border-gray-200 p-1 h-8" v-model="author">
            <option value=""></option>
            <option v-for="author in authors" :key="author">{{ author }}</option>
          </select>
        </div>
        <div>
          <label for="serie" class="p-1 w-16 inline-block md:w-auto md:inline">Serie:</label>
          <select id="serie" name="serie" class="filter-select rounded-lg border border-gray-200 p-1 h-8" v-model="serie">
            <option value=""></option>
            <option v-for="serie in ([...series].sort((a, b) => b - a))" :key="serie">{{ serie }}</option>
          </select>
        </div>
        <div>
          <label for="tag" class="p-1 w-16 inline-block md:w-auto md:inline">Tag:</label>
          <select id="tag" name="tag" class="filter-select rounded-lg border border-gray-200 p-1 h-8" v-model="tag">
            <option value=""></option>
            <option v-for="tag in tags" :key="tag">{{ tag }}</option>
          </select>
        </div>
        <div>
          <label for="order" class="p-1 w-16 inline-block md:w-auto md:inline">Order:</label>
          <select id="order" name="order" class="filter-select rounded-lg border border-gray-200 p-1 h-8" v-model="order">
            <option v-for="order in orders" :key="order">{{ order }}</option>
          </select>
        </div>
        <button class="button-search rounded-lg fill-white h-8 ml-auto w-full md:w-32"
          @click="setFilters">
          <svg class="h-8 mx-auto" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>Search</title><path d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z" /></svg>
        </button>
      </div>
    </div>
    <div class="grid grid-cols-12 w-full max-w-6xl mx-auto gap-2 border border-gray-200 p-2 rounded-lg">
      <template v-for="m in modules" :key="`${m.author}/${m.name}`">
        <Card
        class="col-span-12 sm:col-span-6 md:col-span-4"
        :url="m.url"
        :name="m.name"
        :author="m.author"
        :stars="m.stars"
        :forks="m.forks"
        :series="m.series"
        :tags="m.tags"
        />
      </template>
    </div>
  </div>
</template>

<style scoped>
.module-grid {
  display: grid;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  max-width: 72rem;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 0.5rem;
  padding: 0.5rem;
  border-width: 1px;
  border-color: rgb(#e5e7eb);
  border-radius: 0.5rem;
}
.button-search {
  background-color: var(--bg-color);
}
</style>
