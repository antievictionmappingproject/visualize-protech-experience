// Import Observable Runtime and Inspector
import { Runtime, Inspector } from "https://cdn.jsdelivr.net/npm/@observablehq/runtime@5/dist/runtime.js";

// Import the visualization definition from Observable
import define from "https://api.observablehq.com/@anti-eviction-mapping-project/visualizing-protech-experience.js?v=4";

// Embed the visualization in the div with ID "observablehq-sunBurst-7f21e497"
new Runtime().module(define, (name) => {
    if (name === "sunBurst") {
        return new Inspector(document.querySelector("#observablehq-sunBurst-7f21e497"));
    }
});