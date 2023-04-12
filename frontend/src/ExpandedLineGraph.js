import { useD3 } from './useD3';
import * as d3 from 'd3';

function ExpandedLineGraph({ data, height, width, onChartClick }){

    const margin = { top: 20, right: 30, bottom: 50, left: 30};

    const ref = useD3(

        (svg) => {

            const innerWidth = width - margin.left - margin.right;
            const innerHeight = height - margin.top - margin.bottom;

            const x = d3
                .scalePoint()
                .domain(data.map(d => d[1]['x']))
                .range([margin.left, innerWidth])
                .padding(0.1);

            const y  = d3
                .scaleLinear()
                .domain([0, d3.max(data, d => d[1]['y'])])
                .range([innerHeight, 0]);

            const line = d3.line()
                .x(d => x(d[1]['x']))
                .y(d => y(d[1]['y']));

            const tooltip = d3
                .select('body')
                .append('div')
                .attr('class', 'tooltip')
                .style('opacity', 0);

            const formatTicks = (value) => {
                const maxValue = d3.max(data, d => d[1]['y']);
                if(maxValue >= 1e6){
                    return value / 1e6 + 'M';
                } else {
                    return value;
                }
            }

            svg.selectAll('*').remove();

            svg.append('g')
                .attr('transform', `translate(0, ${innerHeight})`)
                .call(d3.axisBottom(x))
                .append('text')
                    .attr('x', innerWidth/2 + 20)
                    .attr('y', 40)
                    .attr('fill', '#5C96A6')
                    .attr('text-anchor', 'middle')
                    .attr('font-size', '20px')
                    .attr('font-weight', 'bold')
                    .text("Date");


            svg.append('g')
                .attr("transform", `translate(${margin.left} 0)`)
                .call(d3.axisLeft(y).tickFormat(formatTicks))
                .append('text')
                    .attr('x', -innerHeight / 2)
                    .attr('y', -35)
                    .attr('fill', '#5C96A6')
                    .attr('text-anchor', 'middle')
                    .attr('transform', 'rotate(-90)')
                    .attr("font-size", "20px")
                    .attr("font-weight", "bold")
                    .text("Number of Users");

            svg.append('path')
                .datum(data)
                .attr('fill', 'none')
                .attr('stroke', '#63C1BD')
                .attr('stroke-width', 3.5)
                .attr('d', line)
                .on('click', (event, d) => {
                    if (onChartClick){
                        onChartClick(event);
                    }
                    tooltip
                        .transition()
                        .duration(500)
                        .style('opacity', 0);
                });

            svg
                .selectAll(".data-point")
                .data(data)
                .join("circle")
                .attr("class", "data-point")
                .attr("cx", d => x(d[1]['x']))
                .attr("cy", d => y(d[1]['y']))
                .attr("r", 5)
                .attr("fill", "#63C1BD")
                .on("mouseenter", (event, d) => {
                    tooltip
                        .transition()
                        .duration(200)
                        .style("opacity", 0.7);
                    tooltip
                        .html(`x: ${d[1]['x']}, y: ${d[1]['y']}`)
                        .style("left", event.pageX + "px")
                        .style("top", event.pageY + "px");
                })
                .on("mouseleave", () => {
                    tooltip
                    .transition()
                    .duration(500)
                    .style("opacity", 0);
                })
                .on("click", (event, d) => {
                    if(onChartClick){
                        onChartClick(event);
                    }
                    tooltip
                        .transition()
                        .duration(500)
                        .style("opacity", 0);
                });

        }, [data]

    );

    return(

        <svg width = {width+25} height = {height+25}>
            <g ref = {ref} transform = {`translate(${margin.left}, ${margin.right})`} />
        </svg>

    );

};

export default ExpandedLineGraph;