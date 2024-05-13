import { Dispatch, SetStateAction, createContext } from "react";

export enum FormStateTypes {
    "CAMPUS",
    "DATE",
    "START",
    "END",
    "BUILDINGS",
    "ROOM_TYPES",
}

export type FormState = {
    campus: string,
    date: string,
    start: string,
    end: string,
    buildings: string[],
    room_types: string[],
};

export type FormActions = {
    type: FormStateTypes,
    value: string | string[],
};

export const FormDataContext = createContext<FormState>({} as FormState);
export const FormDispatchContext = createContext<Dispatch<FormActions> | (() => void)>(() => {});
export const FormSubmittedContext = createContext({formSubmitted: false, setFormSubmitted: (() => {}) as Dispatch<SetStateAction<boolean>>});