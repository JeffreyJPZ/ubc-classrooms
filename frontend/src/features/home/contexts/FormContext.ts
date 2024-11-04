import { Dispatch, SetStateAction, createContext } from 'react';
import { z } from 'zod';

export enum FormStateTypes {
    "CAMPUS",
    "DATE",
    "START",
    "END",
    "BUILDINGS",
    "ROOM_TYPES",
}

export interface FormActions {
    type: FormStateTypes,
    value: string | string[] | undefined,
};

export const FormStateSchema = z.object({
    campus: z.string(),
    date: z.string(),
    start: z.string().optional(),
    end: z.string().optional(),
    buildings: z.array(z.string()).optional(),
    room_types: z.array(z.string()).optional(),
}).refine((data) => {return (data.start === undefined) || (data.end === undefined) || (data.start !== undefined && data.end !== undefined && (new Date(`${data.date} ${data.start}`) < new Date(`${data.date} ${data.end}`)))}, {
    message: `"Available From" must be before "Available Until"`,
    path: ["start"],
});

export type FormState = z.infer<typeof FormStateSchema>;

export const FormDataContext = createContext<FormState>({} as FormState);
export const FormDispatchContext = createContext<Dispatch<FormActions> | (() => void)>(() => {});
export const FormSubmittedToggleContext = createContext({formSubmittedToggle: false, setFormSubmittedToggle: (() => {}) as Dispatch<SetStateAction<boolean>>});