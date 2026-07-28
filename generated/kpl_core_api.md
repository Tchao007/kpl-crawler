# Kaipanla Core API Wrapper

核心接口服务入口：

```text
GET /api/core
GET|POST /api/core/{name}
```

可用接口：

```text
module_versatile
stock_plates
stock_turnover_distribution
large_orders
large_orders_page
limit_up_gene
today_kline
limit_up_kline
stock_dp_real
stock_dp_explain
xianhuo_list
plate_popup_config
five_level
time_sales
plate_factor_tags
plate_factor_stock_list
```

示例：

```text
GET /api/core/stock_plates?StockID=002354
GET /api/core/limit_up_kline?StockID=002354
GET /api/core/stock_dp_real?StockID=002354
GET /api/core/large_orders_page?StockID=001399&st=50&Type=2&Vol=500
GET /api/core/five_level?StockID=000620
GET /api/core/time_sales?StockID=000620&limit=100
GET /api/core/plate_factor_tags?PlateID=801612
GET /api/core/plate_factor_stock_list?PlateID=801612&TSZB=17&Type=42&Order=1&Date=2026-07-27
```

## Plate Factor Ranking

The `plate_factor_tags` and `plate_factor_stock_list` core APIs package the
plate-detail factor ranking flow captured from Frida on 2026-07-28.

Tag discovery:

```text
GET|POST /api/core/plate_factor_tags?PlateID=801612
GET|POST /api/core/plate_factor_tags?PlateID=801612&Date=2026-07-27
```

Upstream mapping:

| Mode | Host | c | a | Key params |
| --- | --- | --- | --- | --- |
| Realtime tags | `apphwhq.longhuvip.com` | `ConceptionPoint` | `BKFenShiZhiBo` | `PlateID`, `Date=` |
| History tags | `apphis.longhuvip.com` | `HisConceptionPoint` | `BKFenShiZhiBo` | `PlateID`, `Date=YYYY-MM-DD` |

The tag response contains reusable factor definitions:

```json
{
  "TSZB": "17",
  "TSZB_N": "人气激增",
  "TSZB_Order": "1",
  "TSZB_Type": "42",
  "GoodID": "67",
  "Filed_Type": "3",
  "IsOpen": 1
}
```

Stock list:

```text
GET|POST /api/core/plate_factor_stock_list?PlateID=801612&TSZB=17&Type=42&Order=1
GET|POST /api/core/plate_factor_stock_list?PlateID=801612&TSZB=17&Type=42&Order=1&Date=2026-07-27
```

Upstream mapping:

| Mode | Host | c | a | Key params |
| --- | --- | --- | --- | --- |
| Realtime list | `apphwhq.longhuvip.com` | `ZhiShuRanking` | `ZhiShuStockList_W8` | `PlateID`, `TSZB`, `Type`, `Order`, `Index=0`, `st=30` |
| History list | `apphis.longhuvip.com` | `ZhiShuRanking` | `ZhiShuStockList_W8` | `PlateID`, `TSZB`, `Type`, `Order`, `Date=YYYY-MM-DD`, `Index=0`, `st=30` |

Verified factor tags from the same capture include:

| Name | TSZB | Type | Order |
| --- | --- | --- | --- |
| 最正宗 | `3` | `6` | `1` |
| 人气激增 | `17` | `42` | `1` |
| 机构增仓 | `20` | `29` | `1` |
| 机构预测 | `69` | `162` | `1` |
| 外资持股 | `66` | `231` | `1` |
| 低PE | `7` | `46` | `0` |
| 高股息 | `8` | `67` | `1` |
| 破净相关 | `19` | `38` | `0` |
| 中报增长 | `12` | `33` | `1` |

The realtime socket packet observed for 人气激增 used:

```text
hqList|26:20030/2501-0/801612:42:1:0:0:0:17:0
```

## Five-level quote

The `five_level` core API decodes hqStock binary quote packets captured from
the app runtime. It reads the local Frida capture log and returns the latest
decoded packet for the requested stock.

```text
GET|POST /api/core/five_level?StockID=000620
```

`five_level` uses hqStock packet `2015`. The decoded fields are:

