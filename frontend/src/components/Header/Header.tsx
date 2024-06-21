import githubMark from "../../assets/github-mark.svg";
import './Header.css';

export function Header() {
    return (
        <header className="header">
            <a className="logo" href=".">UBC Classrooms</a>
            <nav className="credits">
                <a className="links" href="https://github.com/JeffreyJPZ/ubc-classrooms" target="_blank">
                    <img src={githubMark} alt="Github repository link"></img>
                </a>
            </nav>
        </header>
    );
};