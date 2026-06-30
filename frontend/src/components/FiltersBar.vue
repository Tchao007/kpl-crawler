<script setup lang="ts">
defineProps<{
  groups: string[];
  hosts: string[];
  group: string;
  host: string;
  query: string;
  counts?: Record<string, number>;
}>();

const emit = defineEmits<{
  "update:group": [value: string];
  "update:host": [value: string];
  "update:query": [value: string];
}>();
</script>

<template>
  <aside class="doc-sidebar">
    <div class="sidebar-section">
      <div class="sidebar-title">接口检索</div>
      <input
        class="search"
        type="search"
        placeholder="搜索接口、session、域名"
        :value="query"
        @input="emit('update:query', ($event.target as HTMLInputElement).value)"
      />
      <select class="select" :value="host" @change="emit('update:host', ($event.target as HTMLSelectElement).value)">
        <option value="all">全部域名</option>
        <option v-for="item in hosts" :key="item" :value="item">{{ item }}</option>
      </select>
    </div>

    <div class="sidebar-section">
      <div class="sidebar-title">接口分类</div>
      <button
        v-for="item in groups"
        :key="item"
        class="side-link"
        :class="{ active: item === group }"
        type="button"
        @click="emit('update:group', item)"
      >
        <span>{{ item }}</span>
        <em>{{ counts?.[item] ?? 0 }}</em>
      </button>
    </div>
  </aside>
</template>
