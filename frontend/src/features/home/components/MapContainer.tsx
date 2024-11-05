import { useContext, useEffect, useRef } from "react";
import mapboxgl, { Map, MapMouseEvent, SourceSpecification } from "mapbox-gl";
import 'mapbox-gl/dist/mapbox-gl.css';

import { Building, Coordinates, MapFeature, MapFeatureCollection, MapRef, MapSource } from "../../../types";
import { FormDataContext, FormState, FormSubmittedToggleContext } from "../contexts";
import { useBuildings, useTimeslots } from "../api";
import "./MapContainer.css"

interface BuildingFeatureProperties {
    building_name?: string;
    building_code: string;
    building_address?: string;
}

// Initial map coordinates
const UBCV_CENTER: Coordinates = [-123.24530, 49.26101];
const BUILDING_LAYER_ID: string = "buildings";

// Convert buildings to GeoJSON standard, with additional properties for each building given by AdditionalBuildingsFeatureProperties
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
                building_name: building.building_name,
                building_code: building.building_code,
                building_address: building.building_address
            }
        };
        return feature;
    });

    return {type: "geojson", data: {type: "FeatureCollection", features: transformedBuildings} as MapFeatureCollection};
}

export function MapContainer(): JSX.Element {
    const mapRef = useRef<Map | null>(null) as MapRef<Map | null>;
    const mapContainerRef = useRef<HTMLDivElement | null>(null) as MapRef<HTMLDivElement | null>;

    const formState: FormState = useContext(FormDataContext);
    const {formSubmittedToggle} = useContext(FormSubmittedToggleContext);
    const buildingsQuery = useBuildings({campus: "UBCV"}, {id: "buildings"});
    const timeslotsQuery = useTimeslots(formState, {id: "timeslots", formSubmittedToggle: formSubmittedToggle});

    // Creates a new map if not already created
    function createMap() {
        if (mapContainerRef.current !== null && mapRef.current === null) {
            mapboxgl.accessToken = import.meta.env.PROD ? import.meta.env.VITE_MAPBOX_ACCESS_TOKEN : import.meta.env.VITE_MAPBOX_DEV_ACCESS_TOKEN;
            mapRef.current = new mapboxgl.Map({
                container: mapContainerRef.current as HTMLDivElement,
                center: UBCV_CENTER,
                pitch: 60,
                bearing: 0,
                zoom: 16
            });
        }
    }

    // Updates loaded map with markers
    function updateMarkers() {
        if (buildingsQuery.data !== undefined && timeslotsQuery.data !== undefined) {
            // Keep all buildings that have timeslots initially or when filter list is empty,
            // otherwise only keep selected buildings that have timeslots
            let geojson: MapSource = {} as MapSource;
            if (formState.buildings === undefined || formState.buildings.length === 0) {
                geojson = transformToGeoJson(buildingsQuery.data.filter((building) => {
                    return Object.hasOwn(timeslotsQuery.data, building.building_code)
                }));
            } else {
                geojson = transformToGeoJson(buildingsQuery.data.filter((building) => {
                    return formState.buildings?.includes(building.building_code) &&
                    Object.hasOwn(timeslotsQuery.data, building.building_code)
                }));
            }

            if (mapRef.current?.getLayer(BUILDING_LAYER_ID) === undefined) {
                // layer has not been set before
                mapRef.current?.on('load', () => {
                    mapRef.current?.addSource(BUILDING_LAYER_ID, geojson as SourceSpecification)
                    .addLayer({
                        id: BUILDING_LAYER_ID,
                        type: 'circle',
                        source: BUILDING_LAYER_ID,
                        paint: {
                            "circle-radius": 10,
                            "circle-color": "#2684ff"
                        }
                    });
                });
            } else {
                // reset layer
                mapRef.current?.removeLayer(BUILDING_LAYER_ID)
                .removeSource(BUILDING_LAYER_ID)
                .addSource(BUILDING_LAYER_ID, geojson as SourceSpecification)
                .addLayer({
                    id: BUILDING_LAYER_ID,
                    type: 'circle',
                    source: BUILDING_LAYER_ID,
                    paint: {
                        "circle-radius": 10,
                        "circle-color": "#2684ff"
                    }
                });
            }
        }
    }

    function registerEventHandlers() {
        mapRef.current?.on('load', () => {

            // Scroll to timeslot grouping when building marker is clicked on
            mapRef.current?.on('click', BUILDING_LAYER_ID, (e: MapMouseEvent) => {
                const building: MapFeature = mapRef.current?.queryRenderedFeatures(e.point)[0] as MapFeature;
                const buildingProperties = building.properties as BuildingFeatureProperties;
                const timeslotGroup = document.getElementById(buildingProperties.building_code);

                if (timeslotGroup !== null) {
                    timeslotGroup.focus();
                    timeslotGroup.scrollIntoView({behavior: "smooth"});
                }
            });
        });
    }

    useEffect(() => {
        createMap();
        updateMarkers();
        registerEventHandlers();
    }, [buildingsQuery.data, timeslotsQuery.data]);

    return (
        <div className="map-container" ref={mapContainerRef}/>
    );
}