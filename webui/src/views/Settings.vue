<template>
  <div class="config-container">
    <h2 class="title">系统配置管理</h2>

    <div class="config-grid">
      <ConfigCard title="数据库配置">
        <FormInput label="主机地址" v-model="form.database.host" />
        <FormInput label="数据库名" v-model="form.database.database" />
        <FormInput label="用户名" v-model="form.database.user" />
        <FormInput label="密码" type="password" v-model="form.database.password" />
        <FormInput label="端口" v-model="form.database.port" />
      </ConfigCard>

      <ConfigCard title="OpenAI 配置">
        <FormInput label="Base URL" v-model="form.openai.base_url" />
        <FormInput label="模型名称" v-model="form.openai.model_name" />
        <FormInput label="API Key" type="password" v-model="form.openai.api_key" />
      </ConfigCard>

      <ConfigCard title="qBittorrent 配置">
        <FormInput label="主机地址" v-model="form.qbittorrent.host" />
        <FormInput label="用户名" v-model="form.qbittorrent.user" />
        <FormInput label="密码" type="password" v-model="form.qbittorrent.password" />
        <FormInput label="路径前缀 (如 /bangumi/)" v-model="form.qbittorrent.path_prefix" />
      </ConfigCard>

      <ConfigCard title="过滤器设置">
        <div class="checkbox-row">
          <label><input type="checkbox" v-model="form.filter.hasCHS" /> 包含简体中文</label>
          <label><input type="checkbox" v-model="form.filter.hasCHT" /> 包含繁体中文</label>
        </div>
        <div class="subtype-box">
          <div class="sub-title">字幕类型:</div>
          <label v-for="opt in SUBTYPE_OPTIONS" :key="opt" class="subtype-item">
            <input type="checkbox" :value="opt" v-model="form.filter.subtype" /> {{ opt }}
          </label>
        </div>
      </ConfigCard>
    </div>

    <div class="btn-row">
      <button class="btn save" @click="saveAll">保存全部配置</button>
      <button class="btn reload" @click="loadAll">重新加载配置</button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="message" class="message">{{ message }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

import ConfigCard from '../components/ConfigCard.vue';
import FormInput from '../components/FormInput.vue';

// === 类型定义 ===
interface DatabaseConfig {
  host: string;
  database: string;
  user: string;
  password: string;
  port: string;
}

interface OpenAIConfig {
  base_url: string;
  model_name: string;
  api_key: string;
}

interface QBittorrentConfig {
  host: string;
  user: string;
  password: string;
  path_prefix: string;
}

interface FilterConfig {
  hasCHS: boolean;
  hasCHT: boolean;
  subtype: string[];
}

interface ConfigForm {
  database: DatabaseConfig;
  openai: OpenAIConfig;
  qbittorrent: QBittorrentConfig;
  filter: FilterConfig;
}

// === 常量 ===
const SUBTYPE_OPTIONS = ['HRD', 'SFT', 'EXT', 'UKN'] as const;
// Use relative paths so requests route through nginx proxy to internal backend
const API_BASE = '';

// === 响应式状态 ===
const form = ref<ConfigForm>({
  database: { host: '', database: '', user: '', password: '', port: '' },
  openai: { base_url: '', model_name: '', api_key: '' },
  qbittorrent: { host: '', user: '', password: '', path_prefix: '' },
  filter: { hasCHS: false, hasCHT: false, subtype: [] },
});

const loading = ref(false);
const message = ref('');

// === 工具函数：安全获取/设置嵌套对象值 ===
function getIn(obj: any, path: string): any {
  return path.split('.').reduce((current, key) => current?.[key], obj);
}

function setIn(obj: any, path: string, value: any): void {
  const keys = path.split('.');
  const lastKey = keys.pop()!;
  let current = obj;
  for (const key of keys) {
    if (current[key] === undefined) current[key] = {};
    current = current[key];
  }
  current[lastKey] = value;
}

// === 配置结构元数据（用于自动加载/保存）===
const CONFIG_SCHEMA: Record<string, any> = {
  database: {
    host: String,
    database: String,
    user: String,
    password: String,
    port: String,
  },
  openai: {
    base_url: String,
    model_name: String,
    api_key: String,
  },
  qbittorrent: {
    host: String,
    user: String,
    password: String,
    path_prefix: String,
  },
  filter: {
    hasCHS: Boolean,
    hasCHT: Boolean,
    subtype: Array,
  },
};

// === 递归生成所有扁平化 key ===
function flattenKeys(obj: Record<string, any>, prefix = ''): string[] {
  let keys: string[] = [];
  for (const [key, value] of Object.entries(obj)) {
    const fullPath = prefix ? `${prefix}.${key}` : key;
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      keys = keys.concat(flattenKeys(value, fullPath));
    } else {
      keys.push(fullPath);
    }
  }
  return keys;
}

