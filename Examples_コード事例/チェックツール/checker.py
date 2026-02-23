import pandas as pd

INPUT_CSV = "input.csv"
OUT_ERRORS = "errors.csv"

RULES_REQUIRED = "rules_required.csv"
RULES_DIGITS = "rules_digits.csv"

def add_error(errors, row_idx, column, message, value):
    errors.append(
        {
                "row": row_idx + 2,     # CSVのヘッダ１行　＋　１始まりに合わせる
                "column": column,
                "message": message,
                "value": "" if pd.isna(value) else str(value)
        }
    )

def main():
    df = pd.read_csv(INPUT_CSV, dtype=str)  #文字列として読む（桁落ち防止）
    df.columns = df.columns.astype(str).str.strip().str.lower()

    errors = []

    # --- 必須チェック ---
    req = pd.read_csv(RULES_REQUIRED, dtype=str)
    req_cols = [c.strip().lower() for c in req["column"].tolist()]

    for col in req_cols:
        if col not in df.columns:
            errors.append({"row": "", "column": col, "message": "必須列が存在しません", "value": ""})
            continue

        for i, v in enumerate(df[col].tolist()):
            if v is None or str(v).strip() == "" or str(v).strip().lower() == "nan":
                add_error(errors, i, col, "必須（空欄）", v)
    
    # --- 数字・桁数チェック ---
    dig = pd.read_csv(RULES_DIGITS, dtype=str)
    for _, r in dig.iterrows():
        col = str(r["column"]).strip().lower()
        min_len = int(r["min_len"])
        max_len = int(r["max_len"])

        if col not in df.columns:
            errors.append({"row": "",  "column": col, "message": "桁数チェック列が存在しません", "value": ""})
            continue

        for i,v in enumerate(df[col].tolist()):
            s = "" if v is None else str(v).strip()
            if s == "" or s.lower()== "nan":
                continue    #空は必須側でやる想定
            if not s.isdigit():
                add_error(errors, i, col, "数字のみではありません", v)
                continue
            if not(min_len <= len(s) <= max_len):
                add_error(errors, i, col, f"桁数範囲外（{min_len}~{max_len})", v)
    
    # 出力
    out = pd.DataFrame(errors, columns=["row", "column", "message", "value"])
    out.to_csv(OUT_ERRORS, index = False, encoding="utf-8-sig")

    print(f"checked: {INPUT_CSV}")
    print(f"errors: {len(out)} -> {OUT_ERRORS}")

if __name__== "__main__":
    main()
