# house-map
物件をマップ上に表示するアプリ

## Google APIの課金制度
【結論】
- geocoding
月10000回まで無料．1回の定義は，住所を緯度経度に変換すること．

- Maps JavaScript
月10000回まで無料．1回の定義は，Webページ上でGoogle Mapを1回読み込むこと．
[概要](https://mapsplatform.google.com/pricing/#pay-as-you-go)
[詳細](https://developers.google.com/maps/billing-and-pricing/pay-as-you-go?hl=ja)

## DBのカラムを追加したい場合
1. DBオープン
```
sqlite3 properties.db
```
2. カラム追加
```
ALTER TABLE properties ADD COLUMN memo TEXT;
```
NULLを禁止する予定のものは，既存行のデフォルト値を指定する.
```
ALTER TABLE properties ADD COLUMN memo TEXT NOT NULL DEFAULT '';
```
3. 確認
```
.schema properties
```
4. 終了
```
.quit
```
5. 実装変更
```
database.py
→ CREATE TABLE に memo を追加

schemas.py
→ Property / PropertyCreate に memo を追加するか決める

crud.py
→ SELECT / INSERT / UPDATE に memo を追加

frontend/src/types.ts
→ TypeScriptのProperty型に memo を追加

App.tsx
→ 入力欄や表示に memo を追加するなら修正
```
