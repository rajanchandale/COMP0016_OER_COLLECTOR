import { Link } from 'react-router-dom';

const NotFound = () => {

    return (

        <div className = "not-found">
            <h1> Sorry! That Page Does Not Exist </h1>

            <Link to = "/" className = "take-me-home">
                <h2> Take Me Home ... </h2>
            </Link>
        </div>

    )

}

export default NotFound;