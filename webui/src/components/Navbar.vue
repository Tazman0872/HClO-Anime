<template>
  <header class="navbar">
    <div class="logo">
      <img src="../assets/HClO.png" alt="Logo" />
      <span>| Hypochlorous服务站</span>
    </div>
    <button class="dark-toggle" @click="$emit('toggleDark')">
      <i :class="isDark ? 'icon-sun' : 'icon-moon'"></i>
    </button>
  </header>
</template>

<script setup>
defineProps({
  isDark: Boolean
})
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px; /* ✅ 增加纵向高度 */
  padding: 0 1rem;
  background-color: var(--navbar-bg);
  color: var(--text);
  transition: background-color 0.3s;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1)
}

.logo {
  display: flex;
  align-items: center;
  gap: 4px;
}

.logo img {
  height: 30px; /* ✅ 调整图标高度以匹配新 navbar 高度 */
}

.logo span {
  font-size: 22px; /* ✅ 增大文字大小 */
  font-weight: 500; /* 可选：加粗文字提升可读性 */
  color: var(--text);
}

.icon-sun,
.icon-moon {
  display: inline-block;
  width: 25px;
  height: 25px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  vertical-align: bottom;
}

.icon-sun {
  background-image: url('../assets/sun.svg');
}

.icon-moon {
  background-image: url('../assets/moon.svg');
}

.dark-toggle {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  color: var(--text);
}
</style>