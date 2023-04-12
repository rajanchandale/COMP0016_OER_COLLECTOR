import { useState } from 'react';
import { useNavigate } from 'react-router-dom';


const NewMaterial = () => {
    const[url, setUrl] = useState('');
    const[isPending, setIsPending] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        console.log("handleSubmit")
        e.preventDefault();
        const value = {url};

        setIsPending(true);

        fetch('http://localhost:8000/add_materials', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(value)
        }).then(function(response){
            return response.json();
        }).then(function(data){
            const oer_id = data.data;
            navigate(`/add_materials/playlists/${oer_id}`);
        });
    }

    return(
        <div className="new-url">
            <form onSubmit={ handleSubmit }>
                <input type="text" required value = {url} className = "url-input" placeholder = "Enter URL" onChange = {(e) => setUrl(e.target.value)} />
                {!isPending && <button className = "submit-button"> GO </button> }
                {isPending && <button disabled className = "submit-button-fetching" onClick = {() => console.log("clicked")}> Fetching ... </button>}
                {isPending && <div className = "loading-messages">

                    <div className = "secure-svg">
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="#63C1BD" class="bi bi-lock-fill" viewBox="0 0 16 16">
                            <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/>
                        </svg>
                    </div>

                    <h3 className = "secure-message"> Checking Secure Website </h3>

                    <div className = "checking-oer-svg">
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="#63C1BD" class="bi bi-book-fill" viewBox="0 0 16 16">
                            <path d="M8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783z"/>
                        </svg>
                    </div>

                    <h3 className = "checking-oer-message"> Confirming Open Educational Resources </h3>

                    <div className = "resource-licence-svg">
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="#63C1BD" class="bi bi-clipboard2-check-fill" viewBox="0 0 16 16">
                            <path d="M10 .5a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5.5.5 0 0 1-.5.5.5.5 0 0 0-.5.5V2a.5.5 0 0 0 .5.5h5A.5.5 0 0 0 11 2v-.5a.5.5 0 0 0-.5-.5.5.5 0 0 1-.5-.5Z"/>
                            <path d="M4.085 1H3.5A1.5 1.5 0 0 0 2 2.5v12A1.5 1.5 0 0 0 3.5 16h9a1.5 1.5 0 0 0 1.5-1.5v-12A1.5 1.5 0 0 0 12.5 1h-.585c.055.156.085.325.085.5V2a1.5 1.5 0 0 1-1.5 1.5h-5A1.5 1.5 0 0 1 4 2v-.5c0-.175.03-.344.085-.5Zm6.769 6.854-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 9.793l2.646-2.647a.5.5 0 0 1 .708.708Z"/>
                        </svg>
                    </div>

                    <h3 className = "resource-licence-message"> Checking Resource Licenses </h3>
                </div>}
            </form>
        </div>

    );
}

export default NewMaterial;