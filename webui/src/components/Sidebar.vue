<template>
  <aside class="sidebar">
    <div class="brand">我的应用</div>

    <nav class="nav">
      <RouterLink v-for="item in menu" :key="item.id" :to="item.to" class="nav-item" active-class="active">
        <span class="icon">{{ item.icon }}</span>
        <span class="label">{{ item.label }}</span>
      </RouterLink>
    </nav>
  </aside>
</template>

<script setup>
const menu = [
  { id: 'dashboard', label: '仪表盘', icon: '📊', to: '/dashboard' },
  { id: 'projects', label: '项目', icon: '📁', to: '/projects' },
  { id: 'tasks', label: '任务', icon: '✅', to: '/tasks' },
  { id: 'team', label: '团队', icon: '👥', to: '/team' },
  { id: 'settings', label: '设置', icon: '⚙️', to: '/settings' }
]
</script>

<style scoped>
.sidebar{width:240px;background:#0f172a;color:white;padding:20px;display:flex;flex-direction:column}
.brand{font-weight:700;margin-bottom:20px}
.nav{display:flex;flex-direction:column;gap:6px}
.nav-item{display:flex;align-items:center;gap:10px;padding:10px;border-radius:8px;color:white;text-decoration:none}
.nav-item:hover{background:rgba(255,255,255,0.1)}
.active{background:rgba(255,255,255,0.15)}
.icon{width:28px;text-align:center}
</style>
