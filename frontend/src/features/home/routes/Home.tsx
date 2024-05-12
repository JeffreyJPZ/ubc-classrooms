import { Header } from "../../../components";
import { Footer } from "../../../components";
import { Form } from "../components/Form";
import { TimeslotTable } from "../components/TimeslotTable";
import './Home.css'

export function Home() {
    return (
        <div className="main">
            <Header/>
            <div className="content">
                <div className="introduction">
                    <h1>Looking for a place to study, take meetings, or meet with friends? UBC Classrooms is the right tool for you.</h1>
                </div>
                <Form>
                    <div>
                        <p>Campus</p>
                        <select>
                            <option>UBCV</option>
                        </select>
                    </div>
                    <div>
                        <p>Date</p>
                        <input type="date" required/>
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
                        <select>
                            <option>ALRD - Allard Hall</option>
                            <option>SWNG - West Mall Swing Space</option>
                        </select>
                    </div>
                    <div>
                        <p>Room Types</p>
                        <select>
                            <option>General</option>
                            <option>Restricted</option>
                        </select>
                    </div>
                </Form>
                <TimeslotTable/>
            </div>
            <Footer/>
        </div>
    );
};