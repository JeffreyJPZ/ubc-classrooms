import { useContext, useEffect } from "react";
import { FormDataContext, FormSubmittedToggleContext } from "../contexts";
import { useTimeslots } from "../api";
import { TimeslotGroup } from "./TimeslotGroup";

import './TimeslotGroupTable.css';

export function TimeslotGroupTable() {
    const formState = useContext(FormDataContext);
    const {formSubmittedToggle} = useContext(FormSubmittedToggleContext);
    const timeslotsQuery = useTimeslots(formState, {id: "timeslots", formSubmittedToggle: formSubmittedToggle});

    if (timeslotsQuery.isLoading) {
        return (
            <div>Loading...</div>
        );
    }
    
    if (!timeslotsQuery.data) {
        return (
            <div>Nothing to show...</div>
        );
    }

    return (
        <div className="table">
            {Object.keys(timeslotsQuery.data).map((key) => {
                return <TimeslotGroup key={key} name={key} data={timeslotsQuery.data[key]}/>
            })}
        </div>
    );
}