```text
sell: field 6, price_raw / 10000
buy:  field 7, price_raw / 10000
volume: lots
amount: price * volume * 100
```

Example response body:

```json
{
  "stock": "000620",
  "source": "frida_hqstock_2015",
  "sequence": 1500,
  "base_price": 3.11,
  "sell": [],
  "buy": [
    {
      "price": 3.42,
      "price_raw": 34200,
      "volume": 157948,
      "volume_unit": "lot",
      "amount": 54018216,
      "amount_raw": 5401821600,
      "amount_unit": "CNY"
    }
  ]
}
```

Note: start Frida capture and open the stock quote page before calling this API,
otherwise the local log may not contain a fresh hqStock packet.

## Time-sales

The `time_sales` core API decodes hqStock packet `2006`, which contains
intraday trade prints.

```text
GET|POST /api/core/time_sales?StockID=000620&limit=100
```

Decoded trade fields:

```text
time: field 1, formatted HH:mm:ss.SSS
price: field 2 / 10000
side: field 3, buy/sell/neutral
volume: field 4, lots
amount: field 6, CNY
```

Example response body:

```json
{
  "stock": "000620",
  "source": "frida_hqstock_2006",
  "day": "20260626",
  "count": 25,
  "trades": [
    {
      "time": "14:55:48.000",
      "price": 3.42,
      "side": "buy",
      "volume": 116,
      "volume_unit": "lot",
      "amount": 39672,
      "amount_raw": 39672,
      "amount_unit": "CNY"
    }
  ]
}
```

上游账号参数可用环境变量注入：

```text
KPL_UPSTREAM_USER_ID
KPL_UPSTREAM_TOKEN
KPL_UPSTREAM_DEVICE_ID
```

这些接口来自 Frida 对 `libssl.so!SSL_read` / `SSL_write` 的明文复现。

---

# Scenario API development notes

本文档补充项目场景接口的开发约定。以下内容参考 `outputs/learnme.md`，只整理已从抓包和现有项目确认的信息；未能确认的字段会显式标注为“未确认”。

## Common rules

- 对外入口尽量提供稳定语义化路径；存量抓包路径作为兼容别名保留。
- `Day`、`Time`、`SDay`、`EDay` 这类日期参数需要放到 URL 查询参数中，便于前端直接修改和复用。
- 有实时/历史两个上游源时，服务端根据日期参数选择源：不传日期走实时源，传日期走历史源。
- `Index` / `index` 表示分页偏移，`st` 表示单次返回条数；保持上游大小写，避免破坏已捕获接口。
- 不向前端暴露 `UserID`、`Token`、`DeviceID`、`apiv`、`VerSion` 等抓包账号和设备参数，由服务端统一维护。
- 实时接口建议短缓存 5 到 15 秒；历史接口可按日期、时间、排序和分页参数做长缓存。
- 没有数据时返回空列表和必要的元信息，不要静默改查其他日期，除非接口名称明确表达“最近可用”。

## Market Fengkou

风口模块用于封装 `StockFengKData`、`ZhiShuL2Data` 相关接口。

### Recommended endpoints

- 主入口：`/api/market/fengkou/stocks`。传 `date=YYYYMMDD` 或 `date=YYYY-MM-DD` 锁定交易日；不传 `date` 时返回实时风口股票列表。分页参数使用 `index` 和 `limit`，分别映射上游 `Index` 和 `st`；排序参数 `order` 映射上游 `Order`，默认使用抓包确认的 `17`。
- 概念入口：`/api/market/fengkou/plates`。传 `date` 返回指定交易日风口概念/板块强度列表；不传 `date` 时由服务端解析最近可用交易日。抓包确认历史源为 `StockFengKData.GetFengKYDPlate`，上游返回 `[板块名, 强度值]` 数组。
- 分时入口：`/api/market/fengkou/plates/:plateCode/trend`。查询风口板块分时走势，`plateCode` 对应上游 `StockID`。
- 量能入口：`/api/market/fengkou/plates/:plateCode/volume-turnover`。查询风口板块分钟级量能/成交额，`plateCode` 对应上游 `StockID`。
- 兼容别名：`/api/stockfengkdata_getfengklist` 等价于实时股票列表；`/api/stockfengkdata_getfengklist_18021` 等价于历史股票列表；`/api/stockfengkdata_getfengkydplate` 等价于历史概念列表。

