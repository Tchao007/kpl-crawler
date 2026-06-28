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
```

示例：

```text
GET /api/core/stock_plates?StockID=002354
GET /api/core/limit_up_kline?StockID=002354
GET /api/core/stock_dp_real?StockID=002354
GET /api/core/large_orders_page?StockID=001399&st=50&Type=2&Vol=500
GET /api/core/five_level?StockID=000620
GET /api/core/time_sales?StockID=000620&limit=100
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
