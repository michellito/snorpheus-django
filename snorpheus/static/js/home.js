// ------------- State Functions ----------------- //

function toggleSidebar() {
  let self = this;
  self.sidebarOpen = !self.sidebarOpen;
}

function getPatientPeriods(clientId) {
  let self = this;
  axios.get('data/patients/' + clientId)
    .then(function (response) {
      // handle success
      console.log(response)
      self.patientPeriods = response.data;

    })
    .catch(function (error) {
      // handle error
      console.log(error);
    })
}

function watchPatientId(value) {
  let self = this;
  if (!value.length) {
    self.patientPeriods = [];
  }
}

function state() {

  return {
    // vars
    sidebarOpen: true,
    patientId: "",
    patientPeriods: [],
    positionEvents: [],
    // functions
    watchPatientId,
    toggleSidebar,
    getPatientPeriods,
  }
}

// ------------- State Functions ----------------- //

let width = 1100;
let height = window.innerWidth;
let paddingLeft = 120;
let paddingRight = 75;

// set up svg canvas
let svg = d3.select("#main")
  .append("svg")
  .attr("width", width)
  .attr("height", height)

let timelineGroup = d3.select("#main").select("svg")
  .append("g")
  .attr("id", "timeline")
  .attr("transform", `translate (${0}, ${20})`);

timelineGroup.append("rect")
  .attr("x", paddingLeft)
  .attr("y", 0)
  .attr("height", 30)
  .attr("width", width - paddingLeft - paddingRight)
  .style("stroke", d3.rgb(169,169,169))
  .style("stroke-width", "2")
  .style("fill", d3.rgb(211,211,211))
