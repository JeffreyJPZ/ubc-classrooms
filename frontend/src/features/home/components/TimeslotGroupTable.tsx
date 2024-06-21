import { useContext, useEffect } from "react";
import { FormDataContext, FormSubmittedContext } from "../contexts";
import { useTimeslots } from "../api";
import { TimeslotGroup } from "./TimeslotGroup";

export function TimeslotGroupTable() {
    const formState = useContext(FormDataContext);
    const {formSubmitted, setFormSubmitted} = useContext(FormSubmittedContext);
    const timeslotsQuery = useTimeslots(formState, [formSubmitted]);

    useEffect(() => {
        if (formSubmitted) {
            setFormSubmitted(false);
        }
    });

    if (timeslotsQuery.isLoading) {
        return (
            <div>Loading...</div>
        );
    };
    
    if (!timeslotsQuery.data) {
        return (
            <div>Nothing to show...</div>
        );
    };

    return (
        <div className="table">
            {Object.keys(timeslotsQuery.data).map((key) => {
                return <TimeslotGroup key={key} name={key} data={timeslotsQuery.data[key]}/>
            })}
        </div>
    );
};