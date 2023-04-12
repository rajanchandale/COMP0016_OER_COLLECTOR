import { useState, useEffect } from 'react';

import LineGraph from './LineGraph';
import DoubleLineGraph from './DoubleLineGraph';
import ChordDiagram from './ChordDiagram';

import ExpandedLineGraph from './ExpandedLineGraph';
import ExpandedDoubleLineGraph from './ExpandedDoubleLineGraph';
import ExpandedChordDiagram from './ExpandedChordDiagram';

const ActivityStatistics = () => {

    const [cookieEventsData, setCookieEventsData] = useState([]);
    const [usersWeekData, setUsersWeekData] = useState([]);
    const [usersMonthData, setUsersMonthData] = useState([]);
    const [linksBetweenMaterials, setLinksBetweenMaterials] = useState([]);
    const [monthComparisonData, setMonthComparisonData] = useState([]);

    const [expandedGraph, setExpandedGraph] = useState(false);
    const [expandedCookieEventsData, setExpandedCookieEventsData] = useState(false);
    const [expandedUsersWeekData, setExpandedUsersWeekData] = useState(false);
    const [expandedUsersMonthData, setExpandedUsersMonthData] = useState(false);
    const [expandedLinksBetweenMaterials, setExpandedLinksBetweenMaterials] = useState(false);
    const [expandedMonthComparisonData, setExpandedMonthComparisonData] = useState(false);

    const [Height, setHeight] = useState(250);
    const [Width, setWidth] = useState(360);

    const [isPending, setIsPending] = useState(true);

    const expandCookieEventsData = () => {
        setExpandedCookieEventsData(true);
        setExpandedGraph(true);
        setHeight(450);
        setWidth(600);
    }

    const expandUsersWeekData = () => {
        setExpandedUsersWeekData(true);
        setExpandedGraph(true);
        setHeight(450);
        setWidth(600);
    }

    const expandUsersMonthData = () => {
        setExpandedUsersMonthData(true);
        setExpandedGraph(true);
        setHeight(450);
        setWidth(600);
    }

    const expandLinksBetweenMaterials = () => {
        setExpandedLinksBetweenMaterials(true);
        setExpandedGraph(true);
        setHeight(450);
        setWidth(600);
    }

    const expandMonthComparisonData = () => {
        setExpandedMonthComparisonData(true);
        setExpandedGraph(true);
        setHeight(450);
        setWidth(600);
    }

    const closeModal = () => {
        setHeight(250);
        setWidth(360);
        setExpandedGraph(false);
        setExpandedCookieEventsData(false);
        setExpandedUsersWeekData(false);
        setExpandedUsersMonthData(false);
        setExpandedLinksBetweenMaterials(false);
        setExpandedMonthComparisonData(false);
    }

    const handleChartClick = (event) => {
        event.stopPropagation();
    }

    useEffect(() => {
        fetch("http://localhost:8000/activity_statistics/").then(res => res.json()).then(data => {
            setCookieEventsData(Object.entries(data['data']['cookie_events_data']));
            setUsersWeekData(Object.entries(data['data']['users_week_data']));
            setUsersMonthData(Object.entries(data['data']['users_month_data']));
            setLinksBetweenMaterials(Object.entries(data['data']['links_between_materials']));
            setMonthComparisonData(Object.entries(data['data']['month_comparison_data']));
        }).then(() => {
            if(cookieEventsData !== []){
                setIsPending(false);
            };
        }).catch(e => console.log(e.message));
    }, [])

    return(
        <div>

            {!expandedGraph &&
            <div className = "users-week-box" onClick = {expandUsersWeekData}>
                {!isPending &&
                <div className = "example-line-graph">
                    <LineGraph data = {usersWeekData} height = {Height} width = {Width} />
                </div>
                }

                {isPending && <div className = "loader" />}

                <h5> Users in Last Week </h5>
            </div>
            }

            {expandedUsersWeekData &&
            <div onClick = {closeModal} className = "overlay">
                <div className = "modal-container">
                    <ExpandedLineGraph data = {usersWeekData} height = {Height} width = {Width} />
                    <h2 onClick = {closeModal}> + </h2>
                </div>
            </div>
            }

            {!expandedGraph &&
            <div className = "material-links-box" onClick = {expandLinksBetweenMaterials}>
                {!isPending &&
                <div className = "example-chord">
                    <ChordDiagram data = {linksBetweenMaterials} height = {225} width = {350} />
                </div>
                }

                {isPending && <div className = "loader" />}

                <h5> Links Between Materials </h5>
            </div>
            }

            {expandedLinksBetweenMaterials &&
            <div onClick = {closeModal} className = "overlay">
                <div className = "modal-container">
                    <ExpandedChordDiagram data = {linksBetweenMaterials} height = {Height} width = {Width} />
                    <h2 onClick = {closeModal}> + </h2>
                </div>
            </div>
            }

            {!expandedGraph &&
            <div className = "users-two-time-periods-box" onClick = {expandMonthComparisonData}>
                {!isPending &&
                <div className = "example-line-graph">
                    <DoubleLineGraph data = {monthComparisonData} height = {Height} width = {Width} />
                </div>
                }

                {isPending && <div className = "loader" />}

                <h5> Users Over Two Time Periods </h5>
            </div>
            }

            {expandedMonthComparisonData &&
            <div onClick = {closeModal} className = "overlay">
                <div className = "modal-container">
                    <ExpandedDoubleLineGraph data = {monthComparisonData} height = {Height} width = {Width} />
                    <h2 onClick = {closeModal}> + </h2>
                </div>
            </div>
            }

            {!expandedGraph &&
            <div className = "cookie-events-box" onClick = {expandCookieEventsData}>
                {!isPending &&
                <div className = "example-line-graph">
                    <LineGraph data = {cookieEventsData} height = {Height} width = {Width} />
                </div>
                }

                {isPending &&
                <div className = "loader" />
                }

                <h5> Events Per User </h5>
            </div>
            }

            {expandedCookieEventsData &&
            <div onClick = {closeModal} className = "overlay">
                <div className = "modal-container">
                    <ExpandedLineGraph data = {cookieEventsData} height = {Height} width = {Width} />
                    <h2 onClick = {closeModal}> + </h2>
                </div>
            </div>
            }

            {!expandedGraph &&
            <div className = "users-month-box" onClick = {expandUsersMonthData}>
                {!isPending &&
                <div className = "example-line-graph">
                    <LineGraph data = {usersMonthData} height = {Height} width = {720} />
                </div>
                }

                {isPending && <div className = "loader" />}

                <h5> User Activity In The Past Month </h5>
            </div>
            }

            {expandedUsersMonthData &&
            <div onClick = {closeModal} className = "overlay">
                <div className = "modal-container">
                    <ExpandedLineGraph data = {usersMonthData} height = {Height} width = {720} />
                    <h2 onClick = {closeModal}> + </h2>
                </div>
            </div>
            }

        </div>
    )

};

export default ActivityStatistics;