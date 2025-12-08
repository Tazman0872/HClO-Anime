<template>
  <div class="bg-gray-50 min-h-screen py-10 px-5">
    <div class="max-w-3xl mx-auto bg-white p-8 rounded-2xl shadow-lg border border-gray-100">
      <h2 class="text-2xl font-bold mb-6 text-gray-800">RSS 源管理</h2>

      <!-- 添加 RSS -->
      <AddRssForm
        v-model="newRssLink"
        :loading="adding"
        @submit="addRss"
      />

      <!-- 状态提示 -->
      <StatusBar :loading="loading" :error="error" />

      <!-- 列表 -->
      <RssList
        class="mt-6"
        :items="rssList"
        :loading="deleting"
        @remove="removeRss"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

import AddRssForm from '../components/AddRssForm.vue'
import StatusBar from '../components/StatusBar.vue'
import RssList from '../components/RssList.vue'

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
    const res = await axios.get(`${API_BASE}/list`)
    rssList.value = res.data
  } catch (err: any) {
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
  } catch (err: any) {
    error.value = `添加失败: ${err.response?.data?.detail || err.message}`
  } finally {
    adding.value = false
  }
}

const removeRss = async (link: string) => {
  if (!confirm(`确定要删除 \"${link}\" 吗？`)) return

  deleting.value = true
  error.value = ''
  try {
    await axios.delete(`${API_BASE}/remove`, {
      params: { rss_link: link.trim() }
    })
    await fetchRssList()
  } catch (err: any) {
    error.value = `删除失败: ${err.response?.data?.detail || err.message}`
  } finally {
    deleting.value = false
  }
}

onMounted(fetchRssList)
</script>
