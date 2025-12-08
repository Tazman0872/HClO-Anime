import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import RSS from '../views/RSS.vue'
import Settings from '../views/Settings.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/about', name: 'About', component: About },
  { path: '/rss', name: 'Matrix', component: RSS },
  { path: '/settings', name: 'Ntfy', component: Settings },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
