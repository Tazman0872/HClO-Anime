<template>
  <form @submit.prevent="emitSubmit" class="flex gap-3 mb-6 w-full">
    <input
      v-model="modelValueProxy"
      type="url"
      placeholder="请输入 RSS 链接（如 https://mikanani.me/RSS/...）"
      required
      class="flex-1 p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-400 focus:border-blue-400 transition"
    />
    <button
      type="submit"
      :disabled="loading"
      class="px-4 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 shadow-md"
    >添加</button>
  </form>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue: string
  loading?: boolean
}

const props = defineProps<Props>()
const emit = defineEmits(['update:modelValue', 'submit'])

const modelValueProxy = computed({
  get: () => props.modelValue,
  set: v => emit('update:modelValue', v)
})

const emitSubmit = () => emit('submit')
</script>