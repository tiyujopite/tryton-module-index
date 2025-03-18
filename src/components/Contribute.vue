<script>
import { authors } from '../assets/authors.json'
import { tags } from '../assets/tags.json'

export default {
  data() {
    return {
      modules: [],
      tagsOriginal: [...tags],
      tags: tags,
      authors: authors,
      inputAuthor: '',
      inputName: '',
      inputUrl: '',
      inputPackageName: '',
      inputDocUrl: '',
      inputTags: [],
      newTag: ''
    }
  },
  methods: {
    addModule() {
      // validate form
      if (!this.inputAuthor || !this.inputName || !this.inputUrl || !this.inputPackageName) {
        return
      }
      this.modules.push({
        key: `${this.inputAuthor}/${this.inputName}`,
        author: this.inputAuthor,
        name: this.inputName,
        url: this.inputUrl,
        package_name: this.inputPackageName,
        doc_url: this.inputDocUrl,
        tags: this.inputTags
      })
      this.inputName = ''
      this.inputUrl = ''
      this.inputPackageName = ''
      this.inputDocUrl = ''
      this.inputTags = []
    },
    addTag() {
      if (this.newTag) {
        this.tags.push(this.newTag)
        this.inputTags.push(this.newTag)
        this.newTag = ''
      }
    },
    editModule(key) {
      let module = this.modules.find(module => module.key === key)
      this.modules = this.modules.filter(module => module.key !== key)
      this.inputAuthor = module.author
      this.inputName = module.name
      this.inputUrl = module.url
      this.inputPackageName = module.package_name
      this.inputDocUrl = module.doc_url
      this.inputTags = module.tags
    },
    deleteModule(key) {
      this.modules = this.modules.filter(module => module.key !== key)
    },
    toggleAccordion(accordionPrefix) {
      const content = document.getElementById(`${accordionPrefix}-content`)
      const arrowDown = document.getElementById(`${accordionPrefix}-arrow-down`)
      const arrowUp = document.getElementById(`${accordionPrefix}-arrow-up`)
      content.classList.toggle('hidden')
      arrowDown.classList.toggle('hidden')
      arrowUp.classList.toggle('hidden')
    },
  },
  computed: {
    newAuthors() {
      let authors = []
      for (let module of this.modules) {
        if (!this.authors.includes(module.author)) {
          authors.push(module.author)
        }
      }
      return authors
    },
    newAuthorsJson() {
      let json = ''
      for (let author of this.newAuthors.sort()) {
        json += `    "${author}",\n`
      }
      return json
    },
    newTags() {
      let tags = []
      for (let module of this.modules) {
        for (let tag of module.tags) {
          if (!this.tagsOriginal.includes(tag) && !tags.includes(tag)) {
            tags.push(tag)
          }
        }
      }
      return tags
    },
    newTagsJson() {
      let json = ''
      for (let tag of this.newTags.sort()) {
        json += `    "${tag}",\n`
      }
      return json
    },
    modulesJson() {
      let json = ''
      for (let [idxM, module] of this.modules.sort().entries()) {
        const isLastModule = idxM === this.modules.length - 1
        json += `    {\n`
        json += `      "key": "${module.key}",\n`
        json += `      "package_name": "${module.package_name}",\n`
        json += `      "url": "${module.url}"`
        if (module.doc_url) {
          json += `,\n`
          json += `      "doc_url": "${module.doc_url}"`
        }
        if (module.tags.length) {
          json += `,\n`
          json += `      "tags": [\n`
          for (let [idxT, tag] of module.tags.sort().entries()) {
            const isLastTag = idxT === module.tags.length - 1
            json += `        "${tag}"${isLastTag? '' : ','}\n`
          }
          json += `      ]`
        }
        json += `\n`
        json += `    }${isLastModule? '' : ','}\n`
      }
      return json
    },
    checkCommand() {
      let command = `python api check`
      for (let module of this.modules) {
        command += ` ${module.key}`
      }
      return command
    }
  },
  mounted() {
    document.title = `TMI - Contribute`
  }
}
</script>

