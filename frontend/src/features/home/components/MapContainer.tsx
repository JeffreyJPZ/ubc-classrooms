import { useContext, useEffect, useRef } from "react";
import mapboxgl, { Map, SourceSpecification } from "mapbox-gl";
import 'mapbox-gl/dist/mapbox-gl.css';

import { Building, Coordinates, MapFeature, MapFeatureCollection, MapRef, MapSource } from "../../../types";
import { FormDataContext } from "../contexts";
import { useBuildings } from "../api";
import "./MapContainer.css"

// Initial map coordinates
const UBCV_CENTER: Coordinates = [-123.24530, 49.26101];

// Convert buildings to GeoJSON standard
function transformToGeoJson(buildings: Building[]): MapSource {
    const transformedBuildings: MapFeature[] = buildings.map((building) => {
        const coordinates: Coordinates = [parseFloat(building.longitude), parseFloat(building.latitude)];
        const feature: MapFeature = {
            type: "Feature",
            geometry: {
                type: "Point",
                coordinates: coordinates
            },
            properties: {
                name: building.building_name,
                code: building.building_code,
                address: building.building_address
            }
        };
        return feature;
    });

    return {type: "geojson", data: {type: "FeatureCollection", features: transformedBuildings} as MapFeatureCollection};
}

export function MapContainer(): JSX.Element {
    const mapRef = useRef<Map | null>(null) as MapRef<Map | null>;
    const mapContainerRef = useRef<HTMLDivElement | null>(null) as MapRef<HTMLDivElement | null>;

    const formState = useContext(FormDataContext);
    const buildingsQuery = useBuildings({campus: "UBCV"}, {id: "buildings"});

    useEffect(() => {
        mapboxgl.accessToken = import.meta.env.PROD ? import.meta.env.VITE_MAPBOX_ACCESS_TOKEN : import.meta.env.VITE_MAPBOX_DEV_ACCESS_TOKEN;
        if (mapContainerRef.current !== null && mapRef.current === null) {
            mapRef.current = new mapboxgl.Map({
                container: mapContainerRef.current as HTMLDivElement,
                center: UBCV_CENTER,
                pitch: 60,
                bearing: 0,
                zoom: 16
            });
        }
        
        if (buildingsQuery.data !== undefined && mapRef.current?.loaded && mapRef.current?.getLayer('points') === undefined) {
            mapRef.current.loadImage(
                'https://docs.mapbox.com/mapbox-gl-js/assets/custom_marker.png',
                (error, image) => {
                    if (error) throw error;

                    mapRef.current?.addImage('custom-marker', image as ImageData);
                    
                    const geojson: MapSource = transformToGeoJson(
                        formState.buildings === undefined ?
                        buildingsQuery.data :
                        buildingsQuery.data.filter((building) => {
                        formState.buildings?.includes(building.building_code)})
                    );
                    
                    mapRef.current?.addSource('points', geojson as SourceSpecification);
        
                    mapRef.current?.addLayer({
                        id: 'points',
                        type: 'symbol',
                        source: 'points',
                        layout: {
                            'icon-image': 'custom-marker',
                            'text-field': ['get', 'name'],
                            'text-font': ['Open Sans Semibold', 'Arial Unicode MS Bold'],
                            'text-offset': [0, 1.25],
                            'text-anchor': 'top'
                        }
                    });
                }
            );
        }
    }, [buildingsQuery.data, mapRef.current?.loaded, formState.buildings]);

    if (buildingsQuery.isLoading) {
        return (
            <div>Loading...</div>
        );
    };
    
    if (!buildingsQuery.data) {
        return (
            <div>Nothing to show...</div>
        );
    };

    return (
        <div className="map-container" ref={mapContainerRef}/>
    );
}