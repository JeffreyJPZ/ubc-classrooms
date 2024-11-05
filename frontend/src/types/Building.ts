import { Feature, FeatureCollection, GeoJsonProperties, Geometry } from 'geojson';
import { LngLatLike } from 'mapbox-gl'
import { z } from 'zod';

export const BuildingSchema = z.object({
    campus: z.string().refine((s) => s === "UBCV", {
        message: `Campus must be "UBCV"`
    }),
    building_code: z.string(),
    building_name: z.string(),
    building_address: z.string(),
    latitude: z.string(),
    longitude: z.string()
});
export const BuildingsSchema = z.array(BuildingSchema);

export type Building = z.infer<typeof BuildingSchema>;
export type Buildings = z.infer<typeof BuildingsSchema>;

export interface MapSource {
    type: string;
    data: MapFeatureCollection
}
export type MapFeatureCollection = FeatureCollection<Geometry, GeoJsonProperties>;
export type MapFeature = Feature<Geometry, GeoJsonProperties>;
export type Coordinates = LngLatLike;