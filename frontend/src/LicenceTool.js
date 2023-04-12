import { useState } from 'react';

const LicenceTool = () => {

    const [formState, setFormState] = useState({
        cc_by: false,
        cc_by_sa: false,
        cc_by_nc: false,
        cc_by_nc_sa: false,
        cc_by_nd: false,
        cc_by_nc_nd: false,
    })

    const [acceptableLicenses, setAcceptableLicenses] = useState([])
    const [isSubmitted, setIsSubmitted] = useState(false)

    const handleChange = (event) => {
        const { name, checked } = event.target;
        setFormState((prevState) => ({
            ...prevState,
            [name]: checked,
        }));
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        fetch('http://localhost:8000/licensing_tool/',{
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formState)
        }).then(function(response){
            return response.json();
        }).then(function(data){
            setAcceptableLicenses(data.data);
            setIsSubmitted(true);
        });
    };

    return (
        <div>

            <h2 className = "licence-title"> Select Set of Licenses To Remix </h2>
            <form onSubmit={handleSubmit} className = "licence-form">

                <label>
                    <input
                        type = "checkbox"
                        name = "cc_by"
                        checked = {formState.cc_by}
                        onChange = {handleChange}
                    />
                    &nbsp;&nbsp;CC BY
                </label>

                <br />
                <br />

                <label>
                    <input
                        type = "checkbox"
                        name = "cc_by_sa"
                        checked = {formState.cc_by_sa}
                        onChange = {handleChange}
                    />
                    &nbsp;&nbsp;CC BY SA
                </label>

                <br />
                <br />

                <label>
                    <input
                        type = "checkbox"
                        name = "cc_by_nc"
                        checked = {formState.cc_by_nc}
                        onChange = {handleChange}
                    />
                    &nbsp;&nbsp;CC BY NC
                </label>

                <br />
                <br />

                <label>
                    <input
                        type = "checkbox"
                        name = "cc_by_nc_sa"
                        checked = {formState.cc_by_nc_sa}
                        onChange = {handleChange}
                    />
                    &nbsp;&nbsp;CC BY NC SA
                </label>

                <br />
                <br />

                <label>
                    <input
                        type = "checkbox"
                        name = "cc_by_nd"
                        checked = {formState.cc_by_nd}
                        onChange = {handleChange}
                    />
                    &nbsp;&nbsp;CC BY ND
                </label>

                <br />
                <br />

                <label>
                    <input
                        type = "checkbox"
                        name = "cc_by_nc_nd"
                        checked = {formState.cc_by_nc_nd}
                        onChange = {handleChange}
                    />
                    &nbsp;&nbsp;CC BY NC ND
                </label>

            </form>

            {!isSubmitted && <svg width="100" height="100" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" className = "licence-arrow-svg" onClick = {handleSubmit}>
                <rect x="2" y="2" width="13.5" height="13" rx="2" ry="2" fill="#63C1BD" className="click-rect"/>
                <path fill="#fff" d="M4.5 8.5a.5.5 0 0 1 .5-.5h6.293l-1.646-1.647a.5.5 0 1 1 .708-.708l2.5 2.5a.5.5 0 0 1 0 .708l-2.5 2.5a.5.5 0 1 1-.708-.708L10.793 9H5a.5.5 0 0 1-.5-.5z" className="click-arrow"/>
                <path fill="#fff" stroke="#fff" stroke-width="1" d="M4.5 8.5a.5.5 0 0 1 .5-.5h6.293l-1.646-1.647a.5.5 0 1 1 .708-.708l2.5 2.5a.5.5 0 0 1 0 .708l-2.5 2.5a.5.5 0 1 1-.708-.708L10.793 9H5a.5.5 0 0 1-.5-.5z" className="click-arrow"/>
            </svg>
            }

            {isSubmitted && <svg width="100" height="100" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" className = "licence-arrow-svg" onClick = {handleSubmit}>
                <rect x="2" y="2" width="13.5" height="13" rx="2" ry="2" fill="transparent" className="click-rect"/>
                <path fill="#63C1BD" d="M4.5 8.5a.5.5 0 0 1 .5-.5h6.293l-1.646-1.647a.5.5 0 1 1 .708-.708l2.5 2.5a.5.5 0 0 1 0 .708l-2.5 2.5a.5.5 0 1 1-.708-.708L10.793 9H5a.5.5 0 0 1-.5-.5z" className="click-arrow"/>
                <path fill="#63C1BD" stroke="#63C1BD" stroke-width="1" d="M4.5 8.5a.5.5 0 0 1 .5-.5h6.293l-1.646-1.647a.5.5 0 1 1 .708-.708l2.5 2.5a.5.5 0 0 1 0 .708l-2.5 2.5a.5.5 0 1 1-.708-.708L10.793 9H5a.5.5 0 0 1-.5-.5z" className="click-arrow"/>
            </svg>}

            <div className = "acceptable-licenses-container">
                <div className = "acceptable-licenses">
                    {acceptableLicenses.map((licence) => (
                        <h2> {licence} </h2>
                    ))}
                </div>
            </div>

        </div>
    );

};

export default LicenceTool;