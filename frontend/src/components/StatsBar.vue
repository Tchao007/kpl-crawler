<script setup lang="ts">
import type { Scenario } from "../api/scenarios";

const props = defineProps<{
  items: Scenario[];
  currentGroup: string;
}>();
</script>

<template>
  <div class="stats">
    <div class="stat">
      <div class="label">接口总数</div>
      <div class="value">{{ props.items.length }}</div>
    </div>
    <div class="stat">
      <div class="label">域名数量</div>
      <div class="value">{{ new Set(props.items.map((item) => item.host).filter(Boolean)).size }}</div>
    </div>
    <div class="stat">
      <div class="label">分类数量</div>
      <div class="value">{{ new Set(props.items.map((item) => item.group)).size }}</div>
    </div>
    <div class="stat">
      <div class="label">当前目录</div>
      <div class="value">{{ props.currentGroup }}</div>
    </div>
  </div>
</template>
