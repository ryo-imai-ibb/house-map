# Frontend Learning Notes

## 1. フロントエンドとは何か

Webアプリのフロントエンドは、ブラウザ上でユーザーが直接見る・操作する部分である。

今回のアプリでは、最終的に以下を担当する。

* 物件URLと住所の入力フォームを表示する
* 登録ボタンを表示する
* バックエンドAPIを呼び出す
* 登録済み物件を一覧表示する
* 地図を表示する
* 地図上に物件ピンを表示する

バックエンドが「データ処理・保存」を担当するのに対して、フロントエンドは「画面表示・ユーザー操作」を担当する。

---

## 2. HTML / CSS / JavaScript の役割

Web画面は基本的に以下の3つで構成される。

```text
HTML → 画面の構造
CSS  → 見た目
JS   → 動き
```

物件登録画面で考えると、以下のようになる。

```text
HTML:
  見出し、入力欄、ボタン、リストを置く

CSS:
  余白、色、サイズ、配置を整える

JavaScript:
  ボタンを押したときの処理を書く
  APIを呼ぶ
  取得したデータを画面に反映する
```

---

## 3. 各拡張子の役割

### `.html`

HTMLを書くファイル。

画面に何を置くかを書く。

```html
<h1>物件マップ</h1>
<input type="text" />
<button>登録</button>
```

Reactアプリでは、HTMLファイルをたくさん書くことは少ない。

Vite + Reactの場合、主なHTMLファイルは以下。

```text
frontend/index.html
```

これはReactアプリを差し込むための土台である。

---

### `.css`

CSSを書くファイル。

画面の見た目を整える。

```css
h1 {
  color: blue;
}

button {
  padding: 8px 16px;
}
```

ReactでもCSSは使う。

例:

```text
src/App.css
src/index.css
```

---

### `.js`

JavaScriptを書くファイル。

画面に動きをつける。

```js
const address = "東京都渋谷区";

function sayHello() {
  console.log("hello");
}
```

ボタンを押したときの処理、API通信、画面更新などを書く。

---

### `.ts`

TypeScriptを書くファイル。

TypeScriptは、型付きJavaScriptである。

JavaScript:

```js
const id = 1;
const address = "東京都渋谷区";
```

TypeScript:

```ts
const id: number = 1;
const address: string = "東京都渋谷区";
```

`.ts` は、画面表示を含まない普通のTypeScriptファイルに使う。

今回だと、以下のようなファイルに使う。

```text
types.ts
api.ts
```

例:

```ts
export type Property = {
  id: number;
  source_url: string;
  address: string;
  latitude: number;
  longitude: number;
  created_at: string;
};
```

---

### `.jsx`

JavaScript + JSX のファイル。

JSXとは、JavaScriptの中にHTMLっぽい記法を書ける仕組みである。

```jsx
function App() {
  return <h1>物件マップ</h1>;
}
```

Reactでは、このJSXを使って画面を書く。

---

### `.tsx`

TypeScript + JSX のファイル。

Reactの画面部品をTypeScriptで書くときに使う。

今回主に触るのはこれ。

```text
src/App.tsx
```

例:

```tsx
function App() {
  return (
    <div>
      <h1>物件マップ</h1>
      <button>登録</button>
    </div>
  );
}

export default App;
```

`.tsx` は、以下の2つを同時に扱える。

```text
TypeScript
+
HTMLっぽいJSX
```

---

## 4. 拡張子まとめ

```text
.html  → HTMLを書く。画面の土台。
.css   → CSSを書く。見た目。
.js    → JavaScriptを書く。動き。
.ts    → TypeScriptを書く。型付きJS。画面なし。
.jsx   → JavaScript + JSX。React画面。
.tsx   → TypeScript + JSX。React画面。
```

今回よく使うのは以下。

```text
.tsx → Reactの画面を書く
.ts  → 型定義やAPI関数を書く
.css → 見た目を書く
```

---

## 5. Reactとは何か

Reactは、画面を部品として作るためのJavaScriptライブラリである。

普通のHTMLでは、画面をそのまま書く。

```html
<h1>物件マップ</h1>
<button>登録</button>
```

Reactでは、画面を関数として部品化できる。

```tsx
function PropertyForm() {
  return (
    <div>
      <h2>物件登録</h2>
      <input type="text" />
      <button>登録</button>
    </div>
  );
}
```

この `PropertyForm` は、物件登録フォーム部品である。

さらに、他の部品から呼び出せる。

```tsx
function App() {
  return (
    <div>
      <h1>物件マップ</h1>
      <PropertyForm />
    </div>
  );
}
```

Reactでは画面を以下のように分けて作れる。

```text
App
├── PropertyForm
├── PropertyList
└── PropertyMap
```

今回のアプリでは、最終的に以下のような部品を作る想定。

```text
PropertyForm
→ URLと住所を入力する部品

PropertyList
→ 登録済み物件を表示する部品

PropertyMap
→ 地図とピンを表示する部品
```

