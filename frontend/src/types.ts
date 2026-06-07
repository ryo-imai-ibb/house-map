// これはFastAPIが返すPropertyの形と対応する。
// React側でも同じデータ構造をTypeScript型として定義している。

export type Property = {
  id: number;
  source_url: string;
  address: string;
  latitude: number;
  longitude: number;
  created_at: string;
};