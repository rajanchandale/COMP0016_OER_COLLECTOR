import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';

import NavBar from './NavBar';
import X5Gon_Navbar from './X5Gon_Navbar';
import LandingPage from './LandingPage';
import GeneralStatistics from './GeneralStatistics';
import ActivityStatistics from './ActivityStatistics';
import NewMaterial from './NewMaterial';
import FetchedPlaylists from './FetchedPlaylists';
import FetchedVideos from './FetchedVideos';
import LicenceTool from './LicenceTool';


function App() {
  return (
    <Router>
        <div className="App">
            <NavBar />
            <X5Gon_Navbar />
            <div className = "content">
                <Routes>
                    <Route exact path = "/" element = {<LandingPage />} />
                    <Route exact path = "/general_statistics" element = {<GeneralStatistics />} />
                    <Route exact path = "/activity_statistics" element = {<ActivityStatistics />} />
                    <Route exact path = "/add_materials" element = {<NewMaterial />} />
                    <Route path = "add_materials/playlists/:oer_id" element = {<FetchedPlaylists />} />
                    <Route path = "add_materials/videos/:oer_id" element = {<FetchedVideos />} />
                    <Route exact path = "/licence-tool" element = {<LicenceTool />} />
                </Routes>
            </div>
        </div>
    </Router>
  );
}

export default App;
