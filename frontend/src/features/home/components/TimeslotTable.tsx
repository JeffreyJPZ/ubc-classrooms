import { useContext, useEffect } from "react";
import { FormDataContext, FormSubmittedContext } from "../contexts";
import { useTimeslots } from "../api";

export function TimeslotTable() {
    const formState = useContext(FormDataContext);
    const {formSubmitted, setFormSubmitted} = useContext(FormSubmittedContext);
    const timeslotsQuery = useTimeslots(formState, [formSubmitted]);

    useEffect(() => {
        console.log(formState)
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
        <>
            {timeslotsQuery.data.map(timeslot => {
                return (
                    <div>{timeslot.building_code} {timeslot.room} {timeslot.date} {timeslot.start} {timeslot.end} </div>
                );
            })};
        </>
    );
};