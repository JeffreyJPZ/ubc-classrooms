import { useEffect, useRef } from "react";
import mapboxgl, { Map } from "mapbox-gl";
import 'mapbox-gl/dist/mapbox-gl.css';

import { MapRef } from "../../../types";

import "./MapContainer.css"

export function MapContainer(): JSX.Element {
    const mapRef = useRef<Map | null>(null) as MapRef<Map | null>;
    const mapContainerRef = useRef<HTMLDivElement | null>(null) as MapRef<HTMLDivElement | null>;

    useEffect(() => {
        mapboxgl.accessToken = import.meta.env.PROD ? import.meta.env.VITE_MAPBOX_ACCESS_TOKEN : import.meta.env.VITE_MAPBOX_DEV_ACCESS_TOKEN;
        if (mapContainerRef.current !== null && mapRef.current === null) {
            mapRef.current = new mapboxgl.Map({
                container: mapContainerRef.current as HTMLDivElement
            });
        }
    }, [mapRef, mapContainerRef]);

    return (
        <div className="map-container" ref={mapContainerRef}/>
    );
}