### Upstream mapping

| 场景 | Host | c | a | 关键参数 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 实时风口股票列表 | `apphwhq.longhuvip.com` | `StockFengKData` | `GetFengKList` | `Index=0&st=500&Order=17&Day=&Time=` | 不传日期时使用实时源 |
| 历史风口股票列表 | `apphis.longhuvip.com` | `StockFengKData` | `GetFengKList` | `Index=0&st=500&Order=17&Day=YYYYMMDD&Time=1500` | 有 `Day` 时走历史源 |
| 历史风口概念列表 | `apphis.longhuvip.com` | `StockFengKData` | `GetFengKYDPlate` | `Day=YYYYMMDD` | 返回概念/板块强度 |
| 板块分时走势 | `apphwhq.longhuvip.com` / `apphis.longhuvip.com` | `ZhiShuL2Data` | `GetTrendIncremental` | `StockID=plateCode&Day=` 或 `Day=YYYY-MM-DD` | `Day` 为空为实时，有值为历史 |
| 板块量能成交 | `apphwhq.longhuvip.com` / `apphis.longhuvip.com` | `ZhiShuL2Data` | `GetVolTurIncremental` | `StockID=plateCode&Day=` 或 `Day=YYYY-MM-DD` | 返回分钟级量能/成交额 |

### Main fields

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `date` / `day` | String | 交易日期，统一输出 `YYYYMMDD`，兼容上游 `YYYY-MM-DD` |
| `count` / `total` | Number | 本次返回条数 / 可用记录总数 |
| `stocks[].code` / `stocks[].stockCode` | String | 股票代码 |
| `stocks[].name` / `stocks[].stockName` | String | 股票名称 |
| `stocks[].changePercent` | Number/String | 涨跌幅，上游数组下标 `3` |
| `stocks[].amount` | Number/String | 成交额或历史成交额，上游数组下标 `4` |
| `stocks[].buyAmount` | Number/String | 买入金额，上游数组下标 `5` |
| `stocks[].sellAmount` | Number/String | 卖出金额，上游数组下标 `6` |
| `stocks[].netInflowAmount` | Number/String | 净流入金额，上游数组下标 `7` |
| `stocks[].themeTags` | String | 题材/风口标签，上游数组下标 `8`，多个标签用逗号分隔 |
| `stocks[].capitalTag` | String | 资金/席位标签，例如“基金”“游资”，上游数组下标 `10` |
| `stocks[].classifiedTheme` | String | 归类后的风口题材，上游数组下标 `11` |
| `stocks[].updatedAt` | Number/String | 更新秒级时间戳，上游数组下标 `12` |
| `plates[].name` | String | 风口概念/板块名称 |
| `plates[].score` | Number | 风口强度值，上游 `GetFengKYDPlate` 第二列 |
| `trend[].time` | String | 分钟时间，例如 `09:30` |
| `trend[].price` | Number | 板块分时价格/指数点位 |
| `volumeTurnover[].volume` | Number | 分钟成交量 |
| `volumeTurnover[].turnover` | Number | 分钟成交额 |
| `meta.source` | String | `realtime` 或 `history` |
| `meta.upstreamAction` | String | 实际使用的上游动作，例如 `StockFengKData.GetFengKList` |

### Example response

```json
{
  "date": "20260626",
  "count": 2,
  "stocks": [
    {
      "code": "600973",
      "name": "宝胜股份",
      "changePercent": "2.50",
      "amount": "5757038021",
      "buyAmount": "346355701",
      "sellAmount": "-199007424",
      "netInflowAmount": "147348277",
      "themeTags": "高铁,电网混改",
      "capitalTag": "",
      "classifiedTheme": "高铁,电网混改",
      "updatedAt": "1782438669"
    }
  ],
  "meta": {
    "source": "history",
    "upstreamAction": "StockFengKData.GetFengKList"
  }
}
```

## Longhu Bang

龙虎榜模块用于封装 `LongHuBang`、`BusinessGroup`、`UserBusiness`、`Stock.GetStockChart` 相关接口。

