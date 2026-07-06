# 风口模块接口调用建议

- 主入口：`/api/market/fengkou/stocks`。传 `date=YYYYMMDD` 或 `date=YYYY-MM-DD` 锁定某个交易日，今天或历史交易日都走同一路径，服务端按日期自动选择实时/历史源；不传 `date` 时返回当前可用的实时风口股票列表。分页参数用 `index` 和 `limit`，默认等价于上游 `Index=0&st=500`；排序默认用抓包里的 `Order=17`。
- 概念入口：`/api/market/fengkou/plates`。传 `date` 返回指定交易日的风口概念/板块强度列表；不传 `date` 时建议由服务端解析最近可用交易日。抓包确认该入口历史源为 `StockFengKData.GetFengKYDPlate`，上游返回 `[板块名, 强度值]` 数组。
- 分时入口：`/api/market/fengkou/plates/:plateCode/trend`、`/api/market/fengkou/plates/:plateCode/volume-turnover`。用于风口板块详情页的分时走势和量能成交，传 `date` 查历史，不传 `date` 查实时；`plateCode` 对应上游 `StockID`，例如 `801225`。
- 兼容别名：`/api/stockfengkdata_getfengklist` 等价于主入口不传 `date` 的实时股票列表；`/api/stockfengkdata_getfengklist_18021` 等价于主入口传历史 `date`；`/api/stockfengkdata_getfengkydplate` 等价于概念入口的历史查询。新接入只用主入口和概念入口即可，无需先判断今天还是历史再切别名。

## 上游抓包依据

| 场景 | Host | c | a | 关键参数 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 实时风口股票列表 | `apphwhq.longhuvip.com` | `StockFengKData` | `GetFengKList` | `Index=0&st=500&Order=17&Day=&Time=` | 不传日期时使用实时源 |
| 历史风口股票列表 | `apphis.longhuvip.com` | `StockFengKData` | `GetFengKList` | `Index=0&st=500&Order=17&Day=YYYYMMDD&Time=1500` | 有 `Day` 时必须走历史源 |
| 历史风口概念列表 | `apphis.longhuvip.com` | `StockFengKData` | `GetFengKYDPlate` | `Day=YYYYMMDD` | 返回概念/板块强度 |
| 板块分时走势 | `apphwhq.longhuvip.com` / `apphis.longhuvip.com` | `ZhiShuL2Data` | `GetTrendIncremental` | `StockID=plateCode&Day=` 或 `Day=YYYY-MM-DD` | `Day` 为空为实时，有值为历史 |
| 板块量能成交 | `apphwhq.longhuvip.com` / `apphis.longhuvip.com` | `ZhiShuL2Data` | `GetVolTurIncremental` | `StockID=plateCode&Day=` 或 `Day=YYYY-MM-DD` | 返回分钟级量能/成交额 |

## 主要字段

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `date` / `day` | String | 交易日期，统一输出 `YYYYMMDD`，可兼容上游 `YYYY-MM-DD` |
| `count` / `total` | Number | 本次返回条数 / 可用记录总数 |
| `stocks[].code` / `stocks[].stockCode` | String | 股票代码，兼容 6 位裸码 |
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

## 调用规则

- `date` 为空：股票列表走 `apphwhq.longhuvip.com`，上游 `Day=&Time=`，用于实时风口。
- `date` 不为空：股票列表走 `apphis.longhuvip.com`，上游 `Day=YYYYMMDD`；如果调用方未传 `time`，默认补 `Time=1500`。
- 历史接口中文名称需要带“历史”两个字，例如“历史市场风口-按照股票”“历史市场风口-按概念”，避免和实时风口混用。
- `date` 入参允许 `YYYYMMDD` 和 `YYYY-MM-DD`，服务端统一归一化；对 `ZhiShuL2Data` 历史分时接口可保留 `YYYY-MM-DD` 形式，响应仍统一输出 `YYYYMMDD`。
- `index`、`limit` 映射上游 `Index`、`st`；`order` 映射上游 `Order`，不传时用 `17`。
- 不要向前端暴露 `UserID`、`Token`、`DeviceID`、`apiv`、`VerSion` 等抓包参数，服务端内部维护即可。
- 实时结果建议短缓存 5 到 15 秒；历史结果在收盘后可长缓存，按 `date + time + order + index + limit` 做缓存键。
- 如果历史日期无数据，建议返回空列表并带 `availableDates`；不要自动静默改查其他日期，除非接口名明确是“最近可用风口”。