const CONFIG_KEYS = flattenKeys(CONFIG_SCHEMA);

// === API 方法 ===
async function getSetting(key: string) {
  const res = await axios.get(`${API_BASE}/settings/get`, { params: { configName: key } });
  return res.data;
}

async function setSetting(key: string, value: any) {
  await axios.post(`${API_BASE}/settings/set`, { configName: key, configValue: value });
}

// === 加载全部配置 ===
async function loadAll() {
  loading.value = true;
  message.value = '';
  try {
    for (const key of CONFIG_KEYS) {
      let value = await getSetting(key);
      // 特殊处理数组（避免后端返回 null/undefined）
      if (key === 'filter.subtype') {
        value = Array.isArray(value) ? value : [];
      }
      setIn(form.value, key, value);
    }
  } catch (err) {
    console.error('加载配置失败:', err);
    message.value = '❌ 加载配置失败，请检查网络或后端服务。';
    setTimeout(() => (message.value = ''), 5000);
  } finally {
    loading.value = false;
  }
}

// === 保存全部配置 ===
async function saveAll() {
  message.value = '';
  try {
    for (const key of CONFIG_KEYS) {
      const value = getIn(form.value, key);
      await setSetting(key, value);
    }
    message.value = '✅ 配置已成功保存！';
    setTimeout(() => (message.value = ''), 3000);
  } catch (err) {
    console.error('保存配置失败:', err);
    message.value = '❌ 保存失败，请重试。';
    setTimeout(() => (message.value = ''), 5000);
  }
}

// === 初始化 ===
onMounted(loadAll);
</script>

<style scoped>
/* 样式保持不变，可直接复用 */
.config-container {
  max-width: 760px;
  margin: 0 auto;
  padding: 20px;
  font-family: Inter, Arial, sans-serif;
}
.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 18px;
  align-items: start;
  margin-bottom: 14px;
}
.title {
  text-align: center;
  margin-bottom: 28px;
  font-size: 24px;
  font-weight: 600;
}
.btn-row {
  text-align: center;
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 16px;
}
.btn {
  padding: 10px 22px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 15px;
  transition: 0.2s;
}
.btn.save {
  background-color: var(--hover, #4caf50);
  color: white;
}
.btn.reload {
  background-color: var(--sidebar-bg, #2196f3);
  color: var(--text, #fff);
}
.btn:hover {
  opacity: 0.9;
}
.loading {
  color: var(--text, #777);
  text-align: center;
  margin-top: 16px;
}
.message {
  color: var(--hover, green);
  text-align: center;
  margin-top: 16px;
  font-weight: 500;
}
.checkbox-row {
  display: flex;
  gap: 20px;
  margin-bottom: 12px;
}
.subtype-box {
  margin-top: 10px;
}
.sub-title {
  font-weight: 500;
  margin-bottom: 6px;
}
.subtype-item {
  margin-right: 14px;
}
</style>