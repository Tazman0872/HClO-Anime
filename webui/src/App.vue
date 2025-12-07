<template>
  <div class="app-root">
    <Sidebar />
    <div class="main">
      <Topbar />
      <main class="content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue'
import Topbar from './components/Topbar.vue'
import { RouterView } from 'vue-router'
</script>

<style scoped>
.app-root{display:flex;min-height:100vh;background:#f3f4f6;color:#111}
.main{flex:1;display:flex;flex-direction:column;min-height:100vh}
.content{padding:20px}
</style>
