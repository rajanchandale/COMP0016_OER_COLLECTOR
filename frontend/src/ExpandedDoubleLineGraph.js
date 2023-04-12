import { useD3 } from './useD3';
import * as d3 from 'd3';

function ExpandedDoubleLineGraph({ data, height, width, onChartClick }){


    console.log("DATA: ");
    console.log(data);

    const ref = useD3(

        (svg) => {

            const processedData = data.map(([_, obj]) => obj);

            console.log("PROCESSED DATA")
            console.log(processedData);

            const margin = { top: 20, right: 20, bottom: 40, left: 60 };
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


            const tooltip = d3
                .select('body')
                .append('div')
                .attr('class', 'tooltip')
                .style('opacity', 0);

            svg.append('g')
                .attr('transform', `translate(0, ${height-margin.bottom})`)
                .call(d3.axisBottom(x))
                .append('text')
                    .attr('x', innerWidth/2 + 50)
                    .attr('y', 40)
                    .attr('fill', '#5C96A6')
                    .attr('font-weight', 'bold')
                    .attr('font-size','20px')
                    .attr('text-anchor', 'middle')
                    .text("Date");

            svg.append('g')
                .attr("transform", `translate(${margin.left} 0)`)
                .call(d3.axisLeft(y))
                .append('text')
                    .attr('x', -innerHeight / 2)
                    .attr('y', -40)
                    .attr('fill', '#5C96A6')
                    .attr('font-weight', 'bold')
                    .attr('font-size', '20px')
                    .attr('text-anchor', 'middle')
                    .attr('transform', 'rotate(-90)')
                    .text("Number of Users");

            svg
                .append("path")
                .datum(processedData)
                .attr("fill", "none")
                .attr("stroke", "#63C1BD")
                .attr("stroke-width", 3.5)
                .attr("d", line)
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
                .selectAll(".data-point1")
                .data(processedData)
                .join("circle")
                .attr("class", "data-point1")
                .attr("cx", d => x(d.x))
                .attr("cy", d => y(d.y1))
                .attr("r", 5)
                .attr("fill", "#63C1BD")
                .on("mouseenter", (event, d) => {
                    tooltip
                        .transition()
                        .duration(200)
                        .style("opacity", 0.7);
                    tooltip
                        .html(`x: ${d.x}, y: ${d.y1}`)
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

            svg.append("path")
                .datum(processedData)
                .attr("fill", "none")
                .attr("stroke", "#5C96A6")
                .attr("stroke-width", 3.5)
                .attr("d", line1)

            svg
                .selectAll(".data-point2")
                .data(processedData)
                .join("circle")
                .attr("class", "data-point2")
                .attr("cx", d => x(d.x))
                .attr("cy", d => y(d.y2))
                .attr("r", 5)
                .attr("fill", "#5C96A6")
                .on("mouseenter", (event, d) => {
                    tooltip
                        .transition()
                        .duration(200)
                        .style("opacity", 0.7);
                    tooltip
                        .html(`x: ${d.x}, y: ${d.y2}`)
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
                    if (onChartClick){
                        onChartClick(event);
                    }
                    tooltip
                        .transition()
                        .duration(500)
                        .style("opacity", 0);
                });

            const legend = svg.select('.legend');
            legend.append('text').text('Value 1').attr('x', 10).attr('y', 20);
            legend.append('text').text('Value 2').attr('x', 10).attr('y', 40);

            legend
                .selectAll('rect')
                .data([, 'line2'])
                .enter()
                .append('rect')
                .attr('x', 0)
                .attr('y', (d, i) => 25 + i * 20)
                .attr('width', 10)
                .attr('height', 10)
                .attr('fill', (d) => svg.select(`.${d}`).attr('stroke'));

        }, [data, height, width]

    );

    return(

        <svg
            ref = {ref}
            style = {{
                height: height,
                width: width+30,
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

export default ExpandedDoubleLineGraph;