<template>
  <div class="form-input">
    <label class="form-label">{{ label }}</label>
    <input
      :type="type"
      class="form-field"
      v-model="modelValueProxy"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  label: string;
  modelValue: string | number;
  type?: string;
}

const props = defineProps<Props>();
const emit = defineEmits(['update:modelValue']);

const modelValueProxy = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
});
</script>

<style scoped>
.form-input {
  display: flex;
  flex-direction: column;
}

.form-label {
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
}

.form-field {
  padding: 8px 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  transition: 0.2s;
}

.form-field:focus {
  outline: none;
  border-color: #2196f3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
}
</style>
