import { useD3 } from './useD3';
import * as d3 from 'd3';

function ExpandedChordDiagram({ data, height, width }){

    console.log("INSIDE CHORD");
    console.log(data);
    console.log(data.map(d => d[1]['source']));

    const viewBoxWidth = Math.max(width, height);
    const viewBoxHeight = Math.max(width, height);

    const ref = useD3(

        (svg) => {

            const processedData = data.map(d => d[1]);
            console.log("PROCESSED DATA");
            console.log(processedData);

            const inner_radius = Math.min(width, height) * 0.55;
            const outer_radius = Math.min(width, height) * 0.57;

            const nodes = Array.from(
                new Set(processedData.map(d => d.source).concat(processedData.map(d => d.target)))
            );

            console.log("1")

            const nodeIndices = new Map(nodes.map((node, index) => [node, index]));

            const matrix = Array.from({ length: nodes.length }, () =>
                new Array(nodes.length).fill(0)
            );

            processedData.forEach((d) => {
                matrix[nodeIndices.get(d.source)][nodeIndices.get(d.target)] = d.value;
                matrix[nodeIndices.get(d.target)][nodeIndices.get(d.source)] = d.value;
            });


            const chord = d3.chord().padAngle(12/ inner_radius).sortSubgroups(d3.descending);
            const chords = chord(matrix);

            const arc = d3.arc().innerRadius(inner_radius).outerRadius(outer_radius);

            const ribbon = d3.ribbonArrow().radius(inner_radius - 0.5).padAngle(1/inner_radius);

            const chartColours = [
                "#6B2B00",
                "#EF5713",
                "#3CE8EE",
                "#F1ED12",
                "#EF5713",
                "#D69718",
                "#8DF456",
                "#086402",
                "#33AA7A",
                "#3189DC",
                "#3CE8EE",
                "#003785",
                "#FF1B1B",
                "#F3228A",
                "#FF79C2",
                "#E0B5FF",
                "#9123F3",
                "#3E0087",
                "#BFBFBF",
                "#5F5F5F",
                "#000000"
            ]




            const colour = d3.scaleOrdinal(chartColours);

            const group = svg
                .append('g')
                .attr('transform', `translate(${width / 2 - 150 }, ${height / 2 + 70})`)
                .selectAll('g')
                .data(chords.groups)
                .enter()
                .append('g');

            const ribbonTooltip = d3
                .select('body')
                .append('div')
                .attr('class', 'tooltip')
                .style('opacity', 0);

            const arcTooltip = d3
                .select('body')
                .append('div')
                .attr('class', 'tooltip')
                .style('opacity', 0);

            group
                .append('path')
                .attr('d', arc)
                .attr('fill', (d) => colour(d.index))
                .attr('stroke', (d) => colour(d.index))
                .on('mouseover', (event, d) => {
                    const node = nodes[d.index];
                    const totalIncoming = processedData.reduce(
                      (sum, link) =>
                        nodes[nodeIndices.get(link.target)] === node ? sum + link.value : sum,
                      0
                    );
                    const totalOutgoing = processedData.reduce(
                      (sum, link) =>
                        nodes[nodeIndices.get(link.source)] === node ? sum + link.value : sum,
                      0
                    );

                    arcTooltip
                        .html(
                            `Total Incoming: ${totalIncoming}<br />Total Outgoing: ${totalOutgoing}`
                        )
                        .style('left', event.pageX + 'px')
                        .style('top', event.pageY + 'px')
                        .style('opacity', 0.7);
                })
                .on('mouseout', () => {
                    arcTooltip.style('opacity', 0);
                });

            svg
                .append('g')
                .attr('transform', `translate(${width / 2 - 150}, ${height / 2 + 70})`)
                .selectAll('path')
                .data(chords)
                .enter()
                .append('path')
                .attr('d', ribbon)
                .attr('fill', (d) => {
                    const fillColour = d3.color(colour(d.source.index));
                    fillColour.opacity = 0.4;
                    return fillColour;
                })
                .attr('stroke', (d) => d3.rgb(colour(d.source.index)).darker())
                .on('mouseover', (event, d) => {
                    ribbonTooltip
                        .html(
                            `Source: ${nodes[d.source.index]}<br /> Target: ${nodes[d.target.index]}<br /> Value: ${d.source.value}`
                        )
                        .style('left', event.pageX + 'px')
                        .style('top', event.pageY - 28 + 'px')
                        .style('opacity', 0.7);
                })
                .on('mouseout', () => {
                    ribbonTooltip.style('opacity', 0);
                });

            const legend = svg
                .append('g')
                .attr('class', 'legend')
                .attr('transform', `translate(${width-150}, ${80})`)
                .selectAll('g')
                .data(nodes)
                .enter()
                .append('g')
                .attr('transform', (d, i) => `translate(0, ${i*25})`);

            legend
                .append('rect')
                .attr('width', 17.5)
                .attr('height', 10)
                .attr('fill', (d, i) => colour(i));

            legend
                .append('text')
                .attr('x', 25)
                .attr('y', 7.5)
                .text((d) => d)
                .attr('font-size', '14px')
                .attr('alignment-baseline', 'middle')
                .attr();

        }, [data, height, width]

    );

    return(

        <svg ref = {ref} height = {height} width = {width+200} viewBox = {`0 0 ${viewBoxWidth+200} ${viewBoxHeight}`} />

    );

};

export default ExpandedChordDiagram;