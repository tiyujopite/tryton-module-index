<script>
import { marked } from 'marked'
import { modules } from '../assets/modules-lock.json'

export default {
  data() {
    return {
      key: null,
      module: null,
    }
  },
  async created() {
    const key = `${this.$route.query.author}/${this.$route.query.name}`
    this.key = key
    this.module = modules[key]
  },
  mounted() {
    document.title = `TMI - ${this.module.name}`
    const description = new TextDecoder().decode(
      Uint8Array.from(atob(this.module.description), c => c.charCodeAt(0)))
    document.getElementById('description').innerHTML = marked.parse(description)
  }
}
</script>

<template>
  <div class="w-full max-w-6xl ml-auto mr-auto rounded-lg flex flex-col gap-2 border border-gray-200 p-2 my-2">
    <h5 translate="no" class="text-2xl font-bold mb-2 pl-1 break-all">{{ module.name }}</h5>
    <div id="description" class="prose text-black p-2 pt-0 w-full max-w-6xl"></div>
    <div class="w-full rounded-lg border border-gray-200 px-2">
      <table class="table-auto w-full">
        <tbody>
          <tr class="border-b hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">Author:</td>
            <td translate="no" class="pl-2 p-1.5">{{ module.author }}</td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">Package name:</td>
            <td translate="no" class="pl-2 p-1.5 break-all">{{ module.package_name }}</td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">URL:</td>
            <td class="pl-2 p-1.5"><a class="hover:underline break-all" :href="module.url" target="_blank">{{ module.url }}</a></td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50" v-if="module.pypi_available">
            <td class="font-bold w-auto border-r p-1.5">PyPI available:</td>
            <td class="pl-2 p-1.5">
              <span class="flex items-center gap-1 break-keep" v-if="module.pypi_available">
                <svg class="h-5 fill-green-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>Yes</title><path d="M23,12L20.56,9.22L20.9,5.54L17.29,4.72L15.4,1.54L12,3L8.6,1.54L6.71,4.72L3.1,5.53L3.44,9.21L1,12L3.44,14.78L3.1,18.47L6.71,19.29L8.6,22.47L12,21L15.4,22.46L17.29,19.28L20.9,18.46L20.56,14.78L23,12M10,17L6,13L7.41,11.59L10,14.17L16.59,7.58L18,9L10,17Z" /></svg>
                <a class="hover:underline" :href="`https://pypi.org/project/${module.package_name}`" target="_blank">View on PyPI</a>
              </span>
            </td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50" v-if="module.doc_url">
            <td class="font-bold w-auto border-r p-1.5">Documentation URL:</td>
            <td class="pl-2 p-1.5"><a class="hover:underline break-all" :href="module.doc_url" target="_blank">{{ module.doc_url }}</a></td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">License:</td>
            <td class="pl-2 p-1.5">{{ module.license.toUpperCase() }}</td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">Series:</td>
            <td class="pl-2 p-1.5">{{ [...module.series].sort((a, b) => b - a).join(', ') }}</td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">Tags:</td>
            <td class="pl-2 p-1.5 uppercase">{{ [...module.tags].sort().join(', ') }}</td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50">
            <td translate="no" class="font-bold w-auto border-r p-1.5">Stars:</td>
            <td class="pl-2 p-1.5">{{ module.stars }}</td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50">
            <td translate="no" class="font-bold w-auto border-r p-1.5">Forks:</td>
            <td class="pl-2 p-1.5">{{ module.forks }}</td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">Created at:</td>
            <td class="pl-2 p-1.5">{{ module.created_at }}</td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">Updated at:</td>
            <td class="pl-2 p-1.5">{{ module.updated_at }}</td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">Added at:</td>
            <td class="pl-2 p-1.5">{{ module.added_at }}
              <br>
              <span class="text-xs opacity-70"> (When it was added to our website)</span>
            </td>
          </tr>
          <tr class="p-1.5 hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">Information updated at:</td>
            <td class="pl-2 p-1.5">{{ module.info_updated_at }}
              <br>
              <span class="text-xs opacity-70"> (When the information displayed on our website was last updated)</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="flex flex-wrap gap-2">
      <a
        role="button"
        class="text-white font-bold py-2 px-4 rounded-lg w-fit edit-button"
        target="_blank"
        :href="`https://github.com/tiyujopite/tryton-module-index/edit/main/src/assets/description/${key.replace('/', '__')}.md`"
        >
        Edit description
      </a>
      <a
        role="button"
        class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-lg w-fit"
        target="_blank"
        :href="`https://github.com/tiyujopite/tryton-module-index/issues/new?title=Error%20report%3A%20${key.replace('/', '%2F')}`"
        >
        Report an error
      </a>
    </div>
  </div>
</template>

<style scoped>
.edit-button {
  background-color: var(--bg-color);
}
.edit-button:hover {
  background-color: var(--bg-color-hover);
}
</style>
