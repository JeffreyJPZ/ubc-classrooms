import { z } from 'zod';

export const TimeslotSchema = z.object({
    campus: z.string().refine((s) => s === "UBCV", {
        message: `Campus must be "UBCV"`
    }),
    building_code: z.string(),
    building_name: z.string(),
    room: z.string(),
    room_type: z.string(),
    date: z.string(),
    start: z.string(),
    end: z.string(),
});
export const TimeslotsSchema = z.array(TimeslotSchema);

export type Timeslot = z.infer<typeof TimeslotSchema>;
export type Timeslots = z.infer<typeof TimeslotsSchema>;