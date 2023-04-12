import { useRef, useEffect, useState } from 'react';

import { useD3 } from './useD3';
import * as d3 from 'd3';

function BarChart({ data, height, width }){

    const ref = useD3(

        (svg) => {

            const margin = { top: 20, right: 60, bottom: 50, left: 60};
            const innerWidth = width - margin.left - margin.right;
            const innerHeight = height - margin.top - margin.bottom;

            const x = d3
                .scaleBand()
                .domain(data.map((d) => d[1]['x']))
                .rangeRound([margin.left, width - margin.right])
                .padding(0.1)

            const y = d3
                .scaleLinear()
                .domain([0, d3.max(data, (d) => d[1]['y'])])
                .rangeRound([height - margin.bottom, margin.top]);

            svg
                .append("g")
                .attr("transform", `translate(0, ${height - margin.bottom})`)
                .call(d3.axisBottom(x))
                .selectAll("text")
                .attr("fill", "#5C96A6");

            svg
                .append("g")
                .attr("transform", `translate(${margin.left}, 0)`)
                .call(d3.axisLeft(y))
                .selectAll("text")
                .attr("fill", "#5C96A6");

            svg
                .select(".plot-area")
                .attr("fill", "#63C1BD")
                .selectAll(".bar")
                .data(data)
                .join("rect")
                .attr("class", "bar")
                .attr("x", (d) => x(d[1]['x']))
                .attr("width", x.bandwidth())
                .attr("y", (d) => y(d[1]['y']))
                .attr("height", (d) => y(0) - y(d[1]['y']))

        },
        [data.length]
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
            <g className = "plot-area" />
            <g className = "x-axis" />
            <g className = "y-axis" />

        </svg>

    );

};

export default BarChart;