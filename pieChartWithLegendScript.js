import {Runtime, Inspector} from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@5/dist/runtime.js";

import define from "https://api.observablehq.com/@anti-eviction-mapping-project/visualizing-protech-experience.js?v=4";

new Runtime().module(define, name => {
  if (name === "pieChartWithLegend") return new Inspector(document.querySelector("#observablehq-pieChartWithLegend-ce81ef20"));
});