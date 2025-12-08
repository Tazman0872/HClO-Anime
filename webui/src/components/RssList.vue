<template>
  <div class="rss-list-container">
    <ul v-if="items.length > 0" class="rss-grid">
      <li
        v-for="item in items"
        :key="item.id"
        class="rss-item flex"
      >
        <div class="text-gray-800">
          <strong class="text-lg">{{ item.bangumi_name }}</strong><br />
          <small class="text-gray-600">{{ item.link.trim() }}</small>
        </div>

        <button
          @click="emitRemove(item.link)"
          :disabled="loading"
          class="remove-btn px-3 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600 disabled:opacity-50 shadow"
        >删除</button>
      </li>
    </ul>

    <p v-else class="text-gray-500">暂无 RSS 源</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  items: Array<{ id: number; link: string; bangumi_name: string }>
  loading?: boolean
}

const props = defineProps<Props>()
const emit = defineEmits(['remove'])

const emitRemove = (link: string) => emit('remove', link)
</script>

<style scoped>
.rss-list-container {
  /* 容器不再有卡片样式，保留默认间距（可根据需要调整） */
  width: 100%;
}

/* 列表使用响应式网格；当宽度允许时每行显示两个项目 */
.rss-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 16px;
  list-style: none;
  padding: 0;
  margin: 0;
}

.rss-item {
  display: flex;
  align-items: center;
  background: var(--sidebar-bg);
  border: 1px solid var(--divider, rgba(0,0,0,0.06));
  border-radius: 10px;
  padding: 16px;
  box-shadow: 0 6px 18px rgba(2,6,23,0.04);
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}

.rss-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 24px rgba(2,6,23,0.08);
}

.rss-item > .text-gray-800 {
  /* 文本区域允许换行并占据剩余空间 */
  flex: 1 1 auto;
  min-width: 0;
}

.remove-btn {
  /* 将删除按钮推到文本右侧 */
  margin-left: 12px;
  flex: 0 0 auto;
  align-self: center;
}

/* 在较小屏幕上略微减小卡片内边距 */
@media (max-width: 420px) {
  .rss-item {
    padding: 12px;
  }
}

</style>
