import { Header } from "../../../components";
import { Footer } from "../../../components";
import { Form } from "../components/Form";

import './Home.css'

export function Home() {
    return (
        <div className="main">
            <Header/>
            <div className="content">
                <div className="introduction">
                    <h1>Looking for a place to study, take meetings, or meet with friends? UBC Classrooms shows you when and where empty classrooms are available.</h1>
                </div>
                {/* Wrap form and timeslot table with a context, with form data as state, use on blur for date*/}
                <Form/>
            </div>
            <Footer/>
        </div>
    );
};