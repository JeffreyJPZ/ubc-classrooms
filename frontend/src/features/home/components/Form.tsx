import { useState, useContext } from "react";
import { ZodFormattedError } from "zod";

import { Combobox, Option} from "./Combobox";
import { FormState, FormStateTypes, FormStateSchema, FormDispatchContext, FormSubmittedToggleContext, FormDataContext } from "../contexts";
import { useBuildings, useRoomTypes } from "../api";
import { getCurrentISODate } from "../../../lib/getCurrentISODate";
import { createISODates } from "../../../lib/createISODates";
import { createTimeIntervals } from "../../../lib/createTimeIntervalsAMPM";

import './Form.css';

type FormErrors = ZodFormattedError<FormState>;

export function Form() {
    const formState = useContext(FormDataContext);
    const formDispatch = useContext(FormDispatchContext);
    const {formSubmittedToggle, setFormSubmittedToggle} = useContext(FormSubmittedToggleContext);
    const [errors, setErrors] = useState({} as FormErrors);

    function parseForm(formState: FormState) {
        const result = FormStateSchema.safeParse(formState);
        if (!result.success) {
            setErrors(result.error.format());
        } else {
            setErrors({} as FormErrors);
            // Use toggle to prevent rerender instead of resetting value
            setFormSubmittedToggle(!formSubmittedToggle);
        }
    }

    return (
        <div className="filters">
            <div className="filter">
                <div className="filter-name">Campus</div>
                <Combobox required={true} isMulti={false} isClearable={false} defaultValue="UBCV" defaultLabel="Vancouver" options={[{value: "UBCV", label: "Vancouver"}]} optionValue="value" optionLabel="label" onChange={(e) => formDispatch({type: FormStateTypes.CAMPUS, value: e !== null ? (e as Option).value : undefined})} />
            </div>
            <div className="filter">
                <div className="filter-name">Date</div>
                <Combobox required={true} isMulti={false} isClearable={false} defaultValue={getCurrentISODate()} defaultLabel={getCurrentISODate()} options={createISODates(getCurrentISODate(), 7)} optionValue="value" optionLabel="label" onChange={(e) => formDispatch({type: FormStateTypes.DATE, value: e !== null ? (e as Option).value : undefined})} />
            </div>
            <div className="filter">
                <div className="filter-name">Available From</div>
                <Combobox required={false} isMulti={false} isClearable={true} options={createTimeIntervals("07:00", "22:00", 30)} optionValue="value" optionLabel="label" onChange={(e) => formDispatch({type: FormStateTypes.START, value: e !== null ? (e as Option).value : undefined})} />
            </div>
            <div className="filter">
                <div className="filter-name">Available Until</div>
                <Combobox required={false} isMulti={false} isClearable={true} options={createTimeIntervals("07:00", "22:00", 30)} optionValue="value" optionLabel="label" onChange={(e) => formDispatch({type: FormStateTypes.END, value: e !== null ? (e as Option).value : undefined})} />
            </div>
            <div className="filter">
                <div className="filter-name">Buildings</div>
                <Combobox required={false} isMulti={true} isClearable={true} query={useBuildings({campus: "UBCV"}, {id: "buildings"})} queryValue="building_code" queryLabel="building_name" onChange={(e) => formDispatch({type: FormStateTypes.BUILDINGS, value: e ? (e as readonly Option[]).map(option => option.value) as string[] : undefined})} />
            </div>
            <div className="filter">
                <div className="filter-name">Room Types</div>
                <Combobox required={false} isMulti={true} isClearable={true} query={useRoomTypes({campus: "UBCV"}, {id: "roomtypes"})} queryValue="room_type" queryLabel="room_type" onChange={(e) => formDispatch({type: FormStateTypes.ROOM_TYPES, value: e ? (e as readonly Option[]).map(option => option.value) as string[] : undefined})}/>
            </div>
            <button className="filter-button" onClick={() => parseForm(formState)}>Search</button>
            {errors?.start?._errors && <div className="errors">{errors.start._errors.map(err => <div key={err} className="error">{err}</div>)}</div>}
        </div>
    );
}