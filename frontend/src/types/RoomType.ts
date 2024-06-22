import { z } from 'zod';

export const RoomTypeSchema = z.object({
    campus: z.string().refine((s) => s === "UBCV", {
        message: `Campus must be "UBCV"`
    }),
    room_type: z.string(),
});
export const RoomTypesSchema = z.array(RoomTypeSchema);

export type RoomType = z.infer<typeof RoomTypeSchema>;
export type RoomTypes = z.infer<typeof RoomTypesSchema>;