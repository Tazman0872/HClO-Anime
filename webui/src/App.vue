<template>
  <div :class="['app', { dark: isDark }]">
    <Navbar :isDark="isDark" @toggleDark="toggleDark" />
    <div class="layout">
      <Sidebar
        :collapsed="collapsed"
        :isDark="isDark"
        @toggleCollapse="toggleSidebar"
      />
      <main class="content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import Navbar from './components/Navbar.vue'
import Sidebar from './components/Sidebar.vue'

const isDark = ref(false)
const collapsed = ref(false)

const toggleDark = () => (isDark.value = !isDark.value)
const toggleSidebar = () => (collapsed.value = !collapsed.value)

// Sync dark mode class to the document root so CSS variables apply to body/html
watch(isDark, (val) => {
  try { document.documentElement.classList.toggle('dark', val) } catch (e) {}
})

onMounted(() => {
  try { document.documentElement.classList.toggle('dark', isDark.value) } catch (e) {}
})
</script>

<style>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg);
  color: var(--text);
}

.layout {
  display: flex;
  flex: 1;
  align-items: flex-start;
}

.content {
  flex: 1;
  padding: 1rem;
  transition: background-color 0.3s;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
