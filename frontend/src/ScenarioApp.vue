<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { logout } from "./api/auth";
import {
  callScenario,
  loadScenarios,
  normalizeScenario,
  saveScenarioMeta,
  type LevelOption,
  type Scenario,
  type User
} from "./api/scenarios";
import FiltersBar from "./components/FiltersBar.vue";
import ScenarioCard from "./components/ScenarioCard.vue";
import StatsBar from "./components/StatsBar.vue";
import Topbar from "./components/Topbar.vue";

const scenarios = ref<Scenario[]>([]);
const levelOptions = ref<LevelOption[]>([]);
const user = ref<User | null>(null);
const group = ref("全部");
const host = ref("all");
const query = ref("");
const loading = ref(false);
const loadingText = ref("准备加载");
const busyId = ref<string | null>(null);
const nameBusyId = ref<string | null>(null);
const toast = ref("");
const toastType = ref<"success" | "error">("success");

let toastTimer = 0;

const groups = computed(() => ["全部", ...new Set(scenarios.value.map((item) => item.group))]);
const hosts = computed(() => [...new Set(scenarios.value.map((item) => item.host).filter(Boolean))]);
const groupCounts = computed(() => {
  const counts: Record<string, number> = { 全部: scenarios.value.length };
  scenarios.value.forEach((item) => {
    counts[item.group] = (counts[item.group] || 0) + 1;
  });
  return counts;
});

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase();
  return scenarios.value.filter((item) => {
    const matchGroup = group.value === "全部" || item.group === group.value;
    const matchHost = host.value === "all" || item.host === host.value;
    const haystack = [
      item.sessionId,
      item.title,
      item.titleCn,
      item.maintenanceTime,
      item.levelLabel,
      item.methodName,
      item.endpoint,
      item.aliasEndpoint,
      item.host,
      user.value?.role === "admin" ? JSON.stringify(item.params) : "",
      user.value?.role === "admin" ? JSON.stringify(item.data) : ""
    ]
      .join(" ")
      .toLowerCase();
    return matchGroup && matchHost && (!q || haystack.includes(q));
  });
});

const groupedScenarios = computed(() => {
  const map = new Map<string, Scenario[]>();
  filtered.value.forEach((item) => {
    const key = item.group || "其他";
    if (!map.has(key)) map.set(key, []);
    map.get(key)?.push(item);
  });
  return [...map.entries()];
});

function showToast(message: string, type: "success" | "error" = "success") {
  toast.value = message;
  toastType.value = type;
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    toast.value = "";
  }, 1800);
}

async function refreshScenarios() {
  loading.value = true;
  loadingText.value = "正在从 /api/scenarios 拉取接口清单...";
  try {
    const payload = await loadScenarios();
    user.value = payload.user || user.value;
    levelOptions.value = payload.level_options || levelOptions.value;
    scenarios.value = (payload.scenarios || []).map(normalizeScenario);
    loadingText.value = "";
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    loadingText.value = `加载失败：${message}`;
    showToast(`无法获取接口清单：${message}`, "error");
  } finally {
    loading.value = false;
  }
}

async function runScenarioCall(item: Scenario) {
  if (busyId.value) return;
  busyId.value = item.sessionId;
  try {
    const result = await callScenario(item);
    window.alert(`调用完成: ${result.status}\n\n${result.text.slice(0, 900)}`);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    window.alert(`调用失败: ${message}`);
  } finally {
    busyId.value = null;
  }
}

async function runSaveScenarioName(
  item: Scenario,
  payload: { title: string; title_cn: string; maintenance_time: string; level: string }
) {
  if (!payload.title || !payload.title_cn) {
    showToast("中英文名称不能为空", "error");
    return;
  }

  nameBusyId.value = item.sessionId;
  try {
    const updated = normalizeScenario(await saveScenarioMeta(item, payload));
    const index = scenarios.value.findIndex((scenario) => scenario.sessionId === item.sessionId);
    if (index >= 0) {
      scenarios.value[index] = {
        ...scenarios.value[index],
        ...updated,
        endpoint: updated.endpoint || scenarios.value[index].endpoint,
        aliasEndpoint: updated.aliasEndpoint || scenarios.value[index].aliasEndpoint
      };
    }
    showToast("接口管理信息修改成功");
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    showToast(`接口管理信息修改失败：${message}`, "error");
  } finally {
    nameBusyId.value = null;
  }
}

async function copyCurrentList() {
  const text = filtered.value
    .map((item) => `${item.sessionId}\t${item.title}\t${item.titleCn || ""}\t${item.endpoint}`)
    .join("\n");
  await navigator.clipboard.writeText(text);
  showToast("已复制当前列表");
}

onMounted(() => {
  refreshScenarios();
});
</script>

<template>
  <div v-if="toast" class="toast show" :class="{ error: toastType === 'error' }" role="status" aria-live="polite">
    {{ toast }}
  </div>

  <div class="shell">
    <Topbar :user="user" @reload="refreshScenarios" @copy="copyCurrentList" @logout="logout" />

    <main class="doc-shell">
      <FiltersBar
        v-model:group="group"
        v-model:host="host"
        v-model:query="query"
        :groups="groups"
        :hosts="hosts"
        :counts="groupCounts"
      />

      <section class="doc-main">
        <div class="doc-hero">
          <div>
            <div class="eyebrow">API Documentation</div>
            <h1>开盘啦抓包接口文档</h1>
            <p>按业务目录浏览接口，查看调用路径和参数摘要，并在同一页面完成单接口调试。</p>
          </div>
          <StatsBar :items="scenarios" :current-group="group" />
        </div>

        <section class="panel doc-panel">
          <div class="panel-head">
            <div>
              <strong>接口列表</strong>
              <div class="hint">{{ filtered.length }} / {{ scenarios.length }} 个接口匹配当前条件</div>
            </div>
            <div class="hint">{{ loading ? "加载中" : "点击调用按钮可发起一次调试请求" }}</div>
          </div>
          <div v-if="loadingText" class="loading">{{ loadingText }}</div>
          <div v-if="!groupedScenarios.length && !loading" class="empty">没有找到匹配的接口。</div>
          <section v-for="[groupName, items] in groupedScenarios" :key="groupName" class="group">
            <div class="group-title">
              <div>{{ groupName }}</div>
              <span>{{ items.length }} 条</span>
            </div>
            <div class="cards">
              <ScenarioCard
                v-for="item in items"
                :key="item.sessionId"
                :item="item"
                :user="user"
                :level-options="levelOptions"
                :busy="busyId === item.sessionId"
                :name-busy="nameBusyId === item.sessionId"
                @call="runScenarioCall"
                @save-name="runSaveScenarioName"
              />
            </div>
          </section>
        </section>
      </section>
    </main>
  </div>
</template>
