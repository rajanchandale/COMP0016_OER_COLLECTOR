# COMP0016_OER_COLLECTOR
Collective GitHub Repo for Systems Engineering OER Collector Project (Team Two)

## Deployment Manual

### Table of Contents

- [Set-up](#set-up)
- [Front-End Deployment](#front-end-deployment)
- [Back-End Deployment](#back-end-deployment)

### Set-Up

This project requires Python 3.x. Follow these steps to set up the project:

In a terminal window, navigate to the local directory you would like to clone the repository to

```git clone https://github.com/rajanchandale/COMP0016_OER_COLLECTOR.git```

Once you have cloned the directory, you should have a project with the following file structure 

```
COMP0016 OER_COLLECTOR
|
|--- backend
| |--- analytics
| | |--- browserdata.py
| | |--- cookiedata.py
| | |--- language.py
| | |--- links.py
| | |--- timedata.py
| | |--- typedata.py
| |
| |--- scraping_subsystem
| | |--- youtube_channel.py
| | |--- youtube_master.py
| | |--- youtube_playlist.py
| | |--- youtube_scraper.py
| | |--- youtube_video.py
| |
| |--- licence.py
| |--- main.py
|
|--- frontend
| |--- public
| | |--- index.html
| |
| |--- src
| | |--- ActivityStatistics.js
| | |--- App.js
| | |--- BarChart.js
| | |--- ChordDiagram.js
| | |--- DoubleBarChart.js
| | |--- DoubleLineGraph.js
| | |--- ExpandedBarChart.js
| | |--- ExpandedChordDiagram.js
| | |--- ExpandedDoubleBarChart.js
| | |--- ExpandedDoubleLineGraph.js
| | |--- ExpandedLineGraph.js
| | |--- ExpandedPieChart.js
| | |--- FetchedPlaylists.js
| | |--- FetchedVideos.js
| | |--- GeneralStatistics.js
| | |--- index.css
| | |--- index.js
| | |--- LandingPage.js
| | |--- LicenceTool.js
| | |--- LineGraph.js
| | |--- NavBar.js
| | |--- NewMaterial.js
| | |--- PieChart.js
| | |--- useD3.js
| | |--- x5gon-logo.png
| | |--- X5Gon-Navbar.js
| |
| |--- package.json
| |--- package-lock.json
|
|--- requirements_windows.txt
|--- requirements_mac_linux.txt
```

Create a terminal session and navigate to the directory titled backend

```cd backend```

If you are using a windows machine, you can download the required Python libraries by running the following command:

```pip3 install -r requirements_windows.txt```

If you are using a Mac or Linux machine, you can download the required Python libraries by running the following command:

```pip3 install -r requirements_mac_linux.txt```

Node JS is a pre-requisite for this project and can be installed from the following link

```https://nodejs.org/en/download```

We would recommend downloading the LTS version as it is recommended for most users and is more likely to be stable
Then, follow the installation wizard for Node JS 

Once Node JS has been installed onto your machine, create a new terminal session and navigate to the directory titled frontend

```cd frontend```

Install the required node modules by entering the following command

```npm install```

After executing this command, the file structure for this project should now look like this

```
COMP0016 OER_COLLECTOR
|
|--- backend
| |--- analytics
| | |--- browserdata.py
| | |--- cookiedata.py
| | |--- language.py
| | |--- links.py
| | |--- timedata.py
| | |--- typedata.py
| |
| |--- scraping_subsystem
| | |--- youtube_channel.py
| | |--- youtube_master.py
| | |--- youtube_playlist.py
| | |--- youtube_scraper.py
| | |--- youtube_video.py
| |
| |--- licence.py
| |--- main.py
| |--- requirements_windows.txt
| |--- requirements_mac_linux.txt
|
|--- frontend
| |--- node_modules
| | |--- .bin
| | | |--- ...
| | |--- .cache
| | | |--- ...
| | |--- @adobe
| | | |--- ...
| | |--- ...
| |
| |--- public
| | |--- index.html
| |
| |--- src
| | |--- ActivityStatistics.js
| | |--- App.js
| | |--- BarChart.js
| | |--- ChordDiagram.js
| | |--- DoubleBarChart.js
| | |--- DoubleLineGraph.js
| | |--- ExpandedBarChart.js
| | |--- ExpandedChordDiagram.js
| | |--- ExpandedDoubleBarChart.js
| | |--- ExpandedDoubleLineGraph.js
| | |--- ExpandedLineGraph.js
| | |--- ExpandedPieChart.js
| | |--- FetchedPlaylists.js
| | |--- FetchedVideos.js
| | |--- GeneralStatistics.js
| | |--- index.css
| | |--- index.js
| | |--- LandingPage.js
| | |--- LicenceTool.js
| | |--- LineGraph.js
| | |--- NavBar.js
| | |--- NewMaterial.js
| | |--- PieChart.js
| | |--- useD3.js
| | |--- x5gon-logo.png
| | |--- X5Gon-Navbar.js
| |
| |--- package.json
| |--- package-lock.json
```

The set-up is now complete and you are ready to run the project

### Front-End Deployment
In a new terminal session navigate to the directory titled frontend 

```cd frontend```

Once you are in the frontend directory, enter the following command to run the frontend server 

```npm run start```

The frontend should now be running on 

```http://localhost:3000/```

### Back-End Deployment
If you have access to the X5Gon database, replace the placeholders in all python files in the analytics sub-directory for the database login credentials with your own login credentials

If you have an API-Key for the YoutubeAPI v3, replace the placeholder for self.api_key in the youtube_master.py file with your own developer API Key

In a new terminal session navigate to the directory titled backend

```cd backend```

Once you are in the backend directory, enter the following command to run the backend server

```python3 -m uvicorn main:app --reload```

The backend should now be running on 

```http://localhost:8000/```

#### NOTE for the project to operate as intended, the two terminal sessions for the front-end and back-end servers should be running concurrently 

### Contributors

Rajan Chandale

```https://github.com/rajanchandale```

```https://www.linkedin.com/in/rajan-chandale-0ba001199/```

```rajan.chandale.21@ucl.ac.uk```


Pragya Sinha

```https://github.com/Ibseum```

```https://www.linkedin.com/in/pragya-sinha-baa71a191/```

```pragya.sinha.21@ucl.ac.uk```

Wesley Choy 

```https://github.com/wesleychoyxd```

```https://www.linkedin.com/in/wesley-wing-chi-choy-58300a228/```

```wesley.choy.21@ucl.ac.uk```

### Licence

This work is licenced under the Apache License 2.0.

```https://www.apache.org/licenses/LICENSE-2.0```
