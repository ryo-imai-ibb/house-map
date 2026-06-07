import { useEffect, useState } from "react";

import { createProperty, fetchProperties } from "./api";
import type { Property } from "./types";

type Property = {
  id: number;
  source_url: string;
  address: string;
  latitude: number;
  longitude: number;
  created_at: string;
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

  useEffect(() => {
    async function loadProperties() {
      const response = await fetch("http://127.0.0.1:8000/properties");
      const data = await response.json();
      setProperties(data);
    }

    loadProperties();
  }, []);

  // 登録ボタンを押したときに実行する関数。
  async function handleSubmit() {
    if (sourceUrl === "" || address === "") {
      return;
    }

    await createProperty({
      source_url: sourceUrl,
      address: address,
    });

    const data = await fetchProperties();
    setProperties(data);

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
            {property.address} / {property.source_url}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;