### Recommended endpoints

- 今日/历史上榜股票：`/api/longhubang_getstocklist_18249`。不传 `Time` 或传 `Time=` 时使用当前可用数据；传 `Time=YYYY-MM-DD` 锁定历史交易日。抓包中 `Type=2`、`Index=0`、`st=500`。
- 今日/历史上榜营业部：`/api/longhubang_getagencylistv2`。传 `Time=YYYY-MM-DD` 指定交易日，`Index` 和 `st` 控制分页。
- 营业部买卖列表：`/api/longhubang_getbusinesslist`。传 `Time=YYYY-MM-DD` 指定交易日，`Type`、`Index`、`st` 可动态传入；`Type` 完整枚举未确认。
- 营业部区间统计：`/api/longhubang_getagencydaylist`。传 `SDay=YYYY-MM-DD&EDay=YYYY-MM-DD` 查询区间统计。
- 营业部 K 线：`/api/longhubang_getagencykline`。抓包中只有 `index=0&st=499`，未确认营业部 ID 参数。
- 游资组合信息：`/api/businessgroup_groupinfo`。传 `GID` 查询指定游资组合，`GID` 是区分不同游资组合的关键参数。
- 游资组合流水：`/api/businessgroup_grouplog`。传 `GID`、`Day`、`Index`、`st`、`Money`、`Order`、`SDay` 查询组合流水。
- 游资组合目录：`/api/userbusiness_getofficev2`。返回游资分组、组合列表、营业部信息和近期关联股票。
- 游资日期列表：`/api/userbusiness_getday`。抓包中 `Day` 为空，返回当前可用日期和游资类别列表。
- 游资组合股票图表：`/api/stock_getstockchart_18257`。传 `StockID`、`index`、`st` 查询股票日 K 数据。

固定游资别名接口已经存在；新开发动态切换功能时，优先使用主入口并传 `GID`。

### Fixed GID aliases

| 游资中文名 | GID | 组合信息接口 | 组合流水接口 |
| --- | --- | --- | --- |
| 成都系 | `7` | `/api/businessgroup_groupinfo_18259` | `/api/businessgroup_grouplog_18272` |
| 佛山系 | `10` | `/api/businessgroup_groupinfo_18260` | `/api/businessgroup_grouplog_18273` |
| 炒股养家 | `20` | `/api/businessgroup_groupinfo_18261` | `/api/businessgroup_grouplog_18274` |
| 赵老哥 | `25` | `/api/businessgroup_groupinfo_18262` | `/api/businessgroup_grouplog_18275` |
| 小鳄鱼 | `33` | `/api/businessgroup_groupinfo_18263` | `/api/businessgroup_grouplog_18276` |
| 作手新一 | `35` | `/api/businessgroup_groupinfo_18264` | `/api/businessgroup_grouplog_18277` |
| 章盟主 | `41` | `/api/businessgroup_groupinfo_18265` | `/api/businessgroup_grouplog_18278` |
| 量化基金 | `57` | `/api/businessgroup_groupinfo_18266` | `/api/businessgroup_grouplog_18279` |
| 上塘路 | `64` | `/api/businessgroup_groupinfo_18267` | `/api/businessgroup_grouplog_18280` |
| 北京光华路 | `81` | `/api/businessgroup_groupinfo_18268` | `/api/businessgroup_grouplog_18281` |
| 思明南路 | `82` | `/api/businessgroup_groupinfo_18269` | `/api/businessgroup_grouplog_18282` |
| 南京帮 | `93` | `/api/businessgroup_groupinfo_18270` | `/api/businessgroup_grouplog_18283` |
| 机构 | `999` | `/api/businessgroup_groupinfo_18271` | `/api/businessgroup_grouplog_18284` |

### Main response fields

