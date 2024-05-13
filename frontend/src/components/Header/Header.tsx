import githubMark from "../../assets/github-mark.svg";
import './Header.css';

export function Header() {
    return (
        <header className="header">
            <a className="logo">UBC Classrooms</a>
            <div className="credits">
                <p className="authors">Made by Jeffrey Z and Eric Y</p>
                <a className="links" href="https://github.com/JeffreyJPZ/ubc-classrooms" target="_blank">
                    <img src={githubMark} alt="Github repository link"></img>
                </a>
            </div>
        </header>
    );
};