<template>
  <aside
    :class="['sidebar', { collapsed, hoverExpand }]"
  >
    <nav>
      <RouterLink to="/" class="link" active-class="active">
        <span class="icon">
          <i :class="isDark ? 'home-dark' : 'home-light'"></i>
        </span>
        <span
          class="text"
          :class="{ hidden: collapsed && !hoverExpand }"
        >首页</span>
      </RouterLink>

      <RouterLink to="/rss" class="link" active-class="active">
        <span class="icon">
          <i :class="isDark ? 'rss-dark' : 'rss-light'"></i>
        </span>
        <span
          class="text"
          :class="{ hidden: collapsed && !hoverExpand }"
        >RSS</span>
      </RouterLink>

      <RouterLink to="/settings" class="link" active-class="active">
        <span class="icon">
          <i :class="isDark ? 'settings-dark' : 'settings-light'"></i>
        </span>
        <span
          class="text"
          :class="{ hidden: collapsed && !hoverExpand }"
        >设置</span>
      </RouterLink>

      <RouterLink to="/about" class="link" active-class="active">
        <span class="icon">
          <i :class="isDark ? 'about-dark' : 'about-light'"></i>
        </span>
        <span
          class="text"
          :class="{ hidden: collapsed && !hoverExpand }"
        >关于</span>
      </RouterLink>
    </nav>

    <button class="collapse-btn" @click="$emit('toggleCollapse')">
      {{ collapsed ? '>' : '<' }}
    </button>
  </aside>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

defineProps({
  collapsed: Boolean, 
  isDark: Boolean
})

const hoverExpand = ref(false)

</script>

<style scoped>
.sidebar {
  position: sticky;
  top: 12px;
  margin: 12px 0 12px 12px;
  width: 200px;
  min-width: 60px;
  height: calc(100vh - 68px);
  background-color: var(--sidebar-bg);
  border-radius: 12px;
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.sidebar.collapsed {
  width: 60px;
}

nav {
  display: flex;
  flex-direction: column;
  padding: 8px;
}

.link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  text-decoration: none;
  color: var(--text);
  border-radius: 8px;
  margin: 4px 0;
  transition: background-color 0.25s, padding 0.25s;
}

/* 收起状态下图标居中 */
.sidebar.collapsed .link {
  justify-content: center;
  gap: 0;
}

.link:hover {
  background-color: var(--hover);
}

.active {
  background-color: var(--hover);
  border-radius: 8px;
  margin-left: 4px;
  margin-right: 4px;
  transition: background-color 0.3s, margin 0.3s;
  font-weight: bold;
}

/* 固定 icon 区域宽度，防止跳动 */
.icon {
  width: 24px;
  text-align: center;
  font-size: 18px;
  flex-shrink: 0;
}

/* home的亮暗切换 */
.home-light,
.home-dark {
  display: inline-block;
  width: 25px;
  height: 25px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  vertical-align: bottom;
}
.home-light {
  background-image: url('../assets/home-light.svg');
}
.home-dark {
  background-image: url('../assets/home-dark.svg');
}

/* about的亮暗切换 */
.about-light,
.about-dark {
  display: inline-block;
  width: 25px;
  height: 25px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  vertical-align: bottom;
}
.about-light {
  background-image: url('../assets/about-light.svg');
}
.about-dark {
  background-image: url('../assets/about-dark.svg');
}

/* matrix的亮暗切换 */
.rss-light,
.rss-dark {
  display: inline-block;
  width: 25px;
  height: 25px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  vertical-align: bottom;
}
.rss-light {
  background-image: url('../assets/link-light.svg');
}
.rss-dark {
  background-image: url('../assets/link-dark.svg');
}

/* setting的亮暗切换 */
.settings-light,
.settings-dark {
  display: inline-block;
  width: 25px;
  height: 25px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  vertical-align: bottom;
}
.settings-light {
  background-image: url('../assets/settings-light.svg');
}
.settings-dark {
  background-image: url('../assets/settings-dark.svg');
}

/* 文本淡入淡出 + 完全移除占位 */
.text {
  opacity: 1;
  width: 120px;
  overflow: hidden;
  white-space: nowrap;
  transition: opacity 0.25s ease, width 0.25s ease;
}

.text.hidden {
  opacity: 0;
  width: 0;
  overflow: hidden;
}

/* 收起按钮 */
.collapse-btn {
  background: none;
  border: none;
  padding: 12px;
  cursor: pointer;
  color: var(--text);
  transition: transform 0.3s;
}

.collapse-btn:hover {
  transform: scale(1.1);
}
</style>
