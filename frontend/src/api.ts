import type { Property } from "./types";

const API_BASE_URL = "http://127.0.0.1:8000";

// POST /properties に送るデータの形
export type PropertyCreate = {
  source_url: string;
  address: string;
};

// GET /properties を実行する関数
export async function fetchProperties(): Promise<Property[]> { // 非同期処理の結果として、Property配列を返す
  const response = await fetch(`${API_BASE_URL}/properties`); // ブラウザからHTTPリクエストを送る関数

  if (!response.ok) {
    throw new Error("Failed to fetch properties");
  }

  const properties = await response.json(); // レスポンスJSONをJavaScript/TypeScriptの値に変換
  return properties;
}

// POST /properties を実行する関数
export async function createProperty(
  propertyData: PropertyCreate
): Promise<Property> {
  const response = await fetch(`${API_BASE_URL}/properties`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json", // リクエストボディの形式がJSONであることをバックエンドに伝える
    },
    body: JSON.stringify(propertyData), // TypeScriptのオブジェクトをJSON文字列に変換
  });

  if (!response.ok) {
    throw new Error("Failed to create property");
  }

  const property = await response.json();
  return property;
}