<template>
  <div class="w-full max-w-6xl ml-auto mr-auto rounded-lg flex flex-col gap-2 border border-gray-200 p-2 my-2">
    <a href="https://github.com/tiyujopite/tryton-module-index" target="_blank" class="text-2xl pl-1 flex items-center gap-2 hover:underline">
      <span class="font-bold">SOURCE CODE</span>
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="h-10"><title>link</title><path d="M3.9,12C3.9,10.29 5.29,8.9 7,8.9H11V7H7A5,5 0 0,0 2,12A5,5 0 0,0 7,17H11V15.1H7C5.29,15.1 3.9,13.71 3.9,12M8,13H16V11H8V13M17,7H13V8.9H17C18.71,8.9 20.1,10.29 20.1,12C20.1,13.71 18.71,15.1 17,15.1H13V17H17A5,5 0 0,0 22,12A5,5 0 0,0 17,7Z" /></svg>
    </a>
    <div class="w-full rounded-lg border border-gray-200 px-2">
      <div class="flex items-center justify-between gap-2 cursor-pointer" @click="toggleAccordion('improve-this-website')">
        <h2 class="text-2xl font-bold m-2">Improve this website</h2>
        <svg id="improve-this-website-arrow-down" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="h-8"><title>chevron-down</title><path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z" /></svg>
        <svg id="improve-this-website-arrow-up" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="h-8 hidden"><title>chevron-up</title><path d="M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z" /></svg>
      </div>
      <div id="improve-this-website-content" class="m-2 hidden">
        <p>You can contribute doing improvements or bug/behavior fixes. You must create a fork of the repository and create a PR with the change.</p>
        <p>You can find more details on how to start the project in its README.</p>
        <div class="p-2 my-2 rounded-lg bg-yellow-50 border border-yellow-400 font-semibold w-fit" role="alert">
          PRs that modify the website and add modules at the same time will not be approved !!
        </div>
      </div>
    </div>
    <div class="w-full rounded-lg border border-gray-200 px-2">
      <div class="flex items-center justify-between gap-2 cursor-pointer" @click="toggleAccordion('add-modules')">
        <h2 class="text-2xl font-bold m-2">Add modules</h2>
        <svg id="add-modules-arrow-down" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="h-8"><title>chevron-down</title><path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z" /></svg>
        <svg id="add-modules-arrow-up" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="h-8 hidden"><title>chevron-up</title><path d="M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z" /></svg>
      </div>
      <div id="add-modules-content" class="hidden">
        <div class="m-2">
          <p>To add modules you need to create a PR to the repository adding basic information about them in the file <code class="font-semibold">`src/assets/modules.json`</code></p>
          <p>(always at the end of the list)</p>
          <div class="p-2 my-2 rounded-lg bg-yellow-50 border border-yellow-400 font-semibold w-fit" role="alert">
            Never modify the <code class="font-semibold">`src/assets/modules-lock.json`</code>!!
          </div>
          <br>
          <p class="font-semibold">Information needed:</p>
          <ul class="list-disc list-inside">
            <li class="underline">Mandatory:</li>
            <ul class="list-disc list-inside ml-5">
              <li>Author</li>
              <li>Name</li>
              <li>URL</li>
              <li>Package name</li>
            </ul>
            <li class="underline">Optional, but recommended:</li>
            <ul class="list-disc list-inside ml-5">
              <li>Description</li>
              <li>Documentation URL</li>
              <li>Tags</li>
            </ul>
          </ul>
          <br>
        </div>
        <div>
          <h2 class="text-xl font-bold mb-2">Pull Request wizard</h2>
          <div class="block md:hidden p-2 my-2 rounded-lg bg-yellow-50 border border-yellow-400 font-semibold w-fit" role="alert">
            Only available for desktop mode.
          </div>
          <div class="hidden md:flex flex-col gap-2 rounded-lg border border-gray-200 p-2">
            <form id="add-module" class="flex flex-col gap-2" @submit.prevent>
              <div class="flex">
                <div class="flex items-center">
                  <label for="author" class="p-1 inline-block">Author:</label>
                  <input
                  required
                  id="author"
                  name="author"
                  type="text"
                  class="rounded-lg border border-gray-200 p-1 h-8"
                  v-model="inputAuthor"
                  list="author-list"/>
                  <datalist id="author-list">
                    <option
                    class="m-1"
                    v-for="author in authors"
                    :key="author"
                    :value="author"
                    >{{ author }}</option>
                  </datalist>
                </div>
                <div class="flex items-center w-full">
                  <label for="name" class="p-1 inline-block">Name:</label>
                  <input
                  required
                  id="name"
                  name="name"
                  type="text"
                  class="rounded-lg border border-gray-200 p-1 h-8 w-full"
                  v-model="inputName"/>
                </div>
              </div>
              <div class="flex items-center w-full">
                <label for="url" class="p-1 inline-block">URL:</label>
                <input
                required
                id="url"
                name="url"
                type="text"
                class="rounded-lg border border-gray-200 p-1 h-8"
                v-model="inputUrl"/>
              </div>
              <div class="flex items-center">
                <label for="package_name" class="p-1 inline-block">Package name:</label>
                <input
                required
                id="package_name"
                name="package_name"
                type="text"
                class="rounded-lg border border-gray-200 p-1 h-8 w-1/2"
                v-model="inputPackageName"/>
                <div id="tooltip-package-name">
                  <div class="rounded-lg text-white font-semibold add-button p-1 px-2 ml-2">?</div>
                  <div class="rounded-lg p-1 px-2 ml-2 bg-white border border-gray-200 tooltip-package-name-text w-96">
                    <p>This is the `name` parameter passed to the `setup` function in the `setup.py` file.</p>
                  </div>
                </div>
              </div>
              <div class="flex items-center w-full">
                <label for="doc_url" class="p-1 inline-block">DocURL:</label>
                <input
                id="doc_url"
                name="doc_url"
                type="text"
                class="rounded-lg border border-gray-200 p-1 h-8 w-full"
                v-model="inputDocUrl"/>
              </div>
              <div class="flex items-center">
                <label for="tags" class="p-1 inline-block">Tags:</label>
                <select
                id="tags"
                name="tags"
                class="rounded-lg border border-gray-200 h-24 w-96"
                list="tags-list"
                multiple
                v-model="inputTags">
                  <option
                  class="m-1"
                  v-for="tag in tags"
                  :key="tag"
                  :value="tag"
                  >{{ tag }}</option>
                </select>
                <input
                type="text"
                class="ml-1 rounded-lg border border-gray-200 p-1 h-8 w-34"
                v-model="newTag"
                placeholder="Add new tag"/>
                <button
                class="ml-1 text-white text-xl font-semibold px-2 rounded-lg w-fit add-button"
                @click="addTag">+</button>
              </div>
            </form>
            <button
            class="text-white font-semibold py-2 px-4 rounded-lg w-fit add-button"
            @click="addModule">Add module</button>
          </div>
        </div>
        <div class="mt-2 flex flex-wrap gap-2" v-show="modules.length">
          <div class="flex items-center gap-2 rounded-lg border border-gray-200 p-2" v-for="module in modules" :key="module.key">
            {{ module.key }}
            <button
            class="text-white font-semibold rounded-lg px-2 w-fit add-button"
            @click="deleteModule(module.key)">Delete</button>
            <button
            class="text-white font-semibold rounded-lg px-2 w-fit add-button"
            @click="editModule(module.key)">Edit</button>
          </div>
        </div>
        <div class="mt-2" v-show="modules.length">
          <h2><span class="text-xl font-bold">Summary of changes</span> (copy/paste and step by step)</h2>
          <div class="rounded-lg border border-gray-200 p-2 mt-2" v-show="newAuthors.length">
            <p class="font-semibold">New authors</p>
            <ul class="list-disc list-inside">
              <li>Will be added in <code>`src/assets/authors.json`</code></li>
              <li>Do not forget that authors should be ordered alphabetically.</li>
            </ul>
            <pre class="bg-gray-100 rounded-lg p-1 mt-1">{{ newAuthorsJson }}</pre>
          </div>
          <div class="rounded-lg border border-gray-200 p-2 mt-2" v-show="newTags.length">
            <p class="font-semibold">New tags</p>
            <ul class="list-disc list-inside">
              <li>Will be added in <code>`src/assets/tags.json`</code></li>
              <li>Do not forget that tags should be ordered alphabetically.</li>
            </ul>
            <pre class="bg-gray-100 rounded-lg p-1 mt-1">{{ newTagsJson }}</pre>
          </div>
          <div class="rounded-lg border border-gray-200 p-2 mt-2">
            <p class="font-semibold">New modules</p>
            <ul class="list-disc list-inside">
              <li>Will be added at the end of <code>`src/assets/modules.json`</code></li>
            </ul>
            <pre class="bg-gray-100 rounded-lg p-1 mt-1 overflow-x-auto">{{ modulesJson }}</pre>
          </div>
          <div class="rounded-lg border border-gray-200 p-2 mt-2">
            <p class="font-semibold">Test command</p>
            <ul class="list-disc list-inside">
              <li>Before creating the PR the checks must be run successfully.</li>
            </ul>
            <pre class="bg-gray-100 rounded-lg p-1 mt-1 overflow-x-auto">{{ checkCommand }}</pre>
          </div>
          <div class="rounded-lg border border-gray-200 p-2 mt-2">
            <p class="font-semibold">Descriptions</p>
            <ul class="list-disc list-inside">
              <li>After executing the previous command, the description files will be created and you will be able to fill them.</li>
              <li>Allocated in <code>`src/assets/description/author__module_name.md`</code></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.add-button {
  background-color: var(--bg-color);
}
.add-button:hover {
  background-color: var(--bg-color-hover);
}
#tooltip-package-name {
  position: relative;
  display: inline-block;
}

#tooltip-package-name .tooltip-package-name-text {
  visibility: hidden;
  position: absolute;
  z-index: 1;
  top: 0;
  left: 2rem;
}
#tooltip-package-name:hover .tooltip-package-name-text {
  visibility: visible;
}

</style>
