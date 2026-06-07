import { useEffect, useState } from "react";

import { createProperty, deleteProperty, fetchProperties } from "./api";
import "./App.css";
import type { Property } from "./types";
import MapView from "./MapView";

function App() {
  // Reactに「変化する値」を覚えさせるための書き方．意味は下記．
  // sourceUrl：値の変数名。
  // setSourceUrl：関数の変数名。
  // useState：「Reactが覚えておく値」と「その値を更新して画面再描画を起こす関数」を返す関数．値は引数で指定する．
  const [sourceUrl, setSourceUrl] = useState("");
  const [address, setAddress] = useState("");
  const [properties, setProperties] = useState<Property[]>([]);   // 登録済み物件の住所一覧
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => { // 関数と依存する値を引数に取る。[adress] と書くと、addressが変わるたびに関数が実行される。[] と書くと、最初の1回だけ関数が実行される。
    async function loadProperties() {
      try {
        const data = await fetchProperties();
        setProperties(data);
      } catch {
        setErrorMessage("物件一覧の取得に失敗しました");
      }
    }

    loadProperties();
  }, []);

  // 登録ボタンを押したときに実行する関数。
  async function handleSubmit() {
    if (sourceUrl === "" || address === "") {
      setErrorMessage("URLと住所を入力してください");
      return;
    }

    try {
      setErrorMessage("");

      await createProperty({
        source_url: sourceUrl,
        address: address,
      });

      const data = await fetchProperties();
      setProperties(data);

      setSourceUrl("");
      setAddress("");
    } catch {
      setErrorMessage("物件の登録に失敗しました");
    }
  }

  // 削除ボタンを押したときに実行する関数
  async function handleDelete(propertyId: number) {
    await deleteProperty(propertyId);

    const data = await fetchProperties();
    setProperties(data);
  }

  return (
    <div className="app">
      <h1>物件マップ</h1>
      {errorMessage !== "" && <p className="error-message">{errorMessage}</p>} {/* errorMessageが空でないときに、<p>タグでerrorMessageを表示する. */}

      <section className="form-section">
        <h2>物件登録</h2>

        <div className="form-field">
          <label>住所</label>
          <input
            type="text"
            value={address}
            onChange={(event) => setAddress(event.target.value)}
          />
        </div>

        <div className="form-field">
          <label>サイトURL</label>
          <input
            type="text"
            value={sourceUrl} // この入力欄に表示する文字は sourceUrl の値にしてください
            onChange={(event) => setSourceUrl(event.target.value)} // 入力欄の中身が変わったときに, 入力欄に今入っている文字を、sourceUrl に保存する. 
          />
        </div>

        <button onClick={handleSubmit}>登録</button> {/* クリックされたときにhandleSubmitを実行する. */}
      </section>

      <section className="map-section">
        <h2>地図</h2>
        <MapView properties={properties} /> {/* Reactでは、親コンポーネントから子コンポーネントに渡す値を props と呼ぶ */}
      </section>
    </div>
  );
}

export default App;
