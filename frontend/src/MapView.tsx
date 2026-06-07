import { GoogleMap, Marker, useJsApiLoader } from "@react-google-maps/api";

import type { Property } from "./types";

type MapViewProps = {
  properties: Property[];
};

const containerStyle = {
  width: "100%",
  height: "400px",
};

const center = {
  lat: 35.681236,
  lng: 139.767125,
};

function MapView({ properties }: MapViewProps) {
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
    <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={13}>
        {properties.map((property) => (
            <Marker
            key={property.id}
            position={{
                lat: property.latitude,
                lng: property.longitude,
            }}
            />
        ))}
    </GoogleMap>
  );
}

export default MapView;