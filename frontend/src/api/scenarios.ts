import { apiJson, apiUrl, handleAuthFailure } from "./client";

export interface User {
  username: string;
  role: "admin" | "user" | string;
  expires_at?: string | null;
}

export interface LevelOption {
  value: string;
  label: string;
}

export interface RawScenario {
  session_id?: string | number;
  sessionId?: string | number;
  title?: string;
  name?: string;
  title_cn?: string;
  titleCn?: string;
  added_time?: string;
  addedTime?: string;
  maintenance_time?: string;
  maintenanceTime?: string;
  method_name?: string;
  methodName?: string;
  http_method?: string;
  httpMethod?: string;
  target_url?: string;
  url?: string;
  endpoint?: string;
  alias_endpoint?: string;
  aliasEndpoint?: string;
  level?: string;
  level_label?: string;
  levelLabel?: string;
  params?: Record<string, string>;
  data?: Record<string, string>;
  hide_url_fields?: string[];
  hideUrlFields?: string[];
  is_core?: boolean;
  isCore?: boolean;
  host?: string;
}

export interface Scenario {
  sessionId: string;
  title: string;
  titleCn: string;
  addedTime: string;
  maintenanceTime: string;
  methodName: string;
  httpMethod: string;
  targetUrl: string;
  endpoint: string;
  aliasEndpoint: string;
  level: string;
  levelLabel: string;
  params: Record<string, string>;
  data: Record<string, string>;
  hideUrlFields: string[];
  isCore: boolean;
  host: string;
  group: string;
}

export interface ScenariosPayload {
  count: number;
  scenarios: RawScenario[];
  level_options: LevelOption[];
  user: User;
}

export interface TopicPayload {
  requested_at?: string;
  output?: string;
  result?: {
    requested_at?: string;
    func_name?: string;
    topic_library?: {
      status_code?: string | number;
      upstream_url?: string;
      body?: unknown;
    };
  };
}

export function hostFromUrl(url: string): string {
  try {
    return new URL(url).host || "";
  } catch {
    return "";
  }
}

export function inferGroup(item: RawScenario, host: string): string {
  const title = String(item.title || "");
  const titleCn = String(item.title_cn || item.titleCn || "");
  const sessionId = String(item.session_id || item.sessionId || "");
  const text = `${host} ${title} ${titleCn}`.toLowerCase();

  if (text.includes("local_hqstock") || text.includes("hqstock")) return "行情核心";
  if (text.includes("市场量能") || /^1822[5-9]$|^1823[0-2]$/.test(sessionId)) return "市场量能";
  if (
    text.includes("情绪") ||
    text.includes("大幅回撤") ||
    text.includes("涨停表现") ||
    text.includes("风向标") ||
    /^1820[8-9]$|^1821[0-9]$|^1822[0-4]$|^1823[3-9]$|^1824[0-8]$/.test(sessionId)
  ) {
    return "情绪模块";
  }
  if (text.includes("apphwhq")) return "行情核心";
  if (text.includes("apphis")) return "历史数据";
  if (text.includes("apparticle")) return "资讯内容";
  if (text.includes("appuser") || text.includes("applog")) return "用户与埋点";
  if (text.includes("getsockip")) return "网络配置";
  if (text.includes("applhb")) {
    if (text.includes("longhubang") || text.includes("龙虎榜")) return "龙虎榜";
    if (text.includes("stock") || text.includes("个股") || text.includes("盘口")) return "个股详情";
    return "龙虎榜";
  }
  return "其他";
}

export function normalizeScenario(item: RawScenario): Scenario {
  const host = item.host || hostFromUrl(item.target_url || item.url || "");
  return {
    sessionId: String(item.session_id ?? item.sessionId ?? ""),
    title: item.title || item.name || "未命名场景",
    titleCn: item.title_cn || item.titleCn || "",
    addedTime: item.added_time || item.addedTime || "",
    maintenanceTime: item.maintenance_time || item.maintenanceTime || "",
    methodName: item.method_name || item.methodName || "",
    httpMethod: item.http_method || item.httpMethod || "POST",
    targetUrl: item.target_url || item.url || "",
    endpoint: item.endpoint || "",
    aliasEndpoint: item.alias_endpoint || item.aliasEndpoint || "",
    level: item.level || "normal",
    levelLabel: item.level_label || item.levelLabel || "一般",
    params: item.params || {},
    data: item.data || {},
    hideUrlFields: item.hide_url_fields || item.hideUrlFields || [],
    isCore: Boolean(item.is_core || item.isCore),
    host,
    group: inferGroup(item, host)
  };
}

export function getUrlManagedFields(item: Scenario): string[] {
  const hiddenFields = new Set(item.hideUrlFields || []);
  const fields = ["Day", "Date", "DStart", "DEnd", "SDay", "EDay", "GID", "Type", "ZSType"].filter(
    (key) => item.data[key] && !hiddenFields.has(key)
  );
  if (/^\d{4}-\d{2}-\d{2}$/.test(String(item.data.Time || ""))) fields.push("Time");
  return fields;
}

export function buildRequestUrl(item: Scenario): string {
  const url = apiUrl(item.endpoint || item.aliasEndpoint);
  const params = new URLSearchParams();

  if ((item.httpMethod || "POST").toUpperCase() === "GET") {
    Object.entries(item.params || {}).forEach(([key, value]) => params.set(key, value));
    Object.entries(item.data || {}).forEach(([key, value]) => params.set(key, value));
  } else {
    Object.entries(item.params || {}).forEach(([key, value]) => params.set(key, value));
    getUrlManagedFields(item).forEach((key) => params.set(key, item.data[key]));
  }

  const query = params.toString();
  if (query) url.search = query;
  return url.toString();
}

export async function loadScenarios(): Promise<ScenariosPayload> {
  return apiJson<ScenariosPayload>("/api/scenarios");
}

export async function loadTopicLatest(): Promise<TopicPayload> {
  return apiJson<TopicPayload>("/api/topic-library/latest");
}

export async function crawlTopicLibrary(): Promise<TopicPayload> {
  return apiJson<TopicPayload>("/api/topic-library/crawl", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ func_name: "题材库" })
  });
}

export async function saveScenarioMeta(
  scenario: Scenario,
  payload: { title: string; title_cn: string; maintenance_time: string; level: string }
): Promise<RawScenario> {
  const response = await apiJson<{ scenario: RawScenario }>(
    `/api/admin/scenario-meta/${encodeURIComponent(scenario.sessionId)}`,
    {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }
  );
  return response.scenario;
}

export async function callScenario(item: Scenario): Promise<{ status: number; text: string }> {
  const requestUrl = buildRequestUrl(item);
  const init: RequestInit = {
    method: item.httpMethod || "POST",
    headers: { Accept: "application/json" }
  };

  if ((item.httpMethod || "POST").toUpperCase() === "POST") {
    const body = new URLSearchParams();
    const urlManagedFields = new Set(getUrlManagedFields(item));
    Object.entries(item.data || {}).forEach(([key, value]) => {
      if (!urlManagedFields.has(key)) body.set(key, value);
    });
    init.headers = {
      ...init.headers,
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    };
    init.body = body.toString();
  }

  const response = await fetch(requestUrl, init);
  if (handleAuthFailure(response)) return { status: response.status, text: "" };
  return { status: response.status, text: await response.text() };
}

