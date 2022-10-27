/* Project specific Javascript goes here. */

import * as d3 from "https://cdn.skypack.dev/d3@7"

const div = d3.selectAll("div")

d3
  .select(".target")  // select the elements that have the class 'target'
  .style("stroke-width", 8) // change their style: stroke width is not equal to 8 pixels
