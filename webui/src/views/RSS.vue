<template>
  <div class="rss-manager bg-gray-50 min-h-screen py-10 px-5">
    <div class="max-w-3xl mx-auto bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
      <h2 class="text-2xl font-bold mb-6 text-gray-800">RSS 源管理</h2>

      <!-- 添加 RSS 表单 -->
      <form @submit.prevent="addRss" class="flex gap-3 mb-6">
        <input
          v-model="newRssLink"
          type="url"
          placeholder="请输入 RSS 链接（如 https://mikanani.me/RSS/...）"
          required
          class="flex-1 p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition"
        />
        <button
          type="submit"
          :disabled="adding"
          class="px-4 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 shadow-md"
        >添加</button>
      </form>

      <!-- 加载状态 -->
      <p v-if="loading" class="text-gray-600 text-sm mb-4">加载中...</p>

      <!-- 错误提示 -->
      <p v-if="error" class="text-red-500 mb-4">{{ error }}</p>

      <!-- RSS 列表 -->
      <ul v-if="rssList.length > 0" class="space-y-3">
        <li
          v-for="item in rssList"
          :key="item.id"
          class="flex justify-between items-center p-4 bg-gray-100 rounded-xl border border-gray-200 hover:bg-gray-200 transition"
        >
          <div class="text-gray-800">
            <strong class="text-lg">{{ item.bangumi_name }}</strong><br />
            <small class="text-gray-600">{{ item.link.trim() }}</small>
          </div>
          <button
            @click="removeRss(item.link)"
            :disabled="deleting"
            class="px-3 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600 disabled:opacity-50 shadow"
          >删除</button>
        </li>
      </ul>

      <p v-else class="text-gray-500">暂无 RSS 源</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/rss'

const newRssLink = ref('')
const rssList = ref([])
const loading = ref(false)
const error = ref('')
const adding = ref(false)
const deleting = ref(false)

const fetchRssList = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await axios.get(`${API_BASE}/list`)
    rssList.value = response.data
  } catch (err) {
    error.value = `加载失败: ${err.message}`
  } finally {
    loading.value = false
  }
}

const addRss = async () => {
  adding.value = true
  error.value = ''
  try {
    await axios.post(`${API_BASE}/add`, null, {
      params: { rss_link: newRssLink.value.trim() }
    })
    newRssLink.value = ''
    await fetchRssList()
  } catch (err) {
    error.value = `添加失败: ${err.response?.data?.detail || err.message}`
  } finally {
    adding.value = false
  }
}

const removeRss = async (link) => {
  if (!confirm(`确定要删除 "${link}" 吗？`)) return

  deleting.value = true
  error.value = ''
  try {
    await axios.delete(`${API_BASE}/remove`, {
      params: { rss_link: link.trim() }
    })
    await fetchRssList()
  } catch (err) {
    error.value = `删除失败: ${err.response?.data?.detail || err.message}`
  } finally {
    deleting.value = false
  }
}

onMounted(fetchRssList)
</script>

<style scoped>
/* 这里保留空白，你可以按需求加入更多样式扩展 */
</style>