## 示例响应

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
  "plates": [
    {
      "name": "锂电池",
      "score": 325.69
    }
  ],
  "meta": {
    "source": "history",
    "upstreamAction": "StockFengKData.GetFengKList"
  }
}
```

---

# 龙虎榜模块调用建议

## 数据来源

- `C:\Users\Administrator\Desktop\myfile\行情\api接口\龙虎榜_今日上版_2026_06_28_15_39_57.har`
- `C:\Users\Administrator\Desktop\myfile\行情\api接口\龙虎榜_游资组合_2026_06_28_16_08_47.har`
- `C:\Users\Administrator\Desktop\myfile\行情\api接口\龙虎榜-顶级游资_2026_06_28_16_24_43.har`
- 项目已生成接口：`generated/scenario_api_server.py`

以下说明只基于上述抓包和项目现有接口整理；未能从抓包确认的字段标注为“未确认/预留”。

## 调用建议

- 今日/历史上榜股票主入口：`/api/longhubang_getstocklist_18249`。不传 `Time` 或传 `Time=` 时使用当前可用数据；传 `Time=YYYY-MM-DD` 锁定历史交易日。抓包中 `Type=2`、`Index=0`、`st=500`，其中 `Index` 和 `st` 用于分页。
- 今日/历史上榜营业部列表：`/api/longhubang_getagencylistv2`。传 `Time=YYYY-MM-DD` 指定交易日，`Index` 和 `st` 控制分页。抓包样例为 `Time=2026-06-26&Index=0&st=500`。
- 营业部买卖列表：`/api/longhubang_getbusinesslist`。传 `Time=YYYY-MM-DD` 指定交易日，`Type`、`Index`、`st` 可动态传入。抓包样例为 `Type=1&Time=2026-06-26&Index=0&st=100`，`Type` 完整枚举含义未在抓包中确认。
- 营业部区间统计：`/api/longhubang_getagencydaylist`。传 `SDay=YYYY-MM-DD&EDay=YYYY-MM-DD` 查询区间统计。抓包样例为 `SDay=2026-04-03&EDay=2026-06-16`。
- 营业部K线：`/api/longhubang_getagencykline`。抓包中只有 `index=0&st=499`，未出现营业部 ID 参数；按当前证据，它更像龙虎榜营业部整体统计曲线，不建议自行追加未确认参数。
- 游资组合信息主入口：`/api/businessgroup_groupinfo`。传 `GID` 查询指定游资组合。抓包确认 `GID` 是区分不同游资组合的关键参数。
- 游资组合流水主入口：`/api/businessgroup_grouplog`。传 `GID`、`Day`、`Index`、`st`、`Money`、`Order`、`SDay`。抓包样例为 `GID=41&Day=3&Index=0&st=30&Money=5000000&Order=2&SDay=0`。
- 游资组合目录：`/api/userbusiness_getofficev2`。返回“顶级游资、一线游资”等分组，以及分组下的游资组合列表、营业部信息和近期关联股票。
- 游资日期列表：`/api/userbusiness_getday`。传 `Day=` 时返回当前可用日期和游资类别列表；抓包中 `Day` 为空。
- 游资组合股票图表：`/api/stock_getstockchart_18257`。传 `StockID`、`index`、`st` 查询股票日 K 数据。抓包样例为 `StockID=000783&index=0&st=250`。
- 固定游资别名接口已在项目中存在；如果需要动态切换游资，优先使用主入口并传 `GID`。

## 固定游资别名

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

## 主要字段

### `/api/longhubang_getstocklist_18249`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `Time` | String | 返回数据对应日期；抓包中历史请求使用 `YYYY-MM-DD` |
| `Total` / `Count` | Number | 总条数 / 本次返回条数 |
| `list[]` | Array | 龙虎榜上榜股票列表 |
| `list[].ID` | String | 股票代码 |
| `list[].Name` | String | 股票名称 |
| `list[].IncreaseAmount` | String | 涨跌幅，如 `9.96%` |
| `list[].D3` | String | 抓包中为 `0` 或 `1`，具体业务含义未确认 |
| `list[].BuyIn` | String/Number | 抓包字段名为 `BuyIn`，金额字段；可正可负，具体口径以开盘啦展示为准 |
| `list[].JoinNum` | Number/String | 上榜次数/参与数量类字段，具体口径未确认 |
| `list[].Turnover` | String/Number | 成交额 |
| `list[].CircPrice` | String/Number | 流通市值 |
| `list[].Capitalization` | String/Number | 总市值 |
| `list[].Amplitude` | String | 振幅 |
| `list[].TurnoverRatio` | String | 换手率 |
| `errcode` | String | 错误码，`0` 表示成功 |

### `/api/longhubang_getagencylistv2`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `Day` / `Time` | String | 返回数据日期 / 时间字段 |
| `List[]` | Array | 今日上榜营业部相关股票列表 |
| `List[].ID` | String/Number | 股票代码 |
| `List[].Name` | String | 股票名称 |
| `List[].Day` | String | 上榜日期，`YYYY-MM-DD` |
| `List[].BuyIn` | Number | 金额字段；抓包中可为负数 |
| `List[].JoinNum` | Number/String | 上榜次数/参与数量类字段，具体口径未确认 |
| `List[].IncreaseAmount` | String | 涨跌幅 |
| `List[].Turnover` | String/Number | 成交额 |
| `List[].Amplitude` | String | 振幅 |
| `List[].TurnoverRatio` | String | 换手率 |
| `List[].CircPrice` | String/Number | 流通市值 |
| `List[].Capitalization` | String/Number | 总市值 |
| `List[].FengKou` | Array | 题材/风口代码列表 |
| `errcode` | String | 错误码，`0` 表示成功 |

### `/api/longhubang_getbusinesslist`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `Time` | String | 查询日期 |
| `Total` | Number | 总条数 |
| `list[]` | Array | 营业部买卖列表 |
| `list[].ID` | String | 营业部 ID |
| `list[].Name` | String | 营业部名称 |
| `list[].Buy` | String/Number | 买入金额 |
| `list[].Sell` | String/Number | 卖出金额 |
| `list[].JoinNum` | Number/String | 上榜次数/参与数量类字段，具体口径未确认 |
| `sDay` | String | 抓包响应存在该字段，具体含义未确认 |
| `errcode` | String | 错误码，`0` 表示成功 |

### `/api/longhubang_getagencydaylist`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `List[]` | Array | 营业部区间统计列表 |
| `List[].ID` | String | 股票代码 |
| `List[].Name` | String | 股票名称 |
| `List[].Day` | String | 日期，`YYYY-MM-DD` |
| `List[].D3` | String | 抓包中为 `0` 或 `1`，具体业务含义未确认 |
| `List[].JoinNum` | String/Number | 上榜次数/参与数量类字段，具体口径未确认 |
| `List[].BuyIn` | String/Number | 金额字段；可正可负 |
| `List[].CircPrice` | String/Number | 流通市值 |
| `List[].Capitalization` | String/Number | 总市值 |
| `List[].FengKou` | Array | 题材/风口代码列表 |
| `errcode` | String | 错误码，`0` 表示成功 |

### `/api/longhubang_getagencykline`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `List[]` | Array | K线/曲线点列表 |
| `List[][0]` | String | 日期，`YYYY-MM-DD` |
| `List[][1]` | String/Number | 指标值；抓包样例为 `34.68`、`46.94`，具体指标名称未确认 |
| `errcode` | String | 错误码，`0` 表示成功 |

### `/api/businessgroup_groupinfo`

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
| `MsgList[]` | Array | 消息/说明列表；抓包未展开确认字段含义 |
| `Time` | String/Number | 时间字段 |
| `errcode` | String | 错误码，`0` 表示成功 |

### `/api/businessgroup_grouplog`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `conut` | Number/String | 抓包原字段名为 `conut`，应为总数类字段 |
| `list[]` | Array | 游资组合流水列表 |
| `list[].LogID` | String | 流水记录 ID |
| `list[].StockID` | String/Number | 股票代码 |
| `list[].Name` | String | 股票名称 |
| `list[].IncreaseAmount` | String | 涨跌幅 |
| `list[].D3` | String | 抓包中为 `0` 或 `1`，具体业务含义未确认 |
| `list[].Buy` | String/Number | 买入金额 |
| `list[].Sell` | String/Number | 卖出金额 |
| `list[].Type` | String | 交易方向标记；抓包样例显示 `1` 对应买入记录、`2` 对应卖出记录 |
| `list[].Color` | String | 颜色/展示标记，具体含义未确认 |
| `list[].Time` | String | 交易日期，`YYYY-MM-DD` |
| `list[].BID` | String | 营业部 ID |
| `list[].Money` | String/Number | 本条流水金额；样例中等于买入或卖出金额 |
| `errcode` | String | 错误码，`0` 表示成功 |

### `/api/userbusiness_getofficev2`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `List[]` | Array | 游资大类列表 |
| `List[].Name` | String | 大类名称，如 `顶级游资`、`一线游资` |
| `List[].ID` | Number/String | 大类 ID |
| `List[].Desc` | String | 大类说明 |
| `List[].CreateAt` | Number/String | 创建时间戳 |
| `List[].List[]` | Array | 该大类下的游资组合列表 |
| `List[].List[].ID` | String | 游资组合 ID，对应 `GID` |
| `List[].List[].Name` | String | 游资组合完整名称 |
| `List[].List[].ShortName` | String | 游资组合简称 |
| `List[].List[].Level` | String | 等级/排序类字段，具体口径未确认 |
| `List[].List[].Num` | String | 数量类字段，具体口径未确认 |
| `List[].List[].GType` | String | 游资分组类型字段，具体枚举未确认 |
| `List[].List[].SBZJ` | String/Number | 抓包字段名为 `SBZJ`，像资金阈值字段，但口径未确认 |
| `List[].List[].Stock` | Object | 近期关联股票信息，股票代码为对象键 |
| `errcode` | String | 错误码，`0` 表示成功 |

### `/api/userbusiness_getday`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `TList[]` | Array | 游资大类列表 |
| `TList[].ID` | Number/String | 大类 ID |
| `TList[].Name` | String | 大类名称，如 `顶级游资`、`一线游资` |
| `List[]` | Array | 日期/游资相关列表；抓包未展开确认字段含义 |
| `Day` | String | 当前查询日期 |
| `NDay` | String | 下一/最近可用日期字段，具体方向未确认 |
| `Time` | String/Number | 时间字段 |
| `errcode` | String | 错误码，`0` 表示成功 |

### `/api/stock_getstockchart_18257`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `Name` | String | 股票名称 |
| `x[]` | Array | 日期序列，格式如 `YYYYMMDD` |
| `y[]` | Array | K线价格数组；抓包样例为 `[开, 收, 高, 低]` 形态，例如 `[6.71, 6.72, 6.73, 6.67]` |
| `m5[]` | Array | 5日均线 |
| `m10[]` | Array | 10日均线 |
| `m20[]` | Array | 20日均线 |
| `m30[]` | Array | 30日均线 |
| `vol[]` | Array | 成交量 |
| `errcode` | String | 错误码，`0` 表示成功 |

## 参数规则

| 参数名 | 适用接口 | 说明 |
| --- | --- | --- |
| `Time` | `LongHuBang.GetStockList`、`GetAgencyListV2`、`GetBusinessList` | 日期参数；抓包使用 `YYYY-MM-DD`。为空时表示当前可用数据 |
| `SDay` / `EDay` | `LongHuBang.GetAgencyDayList` | 区间开始/结束日期，格式 `YYYY-MM-DD` |
| `GID` | `BusinessGroup.GroupInfo`、`BusinessGroup.GroupLog` | 游资组合 ID，是区分不同游资组合的关键参数 |
| `Day` | `BusinessGroup.GroupLog`、`UserBusiness.GetDay` | `GroupLog` 抓包中出现 `3`、`6`、`12`，看起来是时间范围枚举，但完整含义未确认 |
| `Money` | `BusinessGroup.GroupLog` | 金额过滤阈值；抓包固定为 `5000000` |
| `Order` | `BusinessGroup.GroupLog` | 排序参数；抓包固定为 `2`，其他取值未确认 |
| `Index` / `index` | 多数列表/K线接口 | 分页或偏移参数；项目保留原始大小写 |
| `st` | 多数列表/K线接口 | 单次返回条数 |
| `StockID` | `Stock.GetStockChart` | 股票代码，抓包使用 6 位代码 |
| `Type` | `LongHuBang.GetStockList`、`GetBusinessList` | 抓包中 `GetStockList` 使用 `Type=2`，`GetBusinessList` 使用 `Type=1`；完整枚举未确认 |

## 不建议作为新接入主入口的存量接口

| 接口 | 说明 |
| --- | --- |
| `/api/longhubang_getstocklist` | 早期存量龙虎榜股票列表接口；新接入建议使用 `/api/longhubang_getstocklist_18249` |
| `/api/longhubang_toptitle` | 龙虎榜标题信息 |
| `/api/longhubangdongcai_getstate` | 龙虎榜东财状态 |
| `/api/longhubang_updatelist` | 龙虎榜更新列表 |
| `/api/longhubang_add` | 动作类接口，非查询主入口 |
| `/api/longhubang_beijiaosuoget` | 北交所龙虎榜数据；本次三份 HAR 未覆盖字段结构，暂不展开 |

---

# 打板模块调用建议

## 数据来源

- `C:\Users\Administrator\Desktop\myfile\行情\api接口\行情-打板_2026_07_06_22_22_15.har`
- 项目存量接口：`/api/hishomedingpan_getnum`
- 项目存量接口：`/api/hishomedingpan_hisdabanlist`

以下说明只基于上述抓包和项目现有接口整理；未能从抓包确认的字段标注为“未确认”。

## 调用建议

- 统计主入口：`/api/hishomedingpan_getnum`。传 `Day=YYYY-MM-DD` 查询指定交易日的打板页顶部统计数量。该接口返回 `nums` 对象，包含涨停、破板、跌停、翘板、竞价等计数字段。
- 列表主入口：`/api/hishomedingpan_hisdabanlist`。传 `Day=YYYY-MM-DD`、`PidType`、`Type` 查询对应分类列表；分页使用 `Index` 和 `st`；排序使用 `Order`。新接入只保留这个动态主入口，不按 `PidType + Type` 拆成多个重复接口。
- 过滤参数：`Is_st`、`Filter`、`FilterGem`、`FilterMotherboard`、`FilterTIB` 由 URL 动态传入。抓包样例均为 `Is_st=1&Filter=0&FilterGem=0&FilterMotherboard=0&FilterTIB=0`。
- 日期参数：`Day` 必须放到 URL 中；抓包格式为 `YYYY-MM-DD`，例如 `2026-07-03`。
- 当前抓包只有历史源，Host 为 `apphis.longhuvip.com`；未确认实时源是否使用同名接口。

## 上游抓包依据

| 场景 | Host | c | a | 关键参数 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 打板统计数量 | `apphis.longhuvip.com` | `HisHomeDingPan` | `GetNum` | `Day=2026-07-03&Is_st=1&Filter=0&FilterGem=0&FilterMotherboard=0&FilterTIB=0` | 返回 `nums` 统计 |
| 打板分类列表 | `apphis.longhuvip.com` | `HisHomeDingPan` | `HisDaBanList` | `Day=2026-07-03&PidType=8&Type=18&Order=1&Index=0&st=30` | 返回 `list` 股票列表 |

## 已确认分类参数

| PidType | Type | 抓包返回条数 | 对应统计项判断 |
| --- | --- | ---: | --- |
| `1` | `6` | `30+` | 可能对应涨停列表，和 `ZT=104` 方向一致 |
| `2` | `4` | `30+` | 可能对应破板列表，和 `PB=52` 方向一致 |
| `3` | `6` | `19` | 对应跌停列表，和 `DT=19` 对得上 |
| `4` | `6` | `30+` | 可能对应 `FYZ=97`，具体中文名未确认 |
| `5` | `4` | `12` | 对应翘板列表，和 `QB=12` 对得上 |
| `8` | `18` | `30+` | 竞价/综合打板列表，可能对应 `JJ` 或 `JJZZ`，具体中文名未确认 |

未在本次 HAR 中抓到对应列表请求的统计项：`WKB`、`FXB`。不要为这两个字段自行编造 `PidType` / `Type`，后续需要点击对应页面后再补。

## 统计字段

### `/api/hishomedingpan_getnum`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `nums` | Object | 打板页顶部统计对象 |
| `nums.JJZZ` | Number | 抓包样例为 `191`，竞价相关子统计，具体中文名未确认 |
| `nums.ZT` | Number | 涨停数量，抓包样例为 `104` |
| `nums.PB` | Number | 破板数量，抓包样例为 `52` |
| `nums.DT` | Number | 跌停数量，抓包样例为 `19` |
| `nums.FYZ` | Number | 抓包样例为 `97`，具体中文名未确认 |
| `nums.QB` | Number | 翘板数量，抓包样例为 `12` |
| `nums.JJ` | Number | 竞价相关总数，抓包样例为 `245` |
| `nums.WKB` | Number | 抓包样例为 `1`，具体中文名未确认 |
| `nums.FXB` | Number | 抓包样例为 `45`，具体中文名未确认 |
| `ttag` | Number | 上游耗时标记 |
| `errcode` | String | 错误码，`0` 表示成功 |

示例：

```text
GET|POST /api/hishomedingpan_getnum?Day=2026-07-03&Is_st=1&Filter=0&FilterGem=0&FilterMotherboard=0&FilterTIB=0
```

示例响应：

```json
{
  "nums": {
    "JJZZ": 191,
    "ZT": 104,
    "PB": 52,
    "DT": 19,
    "FYZ": 97,
    "QB": 12,
    "JJ": 245,
    "WKB": 1,
    "FXB": 45
  },
  "ttag": 0.0012940000000000035,
  "errcode": "0"
}
```

## 列表字段

### `/api/hishomedingpan_hisdabanlist`

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| `list[]` | Array | 股票列表，每行是数组结构 |
| `list[][0]` | String | 股票代码 |
| `list[][1]` | String | 股票名称 |
| `list[][4]` | Number/String | 涨跌幅或阶段涨幅；不同 `PidType/Type` 下含义可能不同 |
| `list[][6]` | Number/String | 时间戳字段；在部分分类中出现 |
| `list[][7]` | Number/String | 时间戳字段；在部分分类中出现 |
| `list[][8]` | Number/String | 金额/成交类字段；具体口径未确认 |
| `list[][9]` | String | 连板标签；样例为 `4天3板` |
| `list[][10]` | Number/String | 连板/高度类数值；具体口径未确认 |
| `list[][11]` | String | 题材/概念标签，多个标签用顿号分隔 |
| `list[][12]` | Number/String | 资金/金额类字段，具体口径未确认 |
| `list[][13]` | Number/String | 成交额或金额类字段，具体口径未确认 |
| `list[][14]` | Number/String | 换手率/比例类字段，具体口径未确认 |
| `list[][15]` | Number/String | 市值类字段，具体口径未确认 |
| `day` | String | 查询日期，格式 `YYYY-MM-DD` |
| `ttag` | Number | 上游耗时标记 |
| `errcode` | String | 错误码，`0` 表示成功 |

示例：

```text
GET|POST /api/hishomedingpan_hisdabanlist?Day=2026-07-03&PidType=8&Type=18&Order=1&Index=0&st=30&Is_st=1&Filter=0&FilterGem=0&FilterMotherboard=0&FilterTIB=0
```

示例响应片段：

```json
{
  "list": [
    [
      "603137",
      "恒尚节能",
      0,
      "",
      10.03,
      0,
      0,
      0,
      0,
      "",
      0,
      "并购重组、基础建设",
      6791218,
      10426365,
      0.73,
      1433615976
    ]
  ],
  "day": "2026-07-03",
  "errcode": "0"
}
```

## 参数规则

| 参数名 | 适用接口 | 说明 |
| --- | --- | --- |
| `Day` | `GetNum`、`HisDaBanList` | 交易日期，抓包格式 `YYYY-MM-DD`，必须放 URL |
| `PidType` | `HisDaBanList` | 分类参数，需要与 `Type` 联合使用 |
| `Type` | `HisDaBanList` | 分类参数，需要与 `PidType` 联合使用 |
| `Order` | `HisDaBanList` | 排序参数；抓包固定为 `1`，其他取值未确认 |
| `Index` | `HisDaBanList` | 分页起点；抓包出现 `0` 和 `12` |
| `st` | `HisDaBanList` | 单次返回数量；抓包为 `30` |
| `Is_st` | `GetNum`、`HisDaBanList` | 抓包固定为 `1`，具体业务含义未确认 |
| `Filter` | `GetNum`、`HisDaBanList` | 过滤开关；抓包为 `0` |
| `FilterGem` | `GetNum`、`HisDaBanList` | 创业板过滤；抓包为 `0` |
| `FilterMotherboard` | `GetNum`、`HisDaBanList` | 主板过滤；抓包为 `0` |
| `FilterTIB` | `GetNum`、`HisDaBanList` | 科创板过滤；抓包为 `0` |

## 接入规则

- 只保留 `GetNum` 和 `HisDaBanList` 两个主入口，分类由 `PidType`、`Type` 动态传入。
- `Day`、`PidType`、`Type`、`Order`、`Index`、`st` 和过滤参数都应在 URL 调用界面可编辑。
- `JJZZ`、`FYZ`、`WKB`、`FXB` 的中文含义和对应列表参数未完全确认，后续必须通过补充抓包确认后再维护。
