
let width = 1500;
let height = 150;
let paddingLeft = 60;
let paddingRight = 75;
let sleepSessions;
let svg;
let paddingTop = 10

// audio indicator variables
let currentAudio = null
let currentAudioTime = null
let audioStartTime = null

let patientId = null
var audioPlayer = document.getElementById("audioPlayer");
var audioIndicator

const formatTime = d3.timeFormat("%H:%M");
const formatDisplayTime = d3.timeFormat("%I:%M %p");
const parseTime = d3.timeParse("%H:%M");


function calculateTimestamp(seconds) {
  let startTime = new Date(audioStartTime);
  let currentTime = new Date(startTime.getTime() + (seconds*1000));
  return currentTime
}

function drawAudioPosition() {
  
  let audioTime = audioPlayer.currentTime;
  let realTime = calculateTimestamp(audioTime)


  audioIndicator = d3.select('#group1')
    .append('rect')
    .attr("id", "audio-indicator")
    .attr("x", (formatTime(realTime)))
    .attr("y", 0)
    .attr("height", height)
    .attr("width", 2)
    .style("fill", '#b3b3cc');
}

function updateAudioPosition() {
  let audioTime = audioPlayer.currentTime;
  let realTime = calculateTimestamp(audioTime)
  audioIndicator.attr("x", (formatTime(realTime)))
}

audioPlayer.onplay = function() {
  if (!audioIndicator) {
    drawAudioPosition()
  }
};

audioPlayer.ontimeupdate = function() {
  updateAudioPosition()
}
 
