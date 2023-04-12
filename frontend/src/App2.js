import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';

import NavBar from './NavBar';
/*import X5Gon_Navbar from './X5Gon_Navbar';
import GeneralStatistics from './GeneralStatistics';
import ActivityStatistics from './ActivityStatistics';
import NewMaterial from './NewMaterial';
import FetchedPlaylists from './FetchedPlaylists';
import FetchingVideos from './FetchingVideos';
import FetchedVideos from './FetchedVideos';
import ViewFetchedMaterials from './ViewFetchedMaterials';
import IngestMaterial from './IngestMaterial';
import NotFound from './NotFound';
import FetchedVideos_2 from './FetchedVideos_2';

import ExampleDateGraph from './ExampleDateGraph';*/

function App() {
  return (
    <Router>
        <div className="App">
            <NavBar />
            /*<X5Gon_Navbar />
            <div className="content">
                <Switch>
                    <Route exact path = "/">
                        <h1> Landing Page</h1>
                    </Route>
                    <Route exact path = "/general_statistics">
                        <GeneralStatistics />
                    </Route>
                    <Route exact path = "/activity_statistics">
                        <ActivityStatistics />
                    </Route>
                    <Route exact path = "/add_materials">
                        <NewMaterial />
                    </Route>
                    <Route path = "/add_materials/playlists/:oer_id">
                        <FetchedPlaylists />
                    </Route>
                    <Route exact path = "/add_materials/fetching_videos">
                        <FetchingVideos />
                    </Route>
                    <Route exact path = "/add_materials/videos/:oer_id">
                        <FetchedVideos />
                    </Route>
                    <Route exact path = "/add_materials/ingest">
                        <IngestMaterial />
                    </Route>
                    <Route exact path = "/rajan">
                        <ExampleDateGraph />
                    </Route>
                    <Route path = "/*">
                        <NotFound />
                    </Route>
                </Switch>
            </div>*/
        </div>
    </Router>
  );
}

export default App;
