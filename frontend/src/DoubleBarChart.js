import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';

const DoubleBarChart = ({ data, height, width }) => {
  const ref = useRef();

  useEffect(() => {
    const margin = { top: 20, right: 30, bottom: 50, left: 30 };
    const chartHeight = height - margin.top - margin.bottom;
    const chartWidth = width - margin.left - margin.right;

    const svg = d3.select(ref.current)
      .attr("width", width)
      .attr("height", height);

    const maxValue = d3.max(data, d => Math.max(d[1]['value1'], d[1]['value2']));

    const x = d3.scaleLinear()
      .domain([0, maxValue])
      .range([0, chartWidth / 2]);

    const y = d3.scaleBand()
      .domain(data.map(d => d[1]['name']))
      .range([0, chartHeight])
      .padding(0.1);

    svg.append("g")
      .attr("transform", `translate(${margin.left + chartWidth / 2},${margin.top})`)
      .selectAll("rect.value1")
      .data(data)
      .join("rect")
        .attr("class", "value1")
        .attr("y", d => y(d[1]['name']))
        .attr("height", y.bandwidth())
        .attr("x", 0)
        .attr("width", d => x(d[1]['value1']))
        .attr("fill", "#63C1BD");

    svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`)
      .selectAll("rect.value2")
      .data(data)
      .join("rect")
        .attr("class", "value2")
        .attr("y", d => y(d[1]['name']))
        .attr("height", y.bandwidth())
        .attr("x", d => chartWidth / 2 - x(d[1]['value2']))
        .attr("width", d => x(d[1]['value2']))
        .attr("fill", "#304C89");

    svg.append("g")
      .attr("transform", `translate(${margin.left + chartWidth / 2},${margin.top})`)
      .call(d3.axisLeft(y))
      .selectAll("text")
      .attr("fill", "#5C96A6")

    const xAxisRight = d3.axisBottom(x.copy().range([0, chartWidth / 2])).ticks(5).tickSize(0).tickPadding(6);
    const xAxisLeft = d3.axisBottom(x.copy().range([chartWidth / 2, 0])).ticks(5).tickSize(0).tickPadding(6);

    svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top + chartHeight + 10})`)
      .call(xAxisLeft)
      .call(g => g.select(".domain").attr("stroke", "currentColor").attr("stroke-opacity", 0.5))
      .selectAll("text")
      .attr("fill", "#5C96A6");

    svg.append("g")
      .attr("transform", `translate(${margin.left + chartWidth / 2},${margin.top + chartHeight + 10})`)
      .call(xAxisRight)
      .call(g => g.select(".domain").attr("stroke", "currentColor").attr("stroke-opacity", 0.5))
      .selectAll("text")
      .attr("fill", "#5C96A6");

  }, [data, height, width]);

  return (
    <svg ref={ref}>
    </svg>
  );
};

export default DoubleBarChart;
