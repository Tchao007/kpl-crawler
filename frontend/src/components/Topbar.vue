<script setup lang="ts">
import type { User } from "../api/scenarios";

defineProps<{
  user: User | null;
}>();

const emit = defineEmits<{
  reload: [];
  copy: [];
  logout: [];
}>();
</script>

<template>
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="/">
        <span class="brand-mark">K</span>
        <span>
          <strong>KPL API Console</strong>
          <small>开盘啦接口文档与调试台</small>
        </span>
      </a>

      <nav class="topnav" aria-label="主导航">
        <a href="/">接口文档</a>
        <a v-if="user?.role === 'admin'" href="/admin.html">用户管理</a>
        <a v-if="user?.role === 'admin'" href="/admin.html#call-logs">调用记录</a>
      </nav>

      <div class="toolbar">
        <span class="userbar">
          <template v-if="user">
            {{ user.username }} / {{ user.role }}
            <template v-if="user.expires_at"> / {{ user.expires_at }}</template>
          </template>
          <template v-else>未登录</template>
        </span>
        <button class="btn ghost" type="button" @click="emit('reload')">刷新</button>
        <button class="btn primary" type="button" @click="emit('copy')">复制列表</button>
        <button class="btn ghost" type="button" @click="emit('logout')">退出</button>
      </div>
    </div>
  </header>
</template>
