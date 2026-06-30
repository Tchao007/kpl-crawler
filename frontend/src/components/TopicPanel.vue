<script setup lang="ts">
defineProps<{
  hint: string;
  result: string;
  busy: boolean;
}>();

const emit = defineEmits<{
  loadLatest: [];
  crawl: [];
}>();
</script>

<template>
  <section class="topic-panel">
    <div class="panel-head">
      <strong>题材库快照</strong>
      <div class="hint">{{ hint }}</div>
    </div>
    <div class="topic-body">
      <div class="topic-actions">
        <button class="btn primary" type="button" :disabled="busy" @click="emit('crawl')">
          {{ busy ? "爬取中" : "爬取题材库" }}
        </button>
        <button class="btn ghost" type="button" @click="emit('loadLatest')">查看最近结果</button>
      </div>
      <pre class="topic-result">{{ result || "暂无结果" }}</pre>
    </div>
  </section>
</template>
