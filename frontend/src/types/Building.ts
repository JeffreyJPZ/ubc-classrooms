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