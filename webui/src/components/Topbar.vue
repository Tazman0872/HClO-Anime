<template>
  <header class="topbar">
    <div class="left">
      <div class="search">
        <input v-model="search" type="text" placeholder="搜索..." />
      </div>
    </div>

    <div class="right">
      <button class="icon-btn">🔔</button>
      <button class="profile">
        <img alt="avatar" src="https://i.pravatar.cc/40" />
        <span>张三</span>
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
const search = ref('')
</script>

<style scoped>
.topbar{height:64px;background:white;display:flex;align-items:center;justify-content:space-between;padding:0 20px;border-bottom:1px solid #e6eef8}
.search input{padding:8px 10px;border-radius:8px;border:1px solid #e6eef8;min-width:200px}
.right{display:flex;align-items:center;gap:10px}
.profile{display:flex;align-items:center;gap:8px;background:none;border:none;cursor:pointer}
.profile img{width:32px;height:32px;border-radius:8px}
</style>
