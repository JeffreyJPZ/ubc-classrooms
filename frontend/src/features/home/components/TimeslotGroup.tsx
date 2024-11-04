import { useState } from "react";
import { Timeslot } from "../../../types";
import { getTimeAMPM } from "../../../lib/getTimeAMPM";

import './TimeslotGroup.css';

type IndicatorArrowProps = {
    className?: string
}

function IndicatorArrow({className}: IndicatorArrowProps) {
    return (
        <div className={className}>
            <svg height="20" width="20" viewBox="0 0 20 20">
                <path d="M4.516 7.548c0.436-0.446 1.043-0.481 1.576 0l3.908 3.747 3.908-3.747c0.533-0.481 1.141-0.446 1.574 0 0.436 0.445 0.408 1.197 0 1.615-0.406 0.418-4.695 4.502-4.695 4.502-0.217 0.223-0.502 0.335-0.787 0.335s-0.57-0.112-0.789-0.335c0 0-4.287-4.084-4.695-4.502s-0.436-1.17 0-1.615z"></path>
            </svg>
        </div>
    )
}

type TimeslotGroupProps = {
    name: string,
    data: Record<string, Timeslot[]>,
};

export function TimeslotGroup({name, data}: TimeslotGroupProps) {
    const [isContentVisible, setContentVisible] = useState(false);

    return (
        <details className={isContentVisible ? "timeslot-group-visible" : "timeslot-group-hidden"}>

            {/* Combine full building name and code */}
            <summary className="timeslot-group-summary" onClick={() => setContentVisible(isContentVisible => !isContentVisible)}>
                <div className="timeslot-group-title">
                    <div className="timeslot-group-name">{`${Object.values(data)[0][0].building_name} (${name})`}</div>
                    <div className="timeslot-group-room-count">{`Rooms: ${Object.keys(data).length}`}</div>
                </div>

                {/* Collapsible indicator arrow */}
                {isContentVisible ? 
                    <IndicatorArrow className="content-visible-indicator"/> :
                    <IndicatorArrow className="content-hidden-indicator"/>
                }
            </summary>
            
            {/* Only show timeslots if they should be visible */}
            {isContentVisible && 
                /* Should probably memoize this */
                <div className="timeslot-group-content">
                    {Object.keys(data).map((room) => {
                        return (
                            <div key={room} className="timeslot">
                                <div className="timeslot-room">{`${name} ${room}`}</div>
                                <div className="timeslot-room-type">{`${data[room][0].room_type}`}</div>

                                {/* Combine all availabilities */}
                                <div className="timeslot-availabilities">
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
}