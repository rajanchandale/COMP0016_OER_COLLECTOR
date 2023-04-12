import { useRef, useEffect, useState } from 'react';

import { useD3 } from './useD3';
import * as d3 from 'd3';

function ExpandedBarChart({ data, height, width, xLabel, yLabel, onChartClick }){

    console.log(xLabel);
    console.log(yLabel);

    const ref = useD3(

        (svg) => {

            const margin = { top: 20, right: 80, bottom: 50, left: 80};
            const innerWidth = width - margin.left - margin.right;
            const innerHeight = height - margin.top - margin.bottom;

            const x = d3
                .scaleBand()
                .domain(data.map((d) => d[1]['x']))
                .rangeRound([margin.left, width-margin.right])
                .padding(0.1);

            const y = d3
                .scaleLinear()
                .domain([0, d3.max(data, (d) => d[1]['y'])])
                .rangeRound([height - margin.bottom, margin.top]);

            svg
                .append("g")
                .attr("transform", `translate(0, ${height - margin.bottom})`)
                .call(d3.axisBottom(x))
                .append('text')
                    .attr('x', innerWidth / 2 + 75)
                    .attr('y', 40)
                    .attr('fill', '#5C96A6')
                    .attr('text-anchor', 'middle')
                    .text(xLabel)
                    .attr("font-size", "14px")
                    .attr("font-weight", "bold");

            svg
                .append("g")
                .attr("transform", `translate(${margin.left}, 0)`)
                .call(d3.axisLeft(y))
                .append('text')
                    .attr('x', -innerHeight / 2 - 30)
                    .attr('y', -60)
                    .attr('fill', '#5C96A6')
                    .attr('text-anchor', 'middle')
                    .attr('transform', 'rotate(-90)')
                    .text(yLabel)
                    .attr("font-size", "14px")
                    .attr("font-weight", "bold");

            const tooltip = d3
                .select('body')
                .append('div')
                .attr('class', 'tooltip')
                .style('opacity', 0);

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
                .on('mouseover', (event, d) => {
                    tooltip
                        .transition()
                        .duration(200)
                        .style('opacity', 1);
                    tooltip
                        .html(d[1]['y'])
                        .style('left', event.pageX + 'px')
                        .style('top', event.pageY + 'px');
                })
                .on('mouseout', () => {
                    tooltip
                        .transition()
                        .duration(500)
                        .style('opacity', 0);
                })
                .on('click', (event, d) => {
                    if (onChartClick){
                        onChartClick(event);
                    }
                    tooltip
                        .transition()
                        .duration(500)
                        .style('opacity', 0);
                });


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

export default ExpandedBarChart;