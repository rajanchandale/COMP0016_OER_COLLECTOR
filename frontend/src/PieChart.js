import { useD3 } from './useD3';
import * as d3 from 'd3';

function PieChart({ data, height, width }){

    const ref = useD3(

        (svg) => {

            const radius = Math.min(width, height) / 2;
            const pie = d3.pie().value(d => d[1]['value']);
            const data_ready = pie(data)

            const arc = d3.arc()
                .innerRadius(0)
                .outerRadius(radius);

            const g = svg.append("g")
                .attr("transform", `translate(${width / 2.5 - 20}, ${height / 2})`)

            const arcs = g.selectAll("arc")
                .data(data_ready)
                .enter()
                .append("g")
                .attr("class", "arc");

            arcs.append("path")
                .attr("d", arc)
                .attr("fill", d => d.data[1]['colour']);

            const legend = svg.append("g")
                .attr("class", "legend")
                .attr("transform", `translate(${width-90}, 30)`)

            legend.selectAll("rect")
                .data(data_ready)
                .enter()
                .append("rect")
                .attr("x", 0)
                .attr("y", (d, i) => i * 20)
                .attr("width", 17.5)
                .attr("height", 10)
                .attr("fill", d => d.data[1]['colour']);

            legend.selectAll("text")
                .data(data_ready)
                .enter()
                .append("text")
                .attr("x", 20)
                .attr("y", (d, i) => i * 20 + 10)
                .text(d => d.data[1]['name'])
                .attr("fill", "#5C96A6");

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
        </svg>

    )

}

export default PieChart;