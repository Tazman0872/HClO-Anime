<template>
  <div>
    <p v-if="loading" class="text-gray-600 text-sm mb-4">加载中...</p>
    <p v-if="error" class="text-red-500 mb-4">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  loading: boolean
  error: string
}

defineProps<Props>()
</script>

<style scoped></style>
