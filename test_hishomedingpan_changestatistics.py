import requests
import pandas as pd
import json
import sys
import os

BASE_URL = "http://localhost:8765"


def login(username: str = "admin", password: str | None = None) -> requests.Session:
    if password is None:
        password = os.environ.get("KPL_ADMIN_PASSWORD", "admin123456")
    session = requests.Session()
    try:
        response = session.post(
            f"{BASE_URL}/api/auth/login",
            json={"username": username, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        if data.get("error"):
            print(f"登录失败: {data['error']}")
            sys.exit(1)
        print(f"登录成功: {data.get('user', {}).get('username', '')}")
        return session
    except Exception as e:
        print(f"登录请求失败: {e}")
        sys.exit(1)


def call_changestatistics(session: requests.Session, **overrides) -> dict:
    try:
        response = session.post(
            f"{BASE_URL}/api/hishomedingpan_changestatistics",
            data=overrides
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"接口调用失败: {e}")
        return {"error": str(e)}


def parse_response_to_dataframe(data: dict) -> pd.DataFrame:
    body = data.get("body") or data
    if not body:
        print("响应体为空")
        return pd.DataFrame()

    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            print("响应体不是有效的JSON")
            return pd.DataFrame({"raw_response": [body]})

    if isinstance(body, dict):
        items = body.get("info") or body.get("data") or body.get("result") or body.get("items")
        if items and isinstance(items, list):
            df = pd.DataFrame(items)
            numeric_cols = ["strong", "ztjs", "lbgd", "df_num"]
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            if "Day" in df.columns:
                df["Day"] = pd.to_datetime(df["Day"], errors="coerce")
            return df

        df = pd.DataFrame(body.items(), columns=["key", "value"])
        return df.explode("value")
    elif isinstance(body, list):
        return pd.DataFrame(body)
    else:
        return pd.DataFrame({"response": [body]})


def main():
    print("=" * 60)
    print("测试 HisHomeDingPan.ChangeStatistics 接口")
    print("=" * 60)

    session = login()

    print("\n调用接口 /api/hishomedingpan_changestatistics...")
    result = call_changestatistics(session)

    if result.get("error"):
        print(f"错误: {result}")
        return

    errcode = result.get("errcode")
    tip = result.get("tip", "")
    print(f"\n响应错误码: {errcode}")
    if tip:
        print(f"温馨提示: {tip}")

    df = parse_response_to_dataframe(result)

    if df.empty:
        print("\n无法解析响应数据")
        print("原始响应:", json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n解析到 {len(df)} 行数据")
        print(f"数据类型:\n{df.dtypes}")
        print("-" * 60)
        print("数据预览:")
        print(df.head(20).to_string(index=False))

        if len(df.columns) > 1:
            print("\n数据统计:")
            numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
            if len(numeric_cols) > 0:
                print(df[numeric_cols].describe())
            else:
                print(df.describe(include="all"))

        csv_path = "changestatistics_result.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"\n数据已保存到: {csv_path}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
