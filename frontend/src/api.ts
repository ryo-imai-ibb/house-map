import type { Property } from "./types";

const API_BASE_URL = "http://127.0.0.1:8000";

// GET /properties を呼ぶ関数
export async function fetchProperties(): Promise<Property[]> { // 非同期処理の結果として、Property配列を返す
  const response = await fetch(`${API_BASE_URL}/properties`); // ブラウザからHTTPリクエストを送る関数

  if (!response.ok) {
    throw new Error("Failed to fetch properties");
  }

  const properties = await response.json(); // レスポンスJSONをJavaScript/TypeScriptの値に変換
  return properties;
}