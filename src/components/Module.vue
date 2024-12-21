<script>
import { modules } from '../assets/modules-lock.json'
export default {
  data() {
    return {
      key: null,
      module: null,
    }
  },
  created() {
    const key = `${this.$route.query.author}/${this.$route.query.name}`
    this.module = modules[key]
  }
}
</script>

<template>
  <div class="w-full max-w-6xl ml-auto mr-auto rounded-lg flex flex-col gap-2 border border-gray-200 p-2 mt-2">
    <h5 class="text-2xl font-bold mb-2 pl-1 break-all">{{ module.name }}</h5>
    <div class="w-full rounded-lg border border-gray-200 px-2">
      <table class="table-auto w-full">
        <tbody>
          <tr class="border-b hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">Author:</td>
            <td class="pl-2 p-1.5">{{ module.author }}</td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">Package name:</td>
            <td class="pl-2 p-1.5">{{ module.package_name }}</td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">URL:</td>
            <td class="pl-2 p-1.5"><a class="hover:underline break-all" :href="module.url" target="_blank">{{ module.url }}</a></td>
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
            <td class="font-bold w-auto border-r p-1.5">PyPI available:</td>
            <td class="pl-2 p-1.5"><input type="checkbox" id="pypi_available" :checked="module.pypi_available" disabled></td>
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
            <td class="font-bold w-auto border-r p-1.5">Stars:</td>
            <td class="pl-2 p-1.5">{{ module.stars }}</td>
          </tr>
          <tr class="border-b p-1.5 hover:bg-gray-50">
            <td class="font-bold w-auto border-r p-1.5">Forks:</td>
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
  </div>
</template>

<style scoped>
</style>
