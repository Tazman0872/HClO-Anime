import { createRouter, createWebHistory } from 'vue-router'

import Dashboard from '../views/Dashboard.vue'
import Projects from '../views/Projects.vue'
import Tasks from '../views/Tasks.vue'
import Team from '../views/Team.vue'
import Settings from '../views/Settings.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', component: Dashboard },
  { path: '/projects', component: Projects },
  { path: '/tasks', component: Tasks },
  { path: '/team', component: Team },
  { path: '/settings', component: Settings }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
