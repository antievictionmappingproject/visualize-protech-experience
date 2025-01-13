d3.json('sunburstHierachy.json').then(function(data)
{  
    // Specify the chart’s dimensions.
    const width = 1000;
    const height = width;
    const radius = width / 6;
  
    // Create the color scale.
    const color = d3.scaleOrdinal(d3.quantize(d3.interpolateRainbow, data.children.length + 1));
  
    // Compute the layout.
    const hierarchy = d3.hierarchy(data)
        .sum(d => d.value)
        .sort((a, b) => b.value - a.value);
    const root = d3.partition()
        .size([2 * Math.PI, hierarchy.height + 1])
      (hierarchy);
    root.each(d => d.current = d);
  
    // Create the arc generator.
    const arc = d3.arc()
        .startAngle(d => d.x0)
        .endAngle(d => d.x1)
        .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
        .padRadius(radius * 1.5)
        .innerRadius(d => d.y0 * radius)
        .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1))
  
    // Create the SVG container.
    const svg = d3.create("svg")
        .attr("viewBox", [-width / 2, -height / 2, width, width])
        .style("font", "10px sans-serif");
  
    const companyNames = data.children.flatMap(tech => tech.children.map(company => company.name));
    const uniqueCompanyNames = Array.from(new Set(companyNames));
    const companyColor = d3.scaleOrdinal(d3.quantize(d3.interpolateTurbo, uniqueCompanyNames.length));
    // Piecewise color scale
    const preferenceColor = d3.scaleSequential()
                              .domain([-1, 0, 1]) // Define the range of preference scores
                              .interpolator(d3.piecewise(d3.interpolateRgb, [
                                "darkred", // Strong dislike (-1)
                                "orange",  // Slight dislike (-0.5)
                                "yellow",  // Neutral (0)
                                "lightgreen", // Slight like (0.5)
                                "darkgreen"   // Strong like (1)
                              ]));
  
    // Create a tooltip div
    const tooltip = d3.select("body").append("div")
                      .attr("class", "tooltip")
                      .style("position", "absolute")
                      .style("visibility", "hidden")
                      .style("background-color", "white")
                      .style("border", "1px solid #ccc")
                      .style("padding", "8px")
                      .style("border-radius", "4px")
                      .style("font-size", "12px")
                      .style("pointer-events", "none");
  
    // Append the arcs.
    const path = svg.append("g")
      .selectAll("path")
      .data(root.descendants().slice(1))
      .join("path")
      .attr("fill", d => {
                          if (d.data.name === "Amenities") return "#a6cee3"; // Set red for Amenities
                          if (d.data.name === "Rent") return "#ccebc5";    // Set green for Rent
                          if (d.data.name === "Units") return "#ffed6f";    // Set blue for Units
                          if (d.parent && d.parent.data.name === "Amenities") return "#a6cee3"; // Inherit from Amenity
                          if (d.parent && d.parent.data.name === "Rent") return "#ccebc5";    // Inherit from Rent
                          if (d.parent && d.parent.data.name === "Units") return "#ffed6f";    // Inherit from Unit
  
                          if (d.depth === 2) return companyColor(d.data.name); // Unique color for each company
        
                          if (d.depth === 1 && d.data.averagePreference !== undefined) {
                                  // Use the custom color scale for tech nodes
                                  return preferenceColor(d.data.averagePreference);
                                }
        
                          return "gray"; // Default color for other cases
                        })
      .attr("fill-opacity", d => arcVisible(d.current) ? (d.children ? 0.6 : 0.4) : 0)
      .attr("pointer-events", d => arcVisible(d.current) ? "auto" : "none")
      .attr("d", d => arc(d.current))
      .on("mouseover", function (event, d) {
        const ancestors = d.ancestors().map(a => a.data.name).reverse().join(" / ");
        // Find the first valid preference score from ancestors
        const inheritedPreference = d.ancestors().find(a => a.data.averagePreference !== undefined);
        const preferenceScore = inheritedPreference
          ? inheritedPreference.data.averagePreference.toFixed(2)
          : "N/A";
      
        const nodeInfo = `
          <strong>${d.data.name}</strong><br>
          Tech Preference Score: ${preferenceScore}<br>
          Count: ${d.value !== undefined ? d.value : "N/A"}<br>
          From: ${ancestors}
        `;
      
        tooltip.style("visibility", "visible")
               .html(nodeInfo);
      })
      .on("mousemove", function (event) {
        // Update tooltip position
        tooltip.style("top", (event.pageY + 10) + "px")
               .style("left", (event.pageX + 10) + "px");
      })
      .on("mouseout", function () {
        // Hide tooltip on mouseout
        tooltip.style("visibility", "hidden");
      })
      ;
  
  
    // Make them clickable if they have children.
    path.filter(d => d.children)
        .style("cursor", "pointer")
        .on("click", clicked);
  
    // const format = d3.format(",d");
    // path.append("title")
    //     .text(d => `${d.ancestors().map(d => d.data.name).reverse().join("/")}\n${format(d.value)}`);
  
    const label = svg.append("g")
        .attr("pointer-events", "none")
        .attr("text-anchor", "middle")
        .style("user-select", "none")
      .selectAll("text")
      .data(root.descendants().slice(1))
      .join("text")
        .attr("dy", "0.35em")
        .attr("fill-opacity", d => +labelVisible(d.current))
        .attr("transform", d => labelTransform(d.current))
        .text(d => d.data.name);
  
    const parent = svg.append("circle")
        .datum(root)
        .attr("r", radius)
        .attr("fill", "none")
        .attr("pointer-events", "all")
        .on("click", clicked);
  
    // Handle zoom on click.
    function clicked(event, p) {
      parent.datum(p.parent || root);
  
      root.each(d => d.target = {
        x0: Math.max(0, Math.min(1, (d.x0 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
        x1: Math.max(0, Math.min(1, (d.x1 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
        y0: Math.max(0, d.y0 - p.depth),
        y1: Math.max(0, d.y1 - p.depth)
      });
  
      const t = svg.transition().duration(750);
  
      // Transition the data on all arcs, even the ones that aren’t visible,
      // so that if this transition is interrupted, entering arcs will start
      // the next transition from the desired position.
      path.transition(t)
          .tween("data", d => {
            const i = d3.interpolate(d.current, d.target);
            return t => d.current = i(t);
          })
        .filter(function(d) {
          return +this.getAttribute("fill-opacity") || arcVisible(d.target);
        })
          .attr("fill-opacity", d => arcVisible(d.target) ? (d.children ? 0.6 : 0.4) : 0)
          .attr("pointer-events", d => arcVisible(d.target) ? "auto" : "none") 
  
          .attrTween("d", d => () => arc(d.current));
  
      label.filter(function(d) {
          return +this.getAttribute("fill-opacity") || labelVisible(d.target);
        }).transition(t)
          .attr("fill-opacity", d => +labelVisible(d.target))
          .attrTween("transform", d => () => labelTransform(d.current));
    }
    
    function arcVisible(d) {
      return d.y1 <= 3 && d.y0 >= 1 && d.x1 > d.x0;
    }
  
    function labelVisible(d) {
      return d.y1 <= 3 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03;
    }
  
    function labelTransform(d) {
      const x = (d.x0 + d.x1) / 2 * 180 / Math.PI;
      const y = (d.y0 + d.y1) / 2 * radius;
      return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180})`;
    }
  
    return svg.node();
  }