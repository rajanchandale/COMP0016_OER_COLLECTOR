import { useD3 } from './useD3';
import * as d3 from 'd3';

function LineGraph({ data, height, width }){

    const margin = { top: 30, right: 30, bottom: 30, left: 40};

    const ref = useD3(

        (svg) => {

            const innerWidth = width - margin.left - margin.right;
            const innerHeight = height - margin.top - margin.bottom;

            const x = d3
                .scalePoint()
                .domain(data.map(d => d[1]['x']))
                .range([0, innerWidth]);

            const y  = d3
                .scaleLinear()
                .domain([0, d3.max(data, d => d[1]['y'])])
                .range([innerHeight, 0]);

            const line = d3.line()
                .x(d => x(d[1]['x']))
                .y(d => y(d[1]['y']));

            const everyOtherString = (d, i) => {
                return i % 2 === 0 ? d : null;
            };

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
                .call(d3.axisBottom(x).tickFormat(everyOtherString))
                .selectAll('text')
                    .attr('fill', '#5C96A6');


            svg.append('g')
                .call(d3.axisLeft(y).tickFormat(formatTicks))
                .selectAll('text')
                    .attr('fill', '#5C96A6');

            svg.append('path')
                .datum(data)
                .attr('fill', 'none')
                .attr('stroke', '#63C1BD')
                .attr('stroke-width', 3.5)
                .attr('d', line);

        }, [data]

    );

    return(

        <svg width = {width} height = {height}>
            <g ref = {ref} transform = {`translate(${margin.left}, ${margin.right})`} />
        </svg>

    );

};

export default LineGraph;