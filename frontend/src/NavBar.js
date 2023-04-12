import { Link } from 'react-router-dom';

const NavBar = () => {

    return(
        <nav className = "navbar">
            <h2>Admin<br/>Panel</h2>

            <Link to = "/">
                <button style = {{top:"17.5%"}}> <b>Home</b> </button>
            </Link>

            <Link to = "/general_statistics">
                <button style = {{top:"32.5%"}}> <b>General Statistics</b> </button>
            </Link>

            <Link to = "/activity_statistics">
                <button style = {{top:"47.5%"}}> <b>Activity Statistics</b> </button>
            </Link>

            <Link to = "/add_materials">
                <button style = {{top:"62.5%"}}> <b>Add<br/>Material</b> </button>
            </Link>

            <Link to = "/licence-tool">
                <button style = {{top: "77.5%"}}> <b>Licence<br/>Tool</b> </button>
            </Link>

        </nav>
    );

};

export default NavBar;
