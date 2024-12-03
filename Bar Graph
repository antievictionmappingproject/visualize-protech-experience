barGraph = {
  // Extract column names for bar chart keys
  const columns = Object.keys(dataset[0]).filter(col => col !== "Technology");

  // Define chart dimensions
  const width = 800;
  const height = 400;
  const margin = { top: 30, right: 20, bottom: 100, left: 50 };

  // Scales
  const xScale = d3.scaleBand()
    .domain(columns)
    .range([margin.left, width - margin.right])
    .padding(0.3);

  const yScale = d3.scaleLinear()
    .range([height - margin.bottom, margin.top]);

  // Create SVG container
  const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .style("font-family", "sans-serif");

  // Add x-axis
  const xAxis = svg.append("g")
    .attr("transform", `translate(0, ${height - margin.bottom})`);

  // Add y-axis
  const yAxis = svg.append("g")
    .attr("transform", `translate(${margin.left}, 0)`);

  // Add bars group
  const barsGroup = svg.append("g")
    .attr("fill", "steelblue");

  // Create tooltip
  const tooltip = d3.select("body").append("div")
    .style("position", "absolute")
    .style("background-color", "white")
    .style("border", "1px solid #ccc")
    .style("border-radius", "4px")
    .style("padding", "5px")
    .style("font-size", "12px")
    .style("pointer-events", "none")
    .style("opacity", 0); // Initially hidden


  // Update function to render the chart based on selected technology
  function updateChart(technologyName) {
    // Find data for the selected technology
    const selectedData = dataset.find(d => d.Technology === technologyName);

    // Map data to keys and values
    const data = columns
  .filter(key => key !== technologyName) // Exclude selected technology
  .map(key => ({
    key,
    value: selectedData[key]
  }));


    // Sort data by value in descending order
    data.sort((a, b) => b.value - a.value);

    // Update xScale domain based on sorted keys
    xScale.domain(data.map(d => d.key));

    const maxValue = d3.max(data, d => d.value); // Only consider visible bar values
    yScale.domain([0, maxValue*1.05]);

    // Update axes
    xAxis.transition().duration(750).call(d3.axisBottom(xScale))
        .selectAll("text") // Select x-axis labels
        .attr("transform", "rotate(-45)") // Rotate the labels
        .style("text-anchor", "end"); // Align labels to the end
    
    yAxis.transition().duration(750).call(d3.axisLeft(yScale));


    // Bind data to bars
    const bars = barsGroup.selectAll("rect")
      .data(data, d => d.key);

    // Enter + Update
    bars.enter().append("rect")
        .attr("x", d => xScale(d.key))
        .attr("y", yScale(0)) // Start at the bottom
        .attr("height", 0) // No height initially
        .attr("width", xScale.bandwidth())
        .on("mouseover", function (event, d) {
          tooltip.transition().duration(200).style("opacity", 1);
          tooltip.html(`Value: ${d.value}`)
            .style("left", `${event.pageX + 10}px`)
            .style("top", `${event.pageY - 28}px`);
        })
        .on("mousemove", function (event) {
          tooltip.style("left", `${event.pageX + 10}px`)
            .style("top", `${event.pageY - 28}px`);
        })
        .on("mouseout", function () {
          tooltip.transition().duration(200).style("opacity", 0);
        })
      .merge(bars)
        .transition().duration(750) // Apply transition
        .attr("x", d => xScale(d.key))
        .attr("y", d => yScale(d.value))
        .attr("height", d => yScale(0) - yScale(d.value))
        .attr("width", xScale.bandwidth());

    // Exit
    bars.exit()
      .transition().duration(750)
      .attr("y", yScale(0))
      .attr("height", 0)
      .remove();
  }

  // Create the dropdown using Observable Inputs
  const dropdown = Inputs.select(
    dataset.map(d => d.Technology),
    { label: "Select Technology", value: dataset[0].Technology }
  );

  // Attach event listener to dropdown
  dropdown.addEventListener("input", () => {
    updateChart(dropdown.value);
  });

  // Initialize the chart with the first technology
  updateChart(dataset[0].Technology);

  // Return a container with both the dropdown and the chart
  const container = d3.create("div")
    .style("display", "flex")
    .style("flex-direction", "column")
    .node();

  // Append dropdown and SVG to the container
  container.appendChild(dropdown);
  container.appendChild(svg.node());

  return container;
}