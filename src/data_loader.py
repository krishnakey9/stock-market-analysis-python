import json
import pandas as pd


def load_stock_data(json_path):
    with open(json_path, "r") as f:
        raw = json.load(f)

    if isinstance(raw, dict) and "data" in raw:
        records = raw["data"]
    elif isinstance(raw, list):
        records = raw
    else:
        raise ValueError("Unsupported JSON format")

    df = pd.DataFrame(records)

    # -------- Detect Date column --------
    for col in ["Date", "CH_TIMESTAMP", "TIMESTAMP", "createdAt"]:
        if col in df.columns:
            df["Date"] = pd.to_datetime(df[col], errors="coerce")
            break
    else:
        raise ValueError("No valid date column found")

    # -------- Map price columns --------
    price_map = {
        "Open": ["Open", "CH_OPENING_PRICE"],
        "High": ["High", "CH_TRADE_HIGH_PRICE"],
        "Low": ["Low", "CH_TRADE_LOW_PRICE"],
        "Close": ["Close", "CH_LAST_TRADED_PRICE"],
        "Volume": ["Volume", "CH_TOT_TRADED_QTY"]
    }

    for std, candidates in price_map.items():
        for c in candidates:
            if c in df.columns:
                df[std] = df[c]
                break

    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna().sort_values("Date").reset_index(drop=True)
    return df
