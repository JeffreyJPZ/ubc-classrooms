import { Header } from "../../../components";
import { Footer } from "../../../components";
import { Content } from "../components/Content";

import './Home.css'

export function Home() {
    return (
        <div className="app">
            <Header/>
            <div className="introduction">
                <h1>Looking for a place on campus to study or hang out? Click on any building marker or use the search fields below to get started.</h1>
            </div>
            <main className="main">
                <Content/>
            </main>
            <Footer/>
        </div>
    );
}