---

## 6. TypeScriptとは何か

TypeScriptは、JavaScriptに型を足した言語である。

目的は、ミスを早めに見つけること。

JavaScriptでは、以下のようなミスに気づきにくい。

```js
const property = {
  id: 1,
  address: "東京都渋谷区"
};

console.log(property.adress);
```

`address` と書きたいのに、`adress` と書いている。

TypeScriptでは、型を定義しておくことで、エディタがミスを教えてくれる。

```ts
type Property = {
  id: number;
  address: string;
};

const property: Property = {
  id: 1,
  address: "東京都渋谷区"
};

console.log(property.adress);
```

この場合、`adress` という項目は存在しないと警告される。

つまりTypeScriptは、JavaScriptをより安全に書くための仕組みである。

---

## 7. ReactとTypeScriptの関係

Reactは画面を作る道具。

TypeScriptは型付きJavaScript。

そのため、React + TypeScript は以下のように理解できる。

```text
React + TypeScript
= 型安全に画面を作る
```

今回の `App.tsx` は、Reactの画面をTypeScriptで書くファイルである。

```text
App.tsx
= Reactの画面
+ TypeScript
+ JSX
```

---

## 8. Viteとは何か

Viteは、Reactアプリを開発するための開発環境ツールである。

以下のコマンドで、React + TypeScript のひな形を作った。

```bash
npm create vite@latest frontend -- --template react-ts
```

これは以下を行う。

```text
frontendフォルダを作る
React + TypeScript のプロジェクトひな形を作る
開発サーバーで動かせるようにする
```

その後、以下で起動する。

```bash
npm run dev
```

起動すると、ブラウザで以下を開ける。

```text
http://localhost:5173
```

Viteは、Reactアプリを起動・開発しやすくする道具である。

---

## 9. npmとは何か

npmは、JavaScript / TypeScript のライブラリ管理ツールである。

Pythonでいう `pip` に近い。

```bash
npm install
```

これは、`package.json` に書かれている必要ライブラリをインストールするコマンド。

Pythonでいうと以下に近い。

```bash
pip install -r requirements.txt
```

---

## 10. Vite + React のファイル構成

ViteでReactプロジェクトを作ると、だいたい以下の構成になる。

```text
frontend/
├── index.html
├── package.json
├── vite.config.ts
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── App.css
    └── index.css
```

各ファイルの役割は以下。

```text
index.html
→ Reactアプリを差し込む土台

src/main.tsx
→ Reactアプリを起動する入口

src/App.tsx
→ 実際の画面本体

src/App.css
→ App用の見た目

src/index.css
→ 全体共通の見た目

package.json
→ npmの設定、使うライブラリ、起動コマンド

vite.config.ts
→ Viteの設定
```

最初に主に触るのは以下。

```text
src/App.tsx
```

---

## 11. Reactアプリが表示される流れ

Reactアプリは、以下の流れでブラウザに表示される。

```text
ブラウザ
  ↓
index.html
  ↓
src/main.tsx が React を起動
  ↓
App.tsx の画面を表示
```

つまり、`App.tsx` を変更すると、ブラウザに表示される画面が変わる。

---

## 12. Reactを使っていることの見極め方

Reactを使っているプロジェクトかどうかは、主に以下を見る。

### 1. `package.json`

`dependencies` に以下があればReactを使っている。

```json
{
  "dependencies": {
    "react": "...",
    "react-dom": "..."
  }
}
```

```text
react
→ React本体

react-dom
→ ReactをブラウザのDOMに描画するためのライブラリ
```

---

### 2. `src/main.tsx`

Vite + Reactでは、だいたい以下のようなコードがある。

```tsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

特に以下がReactアプリの起動を示す。

```tsx
createRoot(document.getElementById("root")!).render(...)
```

これは、`index.html` の `root` にReactアプリを描画する、という意味。

---

### 3. `.tsx` ファイルにJSXがある

`App.tsx` に以下のようなコードがある。

```tsx
function App() {
  return (
    <div>
      <h1>物件マップ</h1>
    </div>
  );
}

export default App;
```

これはReactのJSXである。

`<App />` や `<PropertyForm />` のような独自タグ風の記法が出てくると、Reactらしい。

---

### 4. `vite.config.ts`

以下のようにReactプラグインが入っている。

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
});
```

これは、ViteでReactを使うための設定である。

---

## 13. 最小理解まとめ

```text
React
→ 画面を部品で作るためのライブラリ

TypeScript
→ 型付きJavaScript

.tsx
→ Reactの画面を書くファイル

.ts
→ 型や普通の処理を書くファイル

Vite
→ React開発環境を作って起動する道具

npm
→ JavaScript / TypeScript のライブラリ管理ツール
```

今回のフロントエンドで最初に触る主なファイルは以下。

```text
App.tsx
→ 画面を書く

types.ts
→ データの形を書く

api.ts
→ バックエンドAPIを呼ぶ処理を書く
```
