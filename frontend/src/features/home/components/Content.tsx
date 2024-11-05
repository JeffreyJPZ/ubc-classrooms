/**
 * Handles submission of user input
 */

import {useReducer, useState } from 'react';

import { MapContainer } from './MapContainer';
import { FormStateTypes, FormActions, FormDataContext, FormDispatchContext, FormState, FormSubmittedToggleContext } from '../contexts';
import { getCurrentISODate } from '../../../lib/getCurrentISODate';
import { Form } from './Form';
import { TimeslotGroupTable } from './TimeslotGroupTable';

import './Content.css';

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
    start: undefined,
    end: undefined,
    buildings: undefined,
    room_types: undefined,
}

export function Content() {
    const [formState, formDispatch] = useReducer(formReducer, initialFormState);
    const [formSubmittedToggle, setFormSubmittedToggle]= useState(false);

    return (
        <FormDataContext.Provider value={formState}>
            <FormSubmittedToggleContext.Provider value={{formSubmittedToggle: formSubmittedToggle, setFormSubmittedToggle: setFormSubmittedToggle}}>
                <div className="content">
                    <div className='inputs'>
                        <MapContainer/>
                        <FormDispatchContext.Provider value={formDispatch}>
                            <Form/>
                        </FormDispatchContext.Provider>
                    </div>
                    <TimeslotGroupTable/>
                </div>
            </FormSubmittedToggleContext.Provider>
        </FormDataContext.Provider>
    );
}