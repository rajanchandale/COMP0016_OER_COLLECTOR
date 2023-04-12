import { useD3 } from './useD3';
import * as d3 from 'd3';

function DoubleLineGraph({ data, height, width }){

    const ref = useD3(

        (svg) => {

            const processedData = data.map(([_, obj]) => obj);

            console.log("PROCESSED DATA")
            console.log(processedData);

            const margin = { top: 20, right: 30, bottom: 30, left: 40};
            const innerWidth = width - margin.left - margin.right;
            const innerHeight = height - margin.top - margin.bottom;

            const x = d3
                .scalePoint()
                .domain(processedData.map(d => d.x))
                .rangeRound([margin.left, width - margin.right]);

            const y = d3
                .scaleLinear()
                .domain([0, d3.max(processedData, (d) => d.y1)])
                .rangeRound([height-margin.bottom, margin.top]);

            const y1 = d3
                .scaleLinear()
                .domain([0, d3.max(processedData, d => d.y2)])

            const line = d3.line()
                .x(d => x(d.x))
                .y(d => y(d.y1));

            const line1 = d3.line()
                .x(d => x(d.x))
                .y(d => y(d.y2));

            const everyOtherString = (d, i) => {
                return i % 2 === 0 ? d : null;
            };

            svg.append('g')
                .attr('transform', `translate(0, ${height-margin.bottom})`)
                .call(d3.axisBottom(x).tickFormat(everyOtherString))
                .selectAll('text')
                    .attr('fill','#5C96A6');

            svg.append('g')
                .attr("transform", `translate(${margin.left} 0)`)
                .call(d3.axisLeft(y))
                .selectAll('text')
                    .attr('fill', '#5C96A6');


            svg
                .append("path")
                .datum(processedData)
                .attr("fill", "none")
                .attr("stroke", "#63C1BD")
                .attr("stroke-width", 3.5)
                .attr("d", line);

            svg.append("path")
                .datum(processedData)
                .attr("fill", "none")
                .attr("stroke", "#5C96A6")
                .attr("stroke-width", 3.5)
                .attr("d", line1);


        }, [data, height, width]

    );

    return(

        <svg
            ref = {ref}
            style = {{
                height: height,
                width: width,
                marginRight: "0px",
                marginLeft: "0px",
            }}
        >
            <g className = "x-axis" />
            <g className = "y-axis" />
            <path className = "line" />
        </svg>

    );

};

export default DoubleLineGraph;