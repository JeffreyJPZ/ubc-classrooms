/**
 * Handles submission of user input
 */

import { useReducer, useState } from 'react';
import { FormStateTypes, FormActions, FormDataContext, FormDispatchContext, FormState, FormSubmittedContext } from '../contexts';
import { getCurrentISODate } from '../../../lib/getCurrentISODate';

import './Form.css'
import { FormInputs } from './FormInputs';
import { TimeslotGroupTable } from './TimeslotGroupTable';

function formReducer(state: FormState, action: FormActions): FormState {
    switch (action.type) {
        case FormStateTypes.CAMPUS:
            return {
                ...state,
                campus: action.value as string,
            };
        case FormStateTypes.DATE:
            return {
                ...state,
                date: action.value as string,
            };
        case FormStateTypes.START:
            return {
                ...state,
                start: action.value as string,
            };
        case FormStateTypes.END:
            return {
                ...state,
                end: action.value as string,
            };
        case FormStateTypes.BUILDINGS:
            return {
                ...state,
                buildings: action.value as string[],
            };
        case FormStateTypes.ROOM_TYPES:
            return {
                ...state,
                room_types: action.value as string[],
            };
        default:
            return state;
    }
}

const initialFormState: FormState = {
    campus: "UBCV",
    date: getCurrentISODate(),
    start: "",
    end: "",
    buildings: [],
    room_types: [],
}

export function Form() {
    const [formState, formDispatch] = useReducer(formReducer, initialFormState);
    const [formSubmitted, setFormSubmitted]= useState(false);

    return (
        <FormDataContext.Provider value={formState}>
            <FormSubmittedContext.Provider value={{formSubmitted, setFormSubmitted}}>
                <FormDispatchContext.Provider value={formDispatch}>
                    <FormInputs/>
                </FormDispatchContext.Provider>
                <TimeslotGroupTable/>
            </FormSubmittedContext.Provider>
        </FormDataContext.Provider>
    );
};