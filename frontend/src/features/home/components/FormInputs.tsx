import { useContext } from "react";
import { Combobox, Option} from "./Combobox";
import { FormStateTypes, FormDispatchContext, FormSubmittedContext } from "../contexts";
import { useBuildings, useRoomTypes } from "../api";
import { getCurrentISODate } from "../../../lib/getCurrentISODate";
import { createISODates } from "../../../lib/createISODates";
import { createTimeIntervals } from "../../../lib/createTimeIntervalsAMPM";

export function FormInputs() {
    const formDispatch = useContext(FormDispatchContext);
    const {setFormSubmitted} = useContext(FormSubmittedContext);

    return (
        <div className="filters">
            <div>
                <p>Campus</p>
                <Combobox required={true} isMulti={false} isClearable={false} defaultValue="UBCV" defaultLabel="UBCV" options={[{value: "UBCV", label: "UBCV"}]} optionValue="value" optionLabel="label" onChange={(e) => formDispatch({type: FormStateTypes.CAMPUS, value: e !== null ? (e as Option).value : ""})} />
            </div>
            <div>
                <p>Date</p>
                <Combobox required={true} isMulti={false} isClearable={false} defaultValue={getCurrentISODate()} defaultLabel={getCurrentISODate()} options={createISODates(getCurrentISODate(), 14)} optionValue="value" optionLabel="label" onChange={(e) => formDispatch({type: FormStateTypes.DATE, value: e !== null ? (e as Option).value : ""})} />
            </div>
            <div>
                <p>Start Time</p>
                <Combobox required={false} isMulti={false} isClearable={true} options={createTimeIntervals("07:00", "22:00", 30)} optionValue="value" optionLabel="label" onChange={(e) => formDispatch({type: FormStateTypes.START, value: e !== null ? (e as Option).value : ""})} />
            </div>
            <div>
                <p>End Time</p>
                <Combobox required={false} isMulti={false} isClearable={true} options={createTimeIntervals("07:00", "22:00", 30)} optionValue="value" optionLabel="label" onChange={(e) => formDispatch({type: FormStateTypes.END, value: e !== null ? (e as Option).value : ""})} />
            </div>
            <div>
                <p>Buildings</p>
                <Combobox required={false} isMulti={true} isClearable={true} query={useBuildings({campus: "UBCV"})} queryValue="building_code" queryLabel="building_name" onChange={(e) => formDispatch({type: FormStateTypes.BUILDINGS, value: (e as readonly Option[]).map(option => option.value) as string[]})} />
            </div>
            <div>
                <p>Room Types</p>
                <Combobox required={false} isMulti={true} isClearable={true} query={useRoomTypes({campus: "UBCV"})} queryValue="room_type" queryLabel="room_type" onChange={(e) => formDispatch({type: FormStateTypes.ROOM_TYPES, value: (e as readonly Option[]).map(option => option.value) as string[]})}/>
            </div>
            <button onClick={() => setFormSubmitted(true)}>Search</button>
        </div>
    )
};