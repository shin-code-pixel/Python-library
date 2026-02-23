import pandas as pd

file1 = "a.csv"
file2 = "b.csv"

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

#列名を正規化（空白除去＋小文字）
df1.columns = df1.columns.astype(str).str.strip().str.lower()
df2.columns = df2.columns.astype(str).str.strip().str.lower()

print("df1 columns:", list(df1.columns))
print("df2 columns:", list(df2.columns))

# 両方に共通する列をキーにする（まずは一番左の共通列）
common = [c for c in df1.columns if c in df2.columns]
if not common:
    raise RuntimeError("共通の列名がありません。CSVヘッダを確認してください。")

# ←　最初の列を自動でキーにする
key = common[0]
print("merge key:", key)

#IDをキーにする
merged = df1.merge(df2, on=key, how="outer", indicator=True,suffixes=("_a","_b"))

#1)片側にしか無い行
only_one_side = merged[merged["_merge"] != "both"]

#2)両方にあるが値が違う行（key以外のどれかの列が違う）
value_cols = [c for c in df1.columns if c != key]
different = merged[merged["_merge"] == "both"].copy()
for c in value_cols:
    different = different[different[f"{c}_a"] != different[f"{c}_b"]]

print("only_one_side:")
print(only_one_side)

print("/ndifferent:")
print(different)

only_one_side.to_csv("only_one_side.csv", index=False, encoding="utf-8-sig")
different.to_csv("different.csv", index=False, encoding="utf-8-sig")

print("saved: only_one_side.csv, different.csv")
