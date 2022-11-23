
let width = 1500;
let height = 130;
let paddingLeft = 120;
let paddingRight = 75;
let sleepSessions;
let svg;
let currentAudio = null

console.log(media_url)


function setupCanvas() {
  // set up svg canvas
  svg = d3.select(".sleep-session")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "session-svg")
    .append("g")
    .attr("transform", `translate(${0}, ${10})`)


  setScales(sleepSessions)

  svg.data(sleepSessions).join('g')
    .each(function(d) {
      drawData(d3.select(this), d)
      drawAxes(d3.select(this), d)
    })
}

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
      self.patientPeriods = response.data.collection_periods;
      self.patientName = response.data.patient_name;

    })
    .catch(function (error) {
      // handle error
      console.log(error);
    })
}

function getSessionPosition(sessionId) {
  let self = this;
  axios.get('data/sessions/' + sessionId + '/position')
    .then(function (response) {
      // handle success
      sleepSessions = [response.data];
      self.sleepSessions = [response.data]
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

function getExtents(sleepSessions) {

  function getExtent(extents) {
    let min = extents[0][0]
    let max = extents[0][1]

    extents.forEach(extent => {
      if (extent[0] < min) {
        min = extent[0];
      }

      if (extent[1] > max) {
        max = extent[1]
      }
    });

    return [min, max];
  }

  let timeExtents = [];

  console.log(sleepSessions)

  sleepSessions.forEach( session => {
    console.log(session)
    timeExtents.push(
      d3.extent(session.position_data.map(
        function(d) {
          return new Date(d.timestamp);
        }
      ))
    )
  })

  timeRange = getExtent(timeExtents);

  return {
    time: timeRange,
  }
}

function setScales(data) {

  let extents = getExtents(data);
  let timeDomain = extents.time;

  // time scales
  timeScale = d3.scaleTime()
    .domain(timeDomain)
    .range([paddingLeft, width - paddingRight])

  timeAxis = d3.axisBottom()
    .scale(timeScale);

  // daily steps scale
  positionScale = d3.scaleOrdinal()
    .domain(['Left', 'Supine', 'Right', 'Other', 'Missing'])
    .range([100, 75, 50, 25, 0]);

  positionAxis = d3.axisLeft()
    .scale(positionScale)
    .ticks(3);

  positionColorScale = d3.scaleOrdinal(
    d3.interpolatePurples)
    .domain(['Left', 'Supine', 'Right', 'Other', 'Missing'])
}


function drawAxes(group, d) {

  let axis, label;

  axis = positionAxis;
  className = 'positionAxis';
  label = 'Position';

  group.append("text")
    .text(function(d) {
      return d.id
    })
    .attr("transform", `translate(${0}, ${15})`)
    .attr("class", "participant-label")

  group.append("text")
    .text(function(d) {
      return label
    })
    .attr("transform", `translate(${0}, ${38})`)
    .attr("class", "attribute-label")

  // group.append("text")
  //   .text(function(d) {
  //     return units
  //   })
  //   .attr("transform", `translate(${0}, ${53})`)
  //   .attr("class", "unit-label")


  group.append("g")
    .attr("class", "timeAxis")
    .call(timeAxis)
    .attr("transform", `translate(${0}, ${50})`)

  group.append("g")
    .attr("class", className)
    .call(axis)
    .attr("transform", `translate(${paddingLeft}, ${0})`)
}

function drawData(group, d) {

  let scale, colorScale, tooltip;

  scale = positionScale;
  colorScale = positionColorScale;
  // tooltip = stepsTooltip;
  attrib_name = 'position';
  dataLocation = 'position_data';
  chartType = 'line'
  lineColor = 'darkslateblue';

  let data = d[dataLocation];

  drawLineChart(group, data, scale, colorScale, tooltip, attrib_name, lineColor);
  drawAudioLabels(group, d['audio_labels'])

}

function drawAudioLabels(group, data) {
  let rects = group.selectAll("rect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", function(d, i) {
      // console.log(timeScale(new Date(d.timestamp)))
      return timeScale(new Date(d.timestamp));
    })
    .attr("y", function(d, i) {
      return 15;
    })
    .attr("width", 2)
    .attr("height", function(d, i) {
      return 10;
    })
    .attr("fill", function(d, i) {
      return d['label_1'] === 'Snoring' || d['label_2'] === 'Snoring' ? 'red' : 'blue'
    });

  // call tooltip only if data exists for participant (other throws error)
  // if (data.length) {
  //   rects.call(tooltip)
  //   .on('mouseover', function(event,d) {
  //     tooltip.show(event, d)
  //   })
  //   .on('mouseout', tooltip.hide)
  // }
}

function drawLineChart(group, data, scale, colorScale, tooltip, attrib_name, lineColor) {

  // console.log('line chart: ', data)

  let line = d3.line()
    // .defined(d => !isNaN(d[attrib_name]))
    .x(function(d) {
      // console.log(d.timestamp)
      // console.log(timeScale(d.timestamp))
      return timeScale(new Date(d.timestamp))
    })
    .y(function(d) {
      // console.log(scale(d[attrib_name]))
      return scale(d[attrib_name]);
    }).curve(d3.curveStepBefore)

  // group.append("path")
  //   .datum(data.filter(line.defined()))
  //   .attr("class", "missingPath")
  //   .attr("stroke", "#ccc")
  //   .attr("fill", "none")
  //   .attr("d", line);

  group.append("path")
    .datum(data)
    .attr("class", "dataPath")
    .attr("fill", "none")
    .attr("stroke", lineColor)
    .attr("stroke-width", 2)
    .attr("d", line);
}

  function playAndStop() {
    let self = this;
    if (self.currentlyPlaying) {
      self.$refs.audio.pause();
      self.$refs.audio.currentTime = 0;
      self.currentlyPlaying = false;
    } else {
      self.$refs.audio.play();
      self.currentlyPlaying = true;
    }
  }

function state() {
  return {
    // vars
    sidebarOpen: true,
    currentlyPlaying: false,
    patientId: "",
    patientName: "",
    patientPeriods: [],
    sleepSessions: [],
    // functions
    watchPatientId,
    toggleSidebar,
    getPatientPeriods,
    getSessionPosition,
    playAndStop,
    setupCanvas
  }
}

// ------------- State Functions ----------------- //
