import { useState, useEffect } from 'react';

import BarChart from './BarChart';
import PieChart from './PieChart';
import DoubleBarChart from './DoubleBarChart';

import ExpandedBarChart from './ExpandedBarChart';
import ExpandedPieChart2 from './ExpandedPieChart2';
import ExpandedDoubleBarChart from './ExpandedDoubleBarChart';

const GeneralStatistics = () => {

    const [userBrowserData, setUserBrowserData] = useState([]);
    const [materialLanguageData, setMaterialLanguageData] = useState([]);
    const [userLanguageData, setUserLanguageData] = useState([]);
    const [materialTypeData, setMaterialTypeData] = useState([]);
    const [deviceNameData, setDeviceNameData] = useState([]);
    const [videoTypeData, setVideoTypeData] = useState([]);
    const [languageComparisonData, setLanguageComparisonData] = useState([]);

    const [expandedGraph, setExpandedGraph] = useState(false);
    const [expandedUserBrowser, setExpandedUserBrowser] = useState(false);
    const [expandedMaterialLanguage, setExpandedMaterialLanguage] = useState(false);
    const [expandedUserLanguages, setExpandedUserLanguages] = useState(false);
    const [expandedMaterialTypeData, setExpandedMaterialTypeData] = useState(false);
    const [expandedUserDevice, setExpandedUserDevice] = useState(false);
    const [expandedVideoType, setExpandedVideoType] = useState(false);
    const [expandedLanguageComparisonData, setExpandedLanguageComparisonData] = useState(false);

    const[Height, setHeight] = useState(270);
    const[Width, setWidth] = useState(410);

    const [YLabel, setYLabel] = useState('');
    const [XLabel, setXLabel] = useState('');

    const [isPending, setIsPending] = useState(true);

    const expandUserBrowser = () => {
        setExpandedUserBrowser(true);
        setExpandedGraph(true);
        setHeight(450);
        setWidth(600);
        setXLabel("Web Browser");
        setYLabel("Number of Users");
    }

    const expandMaterialLanguage = () => {
        setExpandedMaterialLanguage(true);
        setExpandedGraph(true);
        setHeight(450);
        setWidth(600);
    }

    const expandMaterialTypeData = () => {
        setExpandedMaterialTypeData(true);
        setExpandedGraph(true);
        setHeight(450);
        setWidth(600);
    }

    const expandUserDevice = () => {
        setExpandedUserDevice(true);
        setExpandedGraph(true);
        setHeight(450);
        setWidth(600);
        setXLabel("User Device/Operating System");
        setYLabel("Number of Users");
    }

    const expandVideoType = () => {
        setExpandedVideoType(true);
        setExpandedGraph(true);
        setHeight(450);
        setWidth(600);
    }

    const expandLanguageComparison = () =>{
        setExpandedLanguageComparisonData(true);
        setExpandedGraph(true);
        setHeight(450);
        setWidth(600);
    }

    const expandUserLanguageData = () => {
        setExpandedUserLanguages(true);
        setExpandedGraph(true);
        setHeight(450);
        setWidth(600);
    }

    const closeModal = () => {
        setHeight(250);
        setWidth(350);
        setExpandedGraph(false);
        setExpandedUserBrowser(false);
        setExpandedMaterialLanguage(false);
        setExpandedUserLanguages(false);
        setExpandedMaterialTypeData(false);
        setExpandedUserDevice(false);
        setExpandedVideoType(false)
        setExpandedLanguageComparisonData(false);
    }

    const handleClick = (event, d) => {
        if(d.data[1]['name'] === 'Video'){
            setExpandedMaterialTypeData(false);
            setExpandedVideoType(true);
            setExpandedGraph(true);
            setHeight(450);
            setWidth(600);
        };
    }

    const handleChartClick = (event) => {
        event.stopPropagation();
    }

    useEffect(() => {
        fetch("http://localhost:8000/general_statistics").then(res => res.json()).then(data => {
            setUserBrowserData(Object.entries(data['data']['user_browser']));
            setMaterialLanguageData(Object.entries(data['data']['material_language_data']));
            setUserLanguageData(Object.entries(data['data']['user_language_data']));
            setMaterialTypeData(Object.entries(data['data']['material_type_data']));
            setDeviceNameData(Object.entries(data['data']['device_name_data']));
            setVideoTypeData(Object.entries(data['data']['video_type_data']))
            setLanguageComparisonData(Object.entries(data['data']['language_comparison_data']));
        }).then(() => {
            if(userBrowserData !== []){
                setIsPending(false);
            };
        }).catch(e => console.log(e.message));
    }, [])

    return(
        <div>

            {!expandedGraph &&
            <div className = "user-browser-box" onClick = {expandUserBrowser} >

                {!isPending &&
                <div className = "example-bar-chart">
                    <BarChart data = {userBrowserData} height = {270} width = {410} />
                </div>}

                {isPending && <div className = "loader" />}

                <h5> User Browser </h5>
            </div> }

            {expandedUserBrowser &&
            <div onClick = {closeModal} className = "overlay">
                <div className = "modal-container">
                    <ExpandedBarChart data = {userBrowserData} height = {Height} width = {Width} yLabel = {YLabel} xLabel = {XLabel} onChartClick = {handleChartClick}/>
                    <h2 onClick = {closeModal}> + </h2>
                </div>
            </div>
            }

            {!expandedGraph &&
            <div className = "user-device-box" onClick = {expandUserDevice}>
                {!isPending &&
                <div className = "example-bar-chart">
                    <BarChart data = {deviceNameData} height = {270} width = {410} />
                </div>
                }

                {isPending && <div className = "loader" />}

                <h5> User Device </h5>

            </div>
            }

            {expandedUserDevice &&
            <div onClick = {closeModal} className = "overlay">
                <div className = "modal-container">
                    <ExpandedBarChart data = {deviceNameData} height = {Height} width = {Width} xLabel = {XLabel} yLabel = {YLabel} onChartClick = {handleChartClick}/>
                    <h2 onClick = {closeModal}> + </h2>
                </div>
            </div>
            }

            {!expandedGraph &&
            <div className = "material-language-box" onClick = {expandMaterialLanguage}>
                {!isPending &&
                <div className = "example-pie-chart">
                    <PieChart data = {materialLanguageData} height = {212.5} width = {315} />
                </div>
                }
                {isPending && <div className = "loader" /> }
                <h5> Material Languages </h5>
            </div>
            }

            {expandedMaterialLanguage &&
            <div onClick = {closeModal} className = "overlay">
                <div className = "modal-container">
                    <h2 onClick = {closeModal} > + </h2>
                    <ExpandedPieChart2 data = {materialLanguageData} height = {Height} width = {Width} onChartClick = {handleChartClick} />
                </div>
            </div>
            }

            {expandedVideoType &&
            <div onClick = {closeModal} className = "overlay">
                <div className = "modal-container">
                    <h2 onClick = {closeModal}> + </h2>
                    <ExpandedPieChart2 data = {videoTypeData} height ={Height} width = {Width} onChartClick = {handleChartClick} />
                </div>
            </div>
            }

            {!expandedGraph &&
            <div className = "video-type-box" onClick = {expandLanguageComparison}>
                {!isPending &&
                <div className = "example-double-bar">
                    <DoubleBarChart data = {languageComparisonData} height = {250} width = {350} />
                </div>
                }

                {isPending && <div className = "loader" />}
                <h5> Language Comparison </h5>
            </div>
            }

            {expandedLanguageComparisonData &&
            <div onClick = {closeModal} className = "overlay">
                <div className = "modal-container">
                    <h2 onClick = {closeModal}> + </h2>
                    <ExpandedDoubleBarChart data = {languageComparisonData} height = {Height} width = {Width} onChartClick = {handleChartClick} />
                </div>
            </div>
            }

            {!expandedGraph &&
            <div className = "user-language-box" onClick = {expandUserLanguageData}>
                {!isPending &&
                    <div className = "example-pie-chart">
                        <PieChart data = {userLanguageData} height = {212.5} width = {315} />
                    </div>
                }

                {isPending && <div className = "loader" /> }

                <h5> User Languages </h5>
            </div>
            }

            {expandedUserLanguages &&
            <div onClick = {closeModal} className = "overlay">
                <div className = "modal-container">
                    <h2 onClick = {closeModal}> + </h2>
                    <ExpandedPieChart2 data = {userLanguageData} height = {Height} width = {Width} onChartClick = {handleChartClick} />
                </div>
            </div>
            }

            {!expandedGraph &&
            <div className = "material-types-box" onClick = {expandMaterialTypeData}>
                {!isPending &&
                    <div className = "example-pie-chart">
                        <PieChart data = {materialTypeData} height = {212.5} width = {315} />
                    </div>
                }

                {isPending && <div className = "loader" />}


                <h5> Material Types </h5>
            </div>
            }

            {expandedMaterialTypeData &&
            <div onClick = {closeModal} className = "overlay">
                <div className = "modal-container">
                    <h2 onClick = {closeModal}> + </h2>
                    <ExpandedPieChart2 data = {materialTypeData} height = {Height} width = {Width} onClick = {handleClick} onChartClick = {handleChartClick} />
                </div>
            </div>
            }

        </div>
    );

};

export default GeneralStatistics;

