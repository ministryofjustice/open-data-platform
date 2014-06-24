var d3;

function type(d) {
  d.count = +d.count; // coerce to number
  return d;
}

var margin = {top: 20, right: 30, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.time.scale()
  .domain([new Date('2002-01-01'), new Date('2013-01-01')])
  .range([0, width]);

//var x = d3.scale.ordinal()
//    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .ticks(d3.time.years, 1)
    .tickFormat(d3.time.format('%Y'));

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var chart = d3.select("#demo1")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv("/static/proceedings-by-month.csv", type, function(error, data) {
  var yearly_averages = [], month, monthIndex, yearIndex, lineFunction;
  y.domain([0, d3.max(data, function(d) { return d.count; })]);

  chart.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  chart.append("g")
      .attr("class", "y axis")
      .call(yAxis);

  chart.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", function(d,i) { return d.year%2 ? "bar oddbar" : "bar evenbar"; })
      .attr("x", function(d) { return x(new Date(d.year,d.month,1)) - 7; })
      .attr("y", function(d) { return y(d.count); })
      .attr("height", function(d) { return height - y(d.count); })
      .attr("width", 8);

  for (month=0; month<data.length; month++) {
    monthIndex = month%12;
    yearIndex = Math.floor(month/12);
    if (monthIndex === 0) {
      yearly_averages[yearIndex] = {average: 0, year: 2002+yearIndex};
    }
    yearly_averages[yearIndex].average += data[month].count/12;
  }


  lineFunction = d3.svg.line()
    .x(function(d) { return x(new Date(d.year,7,1)); })
    .y(function(d) { return y(d.average); })
    .interpolate("linear");

  chart
    .append("path")
    .attr("class","line")
    .attr("d", lineFunction(yearly_averages));
});
