dd3.csv('../DataCleaning/technology_pairs_filtered.csv').then(dataset => {
  console.log("Dataset loaded:", dataset); // Confirm data is loaded

  const width = 800;
  const height = 400;
  const margin = { top: 30, right: 20, bottom: 100, left: 50 };

  // Scales
  const xScale = d3.scaleBand()
      .domain(dataset.map(d => d.Technology))
      .range([margin.left, width - margin.right])
      .padding(0.3);

  const yScale = d3.scaleLinear()
      .domain([0, d3.max(dataset, d => +d.Value1)]) // Replace `Value1` with your actual column name
      .range([height - margin.bottom, margin.top]);

  console.log("Scales created:", xScale.domain(), yScale.domain()); // Debug scales

  // Create SVG container
  const svg = d3.select("#bar-chart-container")
      .append("svg")
      .attr("width", width)
      .attr("height", height);

  console.log("SVG element:", svg.node());

  console.log("SVG created"); // Confirm SVG creation

  // Add x-axis
  svg.append("g")
      .attr("transform", `translate(0, ${height - margin.bottom})`)
      .call(d3.axisBottom(xScale))
      .selectAll("text")
      .attr("transform", "rotate(-45)")
      .style("text-anchor", "end");

  console.log("X-axis added"); // Confirm X-axis rendering

  // Add y-axis
  svg.append("g")
      .attr("transform", `translate(${margin.left}, 0)`)
      .call(d3.axisLeft(yScale));

  console.log("Y-axis added"); // Confirm Y-axis rendering

  // Add bars
  const bars = svg.selectAll("rect")
      .data(dataset)
      .enter()
      .append("rect")
      .attr("x", d => xScale(d.Technology))
      .attr("y", d => yScale(+d.Value1)) // Replace `Value1` with your actual column name
      .attr("width", xScale.bandwidth())
      .attr("height", d => yScale(0) - yScale(+d.Value1)) // Height calculation
      .attr("fill", "steelblue");

  console.log("Bars added:", bars); // Confirm bars are added
});