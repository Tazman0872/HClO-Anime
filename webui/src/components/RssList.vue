<template>
  <div class="rss-list-card p-5 bg-white rounded-2xl shadow-lg border border-gray-100">
    <ul v-if="items.length > 0" class="space-y-4">
      <li
        v-for="item in items"
        :key="item.id"
        class="rss-item flex justify-between items-center p-5 bg-white rounded-2xl border border-gray-200 shadow-md hover:shadow-lg transition"
      >
        <div class="text-gray-800">
          <strong class="text-lg">{{ item.bangumi_name }}</strong><br />
          <small class="text-gray-600">{{ item.link.trim() }}</small>
        </div>

        <button
          @click="emitRemove(item.link)"
          :disabled="loading"
          class="px-3 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600 disabled:opacity-50 shadow"
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
.rss-list-card {
  /* 使用全局主题颜色：卡片背景使用导航/卡片背景变量，边框使用分隔线颜色 */
  background: var(--navbar-bg, #ffffff);
  border: 1px solid var(--divider, rgba(0,0,0,0.06));
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(2,6,23,0.06);
}

.rss-item {
  background: transparent;
  border-radius: 8px;
}

/* 当页面使用 .dark 类切换为深色主题时，CSS 变量会自动切换，无需额外媒体查询 */
</style>
