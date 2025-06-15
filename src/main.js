import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Home from './components/Home.vue'
import Modules from './components/Modules.vue'
import Module from './components/Module.vue'
import Contribute from './components/Contribute.vue'

const app = createApp(App)

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
      {
        path: '/',
        name: 'home',
        component: Home
      },
      {
        path: '/modules',
        name: 'modules',
        component: Modules
      },
      {
        path: '/module',
        name: 'module',
        component: Module
      },
      {
        path: '/contribute',
        name: 'contribute',
        component: Contribute
      },
      { path: '/:pathMatch(.*)*', redirect: '/' },
    ]
  })

app.use(router)

app.mount('#app')
