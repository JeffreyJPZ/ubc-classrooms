import { useState } from "react";
import { Timeslot } from "../../../types";
import { getTimeAMPM } from "../../../lib/getTimeAMPM";

type TimeslotGroupProps = {
    name: string,
    data: Record<string, Timeslot[]>,
}

export function TimeslotGroup({name, data}: TimeslotGroupProps) {
    const [isContentVisible, setContentVisible] = useState(false);

    return (
        <details className="timeslot-group">

            {/* Combine full building name and code */}
            <summary className="timeslot-group-name" onClick={() => setContentVisible(isContentVisible => !isContentVisible)}>{`${Object.values(data)[0][0].building_name} (${name})`}</summary>

            {/* Only show timeslots if they should be visible */}
            {isContentVisible && 
                /* Should probably memoize this */
                <div className="timeslot-group-content">
                    {Object.keys(data).map((room) => {
                        return (
                            <div key={room} className="timeslot">
                                <div className="room">{`${name} ${room}`}</div>
                                <div className="room-type">{`${data[room][0].room_type}`}</div>
                                <div className="date">{`${data[room][0].date}`}</div>

                                {/* Combine all availabilities */}
                                <div className="availabilities">
                                    {data[room].map((timeslot: Timeslot) => {
                                        return (
                                            <div key={timeslot.start}>{`${getTimeAMPM(timeslot.start)}-${getTimeAMPM(timeslot.end)}`}</div>
                                        );
                                    })}
                                </div>
                            </div>
                        );
                    })}
                </div>
            }

        </details>
    );
};