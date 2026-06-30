<script setup lang="ts">
import { computed, reactive, watch } from "vue";
import type { LevelOption, Scenario, User } from "../api/scenarios";
import { buildRequestUrl } from "../api/scenarios";

const props = defineProps<{
  item: Scenario;
  user: User | null;
  levelOptions: LevelOption[];
  busy: boolean;
  nameBusy: boolean;
}>();

const emit = defineEmits<{
  call: [item: Scenario];
  saveName: [
    item: Scenario,
    payload: { title: string; title_cn: string; maintenance_time: string; level: string }
  ];
}>();

const form = reactive({
  title: props.item.title,
  title_cn: props.item.titleCn,
  maintenance_time: props.item.maintenanceTime,
  level: props.item.level
});

watch(
  () => props.item,
  (item) => {
    form.title = item.title;
    form.title_cn = item.titleCn;
    form.maintenance_time = item.maintenanceTime;
    form.level = item.level;
  },
  { deep: true }
);

const fallbackLevels: LevelOption[] = [
  { value: "normal", label: "一般" },
  { value: "important", label: "重要" },
  { value: "rare", label: "稀缺" },
  { value: "pending_delete", label: "待删除" }
];

const paramEntries = computed(() => Object.entries(props.item.params || {}).slice(0, 6));
const dataEntries = computed(() => Object.entries(props.item.data || {}).slice(0, 6));
</script>

<template>
  <article class="card api-card">
    <div class="api-card-head">
      <div>
        <div class="api-kicker">
          <span class="method" :class="item.httpMethod === 'GET' ? 'get' : 'post'">{{ item.httpMethod }}</span>
          <span>session {{ item.sessionId }}</span>
          <span>{{ item.host || "unknown host" }}</span>
        </div>
        <h3 class="title">
          <span>{{ item.title }}</span>
          <span v-if="item.titleCn" class="title-cn">{{ item.titleCn }}</span>
        </h3>
      </div>
      <span class="tag" :class="`level-${item.level}`">{{ item.levelLabel }}</span>
    </div>

    <div class="endpoint-row">
      <span>接口地址</span>
      <code>{{ item.endpoint || item.aliasEndpoint }}</code>
    </div>
    <div class="endpoint-row muted-row">
      <span>调试 URL</span>
      <code>{{ buildRequestUrl(item) }}</code>
    </div>

    <div class="api-grid">
      <div>
        <div class="mini-title">Query 参数</div>
        <dl v-if="paramEntries.length" class="param-list">
          <template v-for="[key, value] in paramEntries" :key="key">
            <dt>{{ key }}</dt>
            <dd>{{ value }}</dd>
          </template>
        </dl>
        <div v-else class="empty-mini">无</div>
      </div>
      <div>
        <div class="mini-title">Body 参数</div>
        <dl v-if="dataEntries.length" class="param-list">
          <template v-for="[key, value] in dataEntries" :key="key">
            <dt>{{ key }}</dt>
            <dd>{{ value }}</dd>
          </template>
        </dl>
        <div v-else class="empty-mini">无</div>
      </div>
    </div>

    <div v-if="user?.role === 'admin'" class="name-editor">
      <label>
        <span>英文名</span>
        <input v-model.trim="form.title" type="text" autocomplete="off" />
      </label>
      <label>
        <span>中文名</span>
        <input v-model.trim="form.title_cn" type="text" autocomplete="off" />
      </label>
      <label>
        <span>维护时间</span>
        <input v-model.trim="form.maintenance_time" type="text" placeholder="例如 2026-06-25" autocomplete="off" />
      </label>
      <label>
        <span>分级</span>
        <select v-model="form.level">
          <option v-for="level in levelOptions.length ? levelOptions : fallbackLevels" :key="level.value" :value="level.value">
            {{ level.label }}
          </option>
        </select>
      </label>
      <button
        class="tiny"
        type="button"
        :disabled="nameBusy"
        @click="emit('saveName', item, { ...form })"
      >
        {{ nameBusy ? "保存中" : "保存" }}
      </button>
    </div>

    <div class="actions">
      <button class="tiny primary" type="button" :disabled="busy" @click="emit('call', item)">
        {{ busy ? "调用中" : "调用接口" }}
      </button>
      <a class="tiny" :href="buildRequestUrl(item)" target="_blank" rel="noreferrer">打开 URL</a>
    </div>
  </article>
</template>
