import { Link } from "react-router-dom";

function Navbar() {
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                <li class="nav-item active">
                    <Link to="/" className="nav-link">Home</Link>
                </li>
                <li class="nav-item">
                    <Link to="/transcendence" className="nav-link">Transcendence</Link>
                </li>
                <li class="nav-item">
                    <Link to="/about" className="nav-link">About</Link>
                </li>
                </ul>
            </div>
        </nav>
    );
}

export default Navbar;