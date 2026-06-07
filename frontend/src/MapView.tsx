import { useState } from "react";
import { GoogleMap, Marker, useJsApiLoader } from "@react-google-maps/api";

import type { Property } from "./types";

const containerStyle = {
  width: "100%",
  height: "100%",
};

const center = {
  lat: 35.681236,
  lng: 139.767125,
};

type MapViewProps = {
  properties: Property[];
};

function MapView({ properties }: MapViewProps) {
  const [selectedProperty, setSelectedProperty] = useState<Property | null>(
    null
  );

  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;

  const { isLoaded, loadError } = useJsApiLoader({
    googleMapsApiKey: apiKey,
  });

  if (loadError) {
    return <p>地図の読み込みに失敗しました</p>;
  }

  if (!isLoaded) {
    return <p>地図を読み込み中...</p>;
  }

  return (
    <div className="map-container">
      <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={13}>
        {properties.map((property) => (
          <Marker
            key={property.id}
            position={{
              lat: property.latitude,
              lng: property.longitude,
            }}
            onClick={() => setSelectedProperty(property)}
          />
        ))}
      </GoogleMap>

      {selectedProperty !== null && (
        <div className="map-info-panel">
          <button
            className="map-info-close-button"
            onClick={() => setSelectedProperty(null)}
          >
            ×
          </button>

          <div className="map-info-title">選択中の物件</div>

          <div className="map-info-address">{selectedProperty.address}</div>

          <a
            href={selectedProperty.source_url}
            target="_blank"
            rel="noreferrer"
          >
            HOME'Sで開く
          </a>

          <button
            className="map-info-delete-button"
            onClick={() => setSelectedProperty(null)}
          >
            削除
          </button>

        </div>
      )}
    </div>
  );
}

export default MapView;