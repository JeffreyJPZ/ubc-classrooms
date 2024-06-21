import { useContext } from "react";
import { Combobox, Option} from "./Combobox";
import { FormStateTypes, FormDispatchContext, FormSubmittedContext } from "../contexts";
import { useBuildings, useRoomTypes } from "../api";
import { getCurrentISODate } from "../../../lib/getCurrentISODate";
import { createISODates } from "../../../lib/createISODates";
import { createTimeIntervals } from "../../../lib/createTimeIntervalsAMPM";

import './FormInputs.css';

export function FormInputs() {
    const formDispatch = useContext(FormDispatchContext);
    const {setFormSubmitted} = useContext(FormSubmittedContext);

    return (
        <div className="filters">
            <div className="filter">
                <div className="filter-name">Campus</div>
                <Combobox required={true} isMulti={false} isClearable={false} defaultValue="UBCV" defaultLabel="UBCV" options={[{value: "UBCV", label: "UBCV"}]} optionValue="value" optionLabel="label" onChange={(e) => formDispatch({type: FormStateTypes.CAMPUS, value: e !== null ? (e as Option).value : ""})} />
            </div>
            <div className="filter">
                <div className="filter-name">Date</div>
                <Combobox required={true} isMulti={false} isClearable={false} defaultValue={getCurrentISODate()} defaultLabel={getCurrentISODate()} options={createISODates(getCurrentISODate(), 14)} optionValue="value" optionLabel="label" onChange={(e) => formDispatch({type: FormStateTypes.DATE, value: e !== null ? (e as Option).value : ""})} />
            </div>
            <div className="filter">
                <div className="filter-name">Available From</div>
                <Combobox required={false} isMulti={false} isClearable={true} options={createTimeIntervals("07:00", "22:00", 30)} optionValue="value" optionLabel="label" onChange={(e) => formDispatch({type: FormStateTypes.START, value: e !== null ? (e as Option).value : ""})} />
            </div>
            <div className="filter">
                <div className="filter-name">Available Until</div>
                <Combobox required={false} isMulti={false} isClearable={true} options={createTimeIntervals("07:00", "22:00", 30)} optionValue="value" optionLabel="label" onChange={(e) => formDispatch({type: FormStateTypes.END, value: e !== null ? (e as Option).value : ""})} />
            </div>
            <div className="filter">
                <div className="filter-name">Buildings</div>
                <Combobox required={false} isMulti={true} isClearable={true} query={useBuildings({campus: "UBCV"})} queryValue="building_code" queryLabel="building_name" onChange={(e) => formDispatch({type: FormStateTypes.BUILDINGS, value: (e as readonly Option[]).map(option => option.value) as string[]})} />
            </div>
            <div className="filter">
                <div className="filter-name">Room Types</div>
                <Combobox required={false} isMulti={true} isClearable={true} query={useRoomTypes({campus: "UBCV"})} queryValue="room_type" queryLabel="room_type" onChange={(e) => formDispatch({type: FormStateTypes.ROOM_TYPES, value: (e as readonly Option[]).map(option => option.value) as string[]})}/>
            </div>
            <button className="filter-button" onClick={() => setFormSubmitted(true)}>Search</button>
        </div>
    );
};