import { Header } from "../../../components";
import { Footer } from "../../../components";
import { Form } from "../components/Form";

import './Home.css'

export function Home() {
    return (
        <div className="app">
            <Header/>
            <div className="introduction">
                <h1>Looking for a place to study, take meetings, or meet with friends? UBC Classrooms shows you when and where empty classrooms are available.</h1>
            </div>
            <main className="content">
                <Form/>
            </main>
            <Footer/>
        </div>
    );
};