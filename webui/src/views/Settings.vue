<template>
  <div class="config-container">
    <h2 class="title">系统配置管理</h2>

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
        <label v-for="opt in ['HRD', 'SFT', 'EXT', 'UKN']" :key="opt" class="subtype-item">
          <input type="checkbox" :value="opt" v-model="form.filter.subtype" /> {{ opt }}
        </label>
      </div>
    </ConfigCard>

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

interface ConfigForm {
  database: { host: string; database: string; user: string; password: string; port: string };
  openai: { base_url: string; model_name: string; api_key: string };
  qbittorrent: { host: string; user: string; password: string; path_prefix: string };
  filter: { hasCHS: boolean; hasCHT: boolean; subtype: string[] };
}

const form = ref<ConfigForm>({
  database: { host: '', database: '', user: '', password: '', port: '' },
  openai: { base_url: '', model_name: '', api_key: '' },
  qbittorrent: { host: '', user: '', password: '', path_prefix: '' },
  filter: { hasCHS: false, hasCHT: false, subtype: [] },
});

const loading = ref(false);
const message = ref('');
const API_BASE = 'http://localhost:8000';

async function getSetting(key: string) {
  const res = await axios.get(`${API_BASE}/settings/get`, { params: { configName: key } });
  return res.data;
}

async function setSetting(key: string, value: any) {
  await axios.post(`${API_BASE}/settings/set`, { configName: key, configValue: value });
}

async function loadAll() {
  loading.value = true;
  message.value = '';
  try {
    const keys = [
      'database.host', 'database.database', 'database.user', 'database.password', 'database.port',
      'openai.base_url', 'openai.model_name', 'openai.api_key',
      'qbittorrent.host', 'qbittorrent.user', 'qbittorrent.password', 'qbittorrent.path_prefix',
      'filter.hasCHS', 'filter.hasCHT', 'filter.subtype',
    ];

    for (const key of keys) {
      const value = await getSetting(key);
      const parts = key.split('.');
      let t: any = form.value;
      for (let i = 0; i < parts.length - 1; i++) t = t[parts[i]];

      const last = parts[parts.length - 1];
      if (key === 'filter.subtype') t[last] = Array.isArray(value) ? value : [];
      else t[last] = value;
    }
  } finally {
    loading.value = false;
  }
}

async function saveAll() {
  const keys = [
    'database.host', 'database.database', 'database.user', 'database.password', 'database.port',
    'openai.base_url', 'openai.model_name', 'openai.api_key',
    'qbittorrent.host', 'qbittorrent.user', 'qbittorrent.password', 'qbittorrent.path_prefix',
    'filter.hasCHS', 'filter.hasCHT', 'filter.subtype',
  ];

  for (const key of keys) {
    const parts = key.split('.');
    let val: any = form.value;
    for (const p of parts) val = val[p];
    await setSetting(key, val);
  }
  message.value = '✅ 配置已成功保存！';
  setTimeout(() => (message.value = ''), 3000);
}

onMounted(loadAll);
</script>

<style scoped>
.config-container {
  max-width: 760px;
  margin: 0 auto;
  padding: 20px;
  font-family: Inter, Arial, sans-serif;
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
  background-color: #4caf50;
  color: white;
}
.btn.reload {
  background-color: #2196f3;
  color: white;
}
.btn:hover {
  opacity: 0.9;
}
.loading {
  color: #777;
  text-align: center;
  margin-top: 16px;
}
.message {
  color: green;
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