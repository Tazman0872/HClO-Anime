<template>
  <div class="config-card">
    <h3 class="card-title">{{ title }}</h3>
    <div class="card-body">
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string;
}
const props = defineProps<Props>();
</script>

<style scoped>
.config-card {
  border: 1px solid var(--divider, #ddd);
  padding: 18px;
  border-radius: 10px;
  margin-bottom: 22px;
  background: var(--navbar-bg, #fff);
  box-shadow: 0 2px 6px rgba(2,6,23,0.04);
}
.card-title {
  margin-bottom: 14px;
  font-size: 18px;
  font-weight: 600;
}
.card-body {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
</style>