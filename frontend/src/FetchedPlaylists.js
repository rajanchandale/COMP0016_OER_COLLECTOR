import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

const FetchedPlaylists = () => {

    const { oer_id } = useParams();
    const[playlistData, setPlaylistData] = useState([]);
    const[deletedData, setDeletedData] = useState([]);
    const[isPending, setIsPending] = useState(true);
    const[isIngesting, setIsIngesting] = useState(false);
    const[isFetching, setIsFetching] = useState(true);
    const navigate = useNavigate();

    console.log("FetchedPlaylists Component Rendered")
    console.log("OER_ID: ", oer_id)

    const groupVideosByPlaylist = (videos) => {
        return videos.reduce((acc, video) => {
            const key = video.playlist_title || 'No Playlist';
            if (!acc[key]) {
                acc[key] = [];
            }
            acc[key].push(video);
            return acc;
        }, {});
    };

    const checkLicensing = (videos) => {
        videos.map(video => {
            if (video.licence_available === "Private Video"){
                video.deleted = true;
            }
        })
    }

    useEffect(() => {
        console.log("Fetching Data in useEffect")
        fetch(`http://localhost:8000/add_materials/playlists/${oer_id}`).then(res => res.json()).then(data => {
            setPlaylistData(Object.entries(data.data).map(([key, value]) => {
                return {
                    ...value,
                    deleted: false,
                };
            }));
        }).then(() => {setIsPending(false);setIsFetching(false);}).catch(e => console.log(e.message));
    }, [oer_id]);

    console.log(playlistData)
    console.log(typeof(playlistData))

    const deleteMaterial = (event, deleted_data) => {
        console.log(event)
        const newData = playlistData.filter(video => video[1]['id'] !== deleted_data[1]['id']);
        setPlaylistData(newData);
    }

    const deleteMaterial2 = (event, video) => {
        console.log(event);
        setPlaylistData(
            playlistData.map(v => {
                if (v.id === video.id){
                    return { ...v, deleted: !v.deleted };
                }
                return v;
            })
        );
    };

    const nextScreen = () => {
        setIsIngesting(true);
        setIsPending(true);
        fetch(`http://localhost:8000/ingest_playlists/${oer_id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({playlistData})
        }).then(function(response){
            return response.json();
        }).then(function(data){
            console.log(data.status)
        }).then(() => {
            navigate(`/add_materials/videos/${oer_id}`)
        })
    }

    checkLicensing(playlistData);
    const groupedPlaylists = groupVideosByPlaylist(playlistData);

    return(
        <div className = "material-info-container">
            {!isPending &&
            <div>
                <h1> Pre-Compiled Playlists </h1>
                <svg width="100" height="100" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" onClick = {nextScreen}>
                    <rect x="2" y="2.25" width="13.5" height="12" rx="2" ry="2" fill="#fff" class="click-rect"/>
                    <path fill="#63C1BD" d="M4.5 8.5a.5.5 0 0 1 .5-.5h6.293l-1.646-1.647a.5.5 0 1 1 .708-.708l2.5 2.5a.5.5 0 0 1 0 .708l-2.5 2.5a.5.5 0 1 1-.708-.708L10.793 9H5a.5.5 0 0 1-.5-.5z" class="click-arrow"/>
                    <path fill="#63C1BD" stroke="#63C1BD" stroke-width="1" d="M4.5 8.5a.5.5 0 0 1 .5-.5h6.293l-1.646-1.647a.5.5 0 1 1 .708-.708l2.5 2.5a.5.5 0 0 1 0 .708l-2.5 2.5a.5.5 0 1 1-.708-.708L10.793 9H5a.5.5 0 0 1-.5-.5z" class="click-arrow"/>
                </svg>
                {Object.entries(groupedPlaylists).map(([playlistTitle, videos]) => (
                    <div key = {playlistTitle}>
                        <details>
                            <summary className = "custom-summary">
                                <div className = "collapsible-summary-container">
                                    {playlistTitle === 'No Playlist' ? 'No Playlist': `Playlist: ${playlistTitle}`}
                                </div>
                            </summary>

                            {videos.map((video) => (
                                <div className = {`material-info-div ${video.deleted ? "greyed-out" : ""}`} key = {video.id} >
                                    <img src = {video.thumbnail} alt = "Thumbnail" />
                                    <h2> {video.title} </h2>
                                    <h3> Author(s): {video.channel} </h3>
                                    {video.playlist_title && <h4 className = "playlist-title"> Episode Of {video.playlist_title} </h4>}
                                    <h4 className = "transcript-tag"> Transcript: {video.transcript_available} </h4>
                                    <h4 className = "licence-tag"> Licence: {video.licence_available} </h4>
                                    <div className = "video-description"> <p> <em> {video.description} </em> </p> </div>
                                    <div className="delete-button-container">
                                        {!video.deleted ? (
                                        <button
                                            onClick={(event) => deleteMaterial2(event, video)}
                                            style={{ transform: "rotate(45deg)" }}
                                        >
                                          +
                                        </button>
                                        ) : video.licence_available !== "Private Video" ? (
                                            <button onClick={(event) => deleteMaterial2(event, video)}>
                                                <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                viewBox="0 0 50 50"
                                                width="50"
                                                height="50">
                                                    <path
                                                      d="M15,25 L20,30 L35,15"
                                                      stroke="green"
                                                      strokeWidth="5"
                                                      fill="none"
                                                    />
                                                </svg>
                                            </button>
                                        ) : null}
                                    </div>
                                </div>
                            ))}
                        </details>
                    </div>
                ))}
            </div>
            }

            {isFetching && <div className = "playlist-fetching-messages">

                <div className = "harvesting-svg">
                    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="#63C1BD" class="bi bi-cloud-download" viewBox="0 0 16 16">
                      <path d="M4.406 1.342A5.53 5.53 0 0 1 8 0c2.69 0 4.923 2 5.166 4.579C14.758 4.804 16 6.137 16 7.773 16 9.569 14.502 11 12.687 11H10a.5.5 0 0 1 0-1h2.688C13.979 10 15 8.988 15 7.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 2.825 10.328 1 8 1a4.53 4.53 0 0 0-2.941 1.1c-.757.652-1.153 1.438-1.153 2.055v.448l-.445.049C2.064 4.805 1 5.952 1 7.318 1 8.785 2.23 10 3.781 10H6a.5.5 0 0 1 0 1H3.781C1.708 11 0 9.366 0 7.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z"/>
                      <path d="M7.646 15.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 14.293V5.5a.5.5 0 0 0-1 0v8.793l-2.146-2.147a.5.5 0 0 0-.708.708l3 3z"/>
                    </svg>
                </div>

                <h3 className = "harvesting-message"> Harvesting Open Educational Resources </h3>

                <br />

                <div className = "creating-collections-svg">
                    <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="#63C1BD" class="bi bi-collection-play" viewBox="0 0 16 16">
                        <path d="M2 3a.5.5 0 0 0 .5.5h11a.5.5 0 0 0 0-1h-11A.5.5 0 0 0 2 3zm2-2a.5.5 0 0 0 .5.5h7a.5.5 0 0 0 0-1h-7A.5.5 0 0 0 4 1zm2.765 5.576A.5.5 0 0 0 6 7v5a.5.5 0 0 0 .765.424l4-2.5a.5.5 0 0 0 0-.848l-4-2.5z"/>
                        <path d="M1.5 14.5A1.5 1.5 0 0 1 0 13V6a1.5 1.5 0 0 1 1.5-1.5h13A1.5 1.5 0 0 1 16 6v7a1.5 1.5 0 0 1-1.5 1.5h-13zm13-1a.5.5 0 0 0 .5-.5V6a.5.5 0 0 0-.5-.5h-13A.5.5 0 0 0 1 6v7a.5.5 0 0 0 .5.5h13z"/>
                    </svg>
                </div>

                <h3 className = "creating-collections-message"> Creating Resource Collections </h3>
            </div>}

            {isIngesting &&
                <div className = "playlist-ingesting-message">
                    <div className = "playlist-ingesting-svg">
                        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="#63C1BD" class="bi bi-database-fill-down" viewBox="0 0 16 16">
                          <path d="M12.5 9a3.5 3.5 0 1 1 0 7 3.5 3.5 0 0 1 0-7Zm.354 5.854 1.5-1.5a.5.5 0 0 0-.708-.708l-.646.647V10.5a.5.5 0 0 0-1 0v2.793l-.646-.647a.5.5 0 0 0-.708.708l1.5 1.5a.5.5 0 0 0 .708 0ZM8 1c-1.573 0-3.022.289-4.096.777C2.875 2.245 2 2.993 2 4s.875 1.755 1.904 2.223C4.978 6.711 6.427 7 8 7s3.022-.289 4.096-.777C13.125 5.755 14 5.007 14 4s-.875-1.755-1.904-2.223C11.022 1.289 9.573 1 8 1Z"/>
                          <path d="M2 7v-.839c.457.432 1.004.751 1.49.972C4.722 7.693 6.318 8 8 8s3.278-.307 4.51-.867c.486-.22 1.033-.54 1.49-.972V7c0 .424-.155.802-.411 1.133a4.51 4.51 0 0 0-4.815 1.843A12.31 12.31 0 0 1 8 10c-1.573 0-3.022-.289-4.096-.777C2.875 8.755 2 8.007 2 7Zm6.257 3.998L8 11c-1.682 0-3.278-.307-4.51-.867-.486-.22-1.033-.54-1.49-.972V10c0 1.007.875 1.755 1.904 2.223C4.978 12.711 6.427 13 8 13h.027a4.552 4.552 0 0 1 .23-2.002Zm-.002 3L8 14c-1.682 0-3.278-.307-4.51-.867-.486-.22-1.033-.54-1.49-.972V13c0 1.007.875 1.755 1.904 2.223C4.978 15.711 6.427 16 8 16c.536 0 1.058-.034 1.555-.097a4.507 4.507 0 0 1-1.3-1.905Z"/>
                        </svg>
                    </div>
                    <h3> Ingesting Materials </h3>
                </div>
            }

        </div>
    )

}

export default FetchedPlaylists;