function setupCanvas() {
  // set up svg canvas
  sessionCharts = d3.selectAll(".sleep-session")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "session-svg")
    // .style("z-index", -1)
    .append("g")
    .attr("transform", `translate(${0}, ${10})`)

  setScales(sleepSessions)

  sessionCharts.data(sleepSessions)
    .join('g')
    .attr("id", function (d) {
      console.log(d)
      return "group" + d.id
    })
    .each(function(d) {
      let timeAxis = d3.axisBottom()
        .scale(timeScale)
        // .ticks(10)
        .tickFormat(x => {
          let start = new Date(d.device_start_time)
          let tick_time = new Date(start.getTime() + (x*1000))
          return formatDisplayTime(tick_time)
        })
      drawData(d3.select(this), d)
      drawAxes(d3.select(this), d, timeAxis)
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
  axios.get('data/periods/1')
    .then(function (response) {
      // handle success
      sleepSessions = response.data;
      
      self.sleepSessions = response.data
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

  min_start_time = d3.min(sleepSessions.map(
    function(d) {
      return formatTime(new Date(d.device_start_time));
    }
  ))

  max_start_time = d3.max(sleepSessions.map(
    function(d) {
      return formatTime(new Date(d.device_start_time));
    }
  ))

  max_length_minutes = d3.max(sleepSessions.map(
    function(d) {
      let device_start_time = new Date(d.device_start_time)
      let device_end_time = new Date(d.device_end_time)
      return d3.timeMinute.count(device_start_time, device_end_time)
    }
  ))

  end_time = d3.timeMinute.offset(parseTime(max_start_time), max_length_minutes)
      
  return {
    time:[parseTime(min_start_time), end_time],
  }
}

function setScales(data) {

  let extents = getExtents(data);
  let timeDomain = extents.time;

  let secondsDiff = d3.timeSecond.count(timeDomain[0], timeDomain[1])

  // scale from 0 to num seconds between time extents
  timeScale = d3.scaleLinear()
    .domain([0, secondsDiff])
    .range([paddingLeft, width - paddingRight])

  // timeAxis = d3.axisBottom()
  //   .scale(timeScale)
  //   .ticks(10)

  // daily steps scale
  positionScale = d3.scaleOrdinal()
    .domain(['Prone', 'Left', 'Supine', 'Right',])
    .range([paddingTop + 75, paddingTop + 50, paddingTop + 25, paddingTop]);

  positionAxis = d3.axisLeft()
    .scale(positionScale)
    .ticks(3);
}


function drawAxes(group, d, timeAxis) {

  let axis, label;

  axis = positionAxis;
  className = 'positionAxis';
  label = 'Position';

  // group.append("text")
  //   .text(function(d) {
  //     return d.id
  //   })
  //   .attr("transform", `translate(${0}, ${15})`)
  //   .attr("class", "participant-label")

  // group.append("text")
  //   .text(function(d) {
  //     return label
  //   })
  //   .attr("transform", `translate(${0}, ${38})`)
  //   .attr("class", "attribute-label")

  // group.append("text")
  //   .text(function(d) {
  //     return units
  //   })
  //   .attr("transform", `translate(${0}, ${53})`)
  //   .attr("class", "unit-label")


  group.append("g")
    .attr("class", "timeAxis")
    .call(timeAxis)
    .attr("transform", `translate(${0}, ${paddingTop + 90})`)

  group.append("g")
    .attr("class", className)
    .call(axis)
    .attr("transform", `translate(${paddingLeft}, ${0})`)
}

function drawData(group, d) {

  let scale, colorScale, tooltip;

  scale = positionScale;
  // tooltip = stepsTooltip;
  attrib_name = 'position';
  dataLocation = 'position_events';
  chartType = 'line'
  lineColor = '#E0E0E0';

  let data = d[dataLocation];

  drawLineChart(group, data, scale, colorScale, tooltip, attrib_name, lineColor);
  drawAudioLabels(group, d['audio_labels'], d['id'])

}

function drawAudioLabels(group, data, session_id) {

  let rects = group.selectAll("rect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", function(d, i) {
      return (timeScale(d.timestamp_seconds));
    })
    .attr("y", function(d, i) {
      return positionScale(d.position) - 5;
    })
    .attr("width", 1)
    .attr("height", function(d, i) {
      return 10;
    })
    .attr("fill", function(d, i) {
      if (d['label_1'] == 'Snoring' ||  d['label_2'] === 'Snoring') {
        return '#ee442f' 
      } else if ((d['label_1'] === 'Speech' &&  d['score_1'] > 0.8) || (d['label_1' === 'Conversation'] &&  d['score_1'] > 0.8)) {
        return '#63acbe'
      } else {
        return '#E0E0E0'
      }
    })
    .attr("opacity", function(d, i) {
      return d['label_1'] === 'Snoring' || d['label_2'] === 'Snoring' ? '1.0' : '.1'
    })

  let tooltip = d3.select("#sleep-session-" + session_id).append("div")
    .attr("id", "tooltip")
    .attr("class", "tooltip-custom")
    .style("opacity", 0)

  rects
    .on("mouseover", function(event, d) {
        let html;

        if (d.label_1 === 'Snoring' || d.label_2 === 'Snoring') {
          html = "Snoring"
        } else {
          html = d.label_1
        }

        html = html + "<br/>" + d.audio_file
        html = html + "<br/>" + d.timestamp_seconds

        tooltip
          .style("left", event.layerX + "px")
          .style("top", event.layerY + "px")
          .style("opacity", 1)
          .html(html)
    })
    .on("mouseout", function(event, d) {
      tooltip.style("opacity", 0)
    })
    .on("click", function(event, d) {
      currentAudio = d.audio_file
      currentAudioTime = d.timestamp_seconds
      audioStartTime = d.audio_start_time
      console.log('current audio time: ', currentAudioTime)
      let audioEvent = new Event('audio-start-event');
      document.dispatchEvent(audioEvent)
    })
}

function drawLineChart(group, data, scale, colorScale, tooltip, attrib_name, lineColor) {

  console.log('line chart: ', data)

  let line = d3.line()
    // .defined(d => !isNaN(d[attrib_name]))
    .x(function(d) {
      console.log('seconds:', d.seconds_elapsed)
      // console.log((d.timestamp))
      return (timeScale(d.seconds_elapsed))
    })
    .y(function(d) {
      // console.log(scale(d[attrib_name]))
      return scale(d[attrib_name]);
    }).curve(d3.curveStepAfter)

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

function startAudio() {
  let self = this;
  self.audioPath = media_url + currentAudio
  console.log('startAudio: ', currentAudioTime)
  self.$refs.audio.currentTime = currentAudioTime;
  self.$refs.audio.play();
  self.currentlyPlaying = true;
}

function playAndStop() {
  let self = this;
  if (self.currentlyPlaying) {
    self.$refs.audio.pause();
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
    audioPath: "",
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
