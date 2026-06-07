import { useState } from "react";

type Property = {
  sourceUrl: string;
  address: string;
};

function App() {
  // Reactに「変化する値」を覚えさせるための書き方．意味は下記．
  // sourceUrl：値の変数名。
  // setSourceUrl：関数の変数名。
  // useState：「Reactが覚えておく値」と「その値を更新して画面再描画を起こす関数」を返す関数．値は引数で指定する．
  const [sourceUrl, setSourceUrl] = useState("");
  const [address, setAddress] = useState("");

  // 登録済み物件の住所一覧
  const [properties, setProperties] = useState<Property[]>([]);

  // 登録ボタンを押したときに実行する関数。
  // 今はまだAPI通信せず、入力値をConsoleに出すだけ。
  function handleSubmit() {
    if (sourceUrl === "" || address === "") {
      return;
    }

    const newProperty: Property = {
      sourceUrl: sourceUrl,
      address: address,
    };

    // propertiesの末尾に、新しい住所を追加した配列を作る。
    // Reactでは既存配列を直接変更せず、新しい配列を作ってsetPropertiesに渡す。
    setProperties([...properties, newProperty]); // ...properties は 配列の中身を展開する書き方

    setSourceUrl("");
    setAddress("");
  }

  return (
    <div>
      <h1>物件マップ</h1>

      <h2>物件登録</h2>

      <div>
        <label>HOME'S URL</label>
        <input
          type="text"
          value={sourceUrl} // この入力欄に表示する文字は sourceUrl の値にしてください
          onChange={(event) => setSourceUrl(event.target.value)} // 入力欄の中身が変わったときに, 入力欄に今入っている文字を、sourceUrl に保存する. 
        />
      </div>

      <div>
        <label>住所</label>
        <input
          type="text"
          value={address}
          onChange={(event) => setAddress(event.target.value)}
        />
      </div>

      <button onClick={handleSubmit}>登録</button> {/* クリックされたときにhandleSubmitを実行する. */}

      <h2>登録済み物件</h2>

      <ul>
        {properties.map((property, index) => (
          <li key={index}>
            {property.address} / {property.sourceUrl}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;