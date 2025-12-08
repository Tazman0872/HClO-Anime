<template>
  <div class="home-root">
    <h1 class="page-title">任务控制面板</h1>

    <div class="home-grid">
      <section class="proc-card">
        <div class="card-head">
          <h2>解析器 (Parser)</h2>
          <span :class="['status-badge', parsing ? 'running' : 'idle']">{{ parsing ? '运行中' : '空闲' }}</span>
        </div>
        <p class="card-desc">触发并监控解析任务。解析正在运行时会禁用启动按钮。</p>

        <div class="card-actions">
          <button class="btn" :disabled="parsing || parsingLoading" @click="startParsing">
            {{ parsingLoading ? '启动中...' : '开始解析' }}
          </button>
        </div>
      </section>

      <section class="proc-card">
        <div class="card-head">
          <h2>下载器 (Downloader)</h2>
          <span :class="['status-badge', downloading ? 'running' : 'idle']">{{ downloading ? '运行中' : '空闲' }}</span>
        </div>
        <p class="card-desc">触发并监控下载任务。下载正在运行时会禁用启动按钮。</p>

        <div class="card-actions">
          <button class="btn" :disabled="downloading || downloadingLoading" @click="startDownloading">
            {{ downloadingLoading ? '启动中...' : '开始下载' }}
          </button>
        </div>
      </section>
    </div>

    <div class="notice" v-if="message">{{ message }}</div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

const parsing = ref(false)
const parsingLoading = ref(false)
const downloading = ref(false)
const downloadingLoading = ref(false)
const message = ref('')

let pollId: number | null = null

const fetchStatuses = async () => {
  try {
    const [p, d] = await Promise.all([
      axios.get(`${API_BASE}/parser/status`),
      axios.get(`${API_BASE}/downloader/status`),
    ])
    parsing.value = !!p.data?.is_parsing
    downloading.value = !!d.data?.is_downloading
  } catch (err: any) {
    // ignore transient errors but show a brief message
    message.value = err?.message || '无法获取状态'
    setTimeout(() => (message.value = ''), 2500)
  }
}

const startParsing = async () => {
  parsingLoading.value = true
  message.value = ''
  try {
    await axios.post(`${API_BASE}/parser/main`)
    message.value = '解析任务已启动'
  } catch (err: any) {
    message.value = err.response?.data?.detail || err.message || '启动解析失败'
  } finally {
    parsingLoading.value = false
    await fetchStatuses()
  }
}

const startDownloading = async () => {
  downloadingLoading.value = true
  message.value = ''
  try {
    await axios.post(`${API_BASE}/downloader/main`)
    message.value = '下载任务已启动'
  } catch (err: any) {
    message.value = err.response?.data?.detail || err.message || '启动下载失败'
  } finally {
    downloadingLoading.value = false
    await fetchStatuses()
  }
}

onMounted(() => {
  fetchStatuses()
  pollId = window.setInterval(fetchStatuses, 3000)
})

onUnmounted(() => {
  if (pollId) {
    clearInterval(pollId)
    pollId = null
  }
})
</script>

<style scoped>
.home-root {
  padding: 12px;
}
.page-title {
  font-size: 20px;
  margin-bottom: 18px;
}
.home-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 16px;
}
.proc-card {
  background: var(--navbar-bg, #fff);
  border: 1px solid var(--divider, #ddd);
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(2,6,23,0.04);
}
.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.status-badge {
  padding: 4px 8px;
  border-radius: 999px;
  font-size: 12px;
  color: #fff;
}
.status-badge.running { background: var(--hover, #2ecc71); }
.status-badge.idle { background: rgba(120,120,120,0.5); }
.card-desc { color: var(--text); margin: 10px 0 12px; }
.card-actions { display:flex; gap:10px; }
.btn { padding: 8px 14px; border-radius: 8px; border: none; cursor: pointer; background: var(--hover); color: #fff; }
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
.notice { margin-top: 14px; color: var(--text); }

@media (max-width: 420px) {
  .page-title { font-size: 18px; }
}
</style>