#### `/api/longhubang_getstocklist_18249`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `Time` | String | 返回数据对应日期，历史请求使用 `YYYY-MM-DD` |
| `Total` / `Count` | Number | 总条数 / 本次返回条数 |
| `list[]` | Array | 龙虎榜上榜股票列表 |
| `list[].ID` | String | 股票代码 |
| `list[].Name` | String | 股票名称 |
| `list[].IncreaseAmount` | String | 涨跌幅，例如 `9.96%` |
| `list[].D3` | String | 抓包中为 `0` 或 `1`，业务含义未确认 |
| `list[].BuyIn` | String/Number | 金额字段，可正可负，具体口径以开盘啦展示为准 |
| `list[].JoinNum` | Number/String | 上榜次数/参与数量类字段，具体口径未确认 |
| `list[].Turnover` | String/Number | 成交额 |
| `list[].CircPrice` | String/Number | 流通市值 |
| `list[].Capitalization` | String/Number | 总市值 |
| `list[].Amplitude` | String | 振幅 |
| `list[].TurnoverRatio` | String | 换手率 |
| `errcode` | String | 错误码，`0` 表示成功 |

#### `/api/businessgroup_groupinfo`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `GID` | String/Number | 游资组合 ID |
| `Info` | String | 游资组合介绍 |
| `ShortName` | String | 游资组合简称 |
| `Total` | Number/String | 总数类字段，具体口径未确认 |
| `CertifiID` | String/Number | 认证 ID/标记，具体含义未确认 |
| `BusinessList[]` | Array | 关联营业部列表 |
| `BusinessList[].ID` | String | 营业部 ID |
| `BusinessList[].Name` | String | 营业部名称 |
| `MsgList[]` | Array | 消息/说明列表，字段含义未展开确认 |
| `errcode` | String | 错误码，`0` 表示成功 |

#### `/api/businessgroup_grouplog`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `conut` | Number/String | 抓包原字段名为 `conut`，应为总数类字段 |
| `list[]` | Array | 游资组合流水列表 |
| `list[].LogID` | String | 流水记录 ID |
| `list[].StockID` | String/Number | 股票代码 |
| `list[].Name` | String | 股票名称 |
| `list[].IncreaseAmount` | String | 涨跌幅 |
| `list[].D3` | String | 抓包中为 `0` 或 `1`，业务含义未确认 |
| `list[].Buy` | String/Number | 买入金额 |
| `list[].Sell` | String/Number | 卖出金额 |
| `list[].Type` | String | 交易方向标记；抓包样例显示 `1` 对应买入记录、`2` 对应卖出记录 |
| `list[].Color` | String | 颜色/展示标记，具体含义未确认 |
| `list[].Time` | String | 交易日期，`YYYY-MM-DD` |
| `list[].BID` | String | 营业部 ID |
| `list[].Money` | String/Number | 本条流水金额；样例中等于买入或卖出金额 |
| `errcode` | String | 错误码，`0` 表示成功 |

### Parameter notes

| 参数名 | 适用接口 | 说明 |
| --- | --- | --- |
| `Time` | `LongHuBang.GetStockList`、`GetAgencyListV2`、`GetBusinessList` | 日期参数，抓包使用 `YYYY-MM-DD`；为空时表示当前可用数据 |
| `SDay` / `EDay` | `LongHuBang.GetAgencyDayList` | 区间开始/结束日期，格式 `YYYY-MM-DD` |
| `GID` | `BusinessGroup.GroupInfo`、`BusinessGroup.GroupLog` | 游资组合 ID，是区分不同游资组合的关键参数 |
| `Day` | `BusinessGroup.GroupLog`、`UserBusiness.GetDay` | `GroupLog` 抓包中出现 `3`、`6`、`12`，看起来是时间范围枚举，完整含义未确认 |
| `Money` | `BusinessGroup.GroupLog` | 金额过滤阈值；抓包固定为 `5000000` |
| `Order` | `BusinessGroup.GroupLog` | 排序参数；抓包固定为 `2`，其他取值未确认 |
| `Index` / `index` | 多数列表/K线接口 | 分页或偏移参数；项目保留原始大小写 |
| `st` | 多数列表/K线接口 | 单次返回条数 |
| `StockID` | `Stock.GetStockChart` | 股票代码，抓包使用 6 位代码 |
| `Type` | `LongHuBang.GetStockList`、`GetBusinessList` | 抓包中 `GetStockList` 使用 `Type=2`，`GetBusinessList` 使用 `Type=1`；完整枚举未确认 |
