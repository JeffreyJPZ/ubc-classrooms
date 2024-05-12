import { Header } from "../../../components";
import { Footer } from "../../../components";
import { Combobox } from "../components/Combobox";
import { Form } from "../components/Form";
import { TimeslotTable } from "../components/TimeslotTable";
import { useBuildings, useRoomTypes, useTimeslots } from "../api";
import { getCurrentISODate } from "../../../lib/getCurrentISODate";

import './Home.css'

export function Home() {
    return (
        <div className="main">
            <Header/>
            <div className="content">
                <div className="introduction">
                    <h1>Looking for a place to study, take meetings, or meet with friends? UBC Classrooms shows you when and where empty classrooms are available.</h1>
                </div>
                <Form>
                    <div>
                        <p>Campus</p>
                        <Combobox isMulti={false} defaultValue="UBCV" defaultLabel="UBCV" options={[{value: "UBCV", label: "UBCV"}]} optionValue="value" optionLabel="label" />
                    </div>
                    <div>
                        <p>Date</p>
                        <input type="date" required defaultValue={getCurrentISODate()}/>
                    </div>
                    <div>
                        <p>Start Time</p>
                        <input type="time" min="07:00" max="22:00" />
                    </div>
                    <div>
                        <p>End Time</p>
                        <input type="time" min="07:00" max="22:00" />
                    </div>
                    <div>
                        <p>Buildings</p>
                        <Combobox isMulti={true} query={useBuildings({campus: "UBCV"})} queryValue="building_code" queryLabel="building_name"/>
                    </div>
                    <div>
                        <p>Room Types</p>
                        <Combobox isMulti={true} query={useRoomTypes({campus: "UBCV"})} queryValue="room_type" queryLabel="room_type"/>
                    </div>
                </Form>
                <TimeslotTable/>
            </div>
            <Footer/>
        </div>
    );
};