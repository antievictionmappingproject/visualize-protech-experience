pieChartWithLegend = {
  const width = 400;
  const height = 400;
  const radius = Math.min(width, height) / 2;

  // Define the color scale
  const color = d3.scaleOrdinal()
    .domain(["Installed after the Pandemic", "Installed before the Pandemic"])
    .range(["steelblue", "orange"]);

  // Create the SVG container
  const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height + 50) // Extra space for the legend
    .style("font-family", "sans-serif");

  // Create a group to hold the pie chart
  const chartGroup = svg.append("g")
    .attr("transform", `translate(${width / 2}, ${height / 2})`);

  // Pie generator
  const pie = d3.pie().value(d => d.value);

  // Arc generator
  const arc = d3.arc()
    .innerRadius(0)
    .outerRadius(radius);

  // Tooltip
  const tooltip = d3.select("body").append("div")
    .style("position", "absolute")
    .style("background-color", "white")
    .style("border", "1px solid #ccc")
    .style("border-radius", "4px")
    .style("padding", "5px")
    .style("font-size", "15px")
    .style("pointer-events", "none")
    .style("opacity", 0);

  // Update function
  function updateChart(technologyName) {
    // Find data for the selected technology
    const selectedData = pie_data.find(d => d.Technology === technologyName);
    if (!selectedData) {
      console.error("No data found for technology:", technologyName);
      return;
    }

    // Prepare data for the pie chart with labels
    const data = [
      { label: "Installed after the Pandemic", value: selectedData["0s"] },
      { label: "Installed before the Pandemic", value: selectedData["1s"] }
    ];

    if (data.every(d => d.value === 0)) {
      console.warn("No data values to display for this technology:", technologyName);
      chartGroup.selectAll("path").remove();
      return;
    }

    // Bind data to pie slices
    const slices = chartGroup.selectAll("path").data(pie(data));

    // Enter + Update
    slices.enter()
      .append("path")
      .merge(slices)
      .attr("d", arc)
      .attr("fill", d => color(d.data.label))
      .on("mouseover", function (event, d) {
        tooltip.transition().duration(200).style("opacity", 1);
        tooltip.html(`${d.data.label}: ${((d.data.value / d3.sum(data, d => d.value)) * 100).toFixed(1)}%`)
          .style("left", `${event.pageX + 10}px`)
          .style("top", `${event.pageY - 28}px`);
      })
      .on("mousemove", function (event) {
        tooltip.style("left", `${event.pageX + 10}px`)
          .style("top", `${event.pageY - 28}px`);
      })
      .on("mouseout", function () {
        tooltip.transition().duration(200).style("opacity", 0);
      });

    // Exit
    slices.exit().remove();
  }

  // Dropdown
  const dropdown = Inputs.select(
    pie_data.map(d => d.Technology),
    { label: "Select Technology", value: pie_data[0].Technology, style: "font-size: 15px;" }
  );

  dropdown.addEventListener("input", () => {
    updateChart(dropdown.value);
  });

  // Initialize chart
  updateChart(pie_data[0].Technology);

  // Add a legend
  const legend = svg.append("g")
    .attr("transform", `translate(${width / 2 - 80}, ${height + 10})`); // Position below the chart

  const legendData = [
    { label: "Installed after the Pandemic", color: "steelblue" },
    { label: "Installed before the Pandemic", color: "orange" }
  ];

  legend.selectAll("rect")
    .data(legendData)
    .enter()
    .append("rect")
    .attr("x", 0)
    .attr("y", (d, i) => i * 20)
    .attr("width", 15)
    .attr("height", 15)
    .attr("fill", d => d.color);

  legend.selectAll("text")
    .data(legendData)
    .enter()
    .append("text")
    .attr("x", 20)
    .attr("y", (d, i) => i * 20 + 12)
    .text(d => d.label)
    .style("font-size", "15px")
    .style("alignment-baseline", "middle");

  // Container for dropdown and chart
  const container = d3.create("div")
    .style("display", "flex")
    .style("flex-direction", "column");

  container.append(() => dropdown);
  container.append(() => svg.node());

  return container.node();
}