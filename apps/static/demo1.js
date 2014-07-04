var d3, topojson;

(function(d3) {
  "use strict";

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
        .attr("class", function(d) { return d.year%2 ? "bar oddbar" : "bar evenbar"; })
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

})(d3);

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
// Map

(function(d3, topojson) {
  "use strict";
  var width = 1000;
  var height = 800;

  var svg = d3.select("#demo2")
    .attr("width", width)
    .attr("height", height)
//    .on("click", function() { console.log(d3.mouse(this)); })
  ;

  var svgTopGroup=svg
    .append("g")
    .attr("id","svgTopGroup")
  ;

  var projection = d3.geo.albers()
      .center([0, 53])
      .rotate([4.4, 0])
      .parallels([50, 60])
      .scale(1450 * 5)
      .translate([-200+width / 2, height / 2]);

  var path = d3.geo.path()
      .projection(projection);

  var svgCourtText;

  function zoomTo(x,y,scale) {
    d3.select("#svgTopGroup")
      .transition()
      .duration(750)
      .attr("transform", "scale("+scale+") translate("+x+","+y+")")
    ;
  }

  d3.json("/static/uk.json", function(error, uk) {
    svgTopGroup
      .append("path")
      .datum(topojson.feature(uk, uk.objects.subunits))
      .attr("class","subunit")
      .attr("d", path)
      .on("click",function(){
        if (svgCourtText) { svgCourtText.remove(); }
        zoomTo(0,0,1); })
    ;


    d3.json("/static/court-locations.json", function(error, topology) {
      d3.csv("/static/ages.csv", function(error, court_ages) {
        var svgCourtGroup;
        function averageAge(courtNumber) {
          var court;
          for (court in court_ages) {
            if (parseInt(court_ages[court].court) === courtNumber) {
              return court_ages[court].avg;
            }
          }
          return 0;
        }

        var courts = topojson.feature(topology, topology.objects.courts).features;
        courts = courts.filter(function(element) {
          return averageAge(element.properties.court_number) !== 0;
        });

        svgCourtGroup = svgTopGroup.selectAll(".court")
          .data(courts)
          .enter()
          .append("g")
          .attr("class","court")
        ;

        svgCourtGroup.append("circle")
          .attr("cx", function(d) {
            return projection(d.geometry.coordinates)[0];
          })
          .attr("cy", function(d) {
            return projection(d.geometry.coordinates)[1];
          })
          .attr("r", 7)
          .style("fill", function(d) {
            var rgb = averageAge(d.properties.court_number);
            rgb = Math.floor(23*(rgb-25));
            return "rgba("+rgb+","+rgb+","+rgb+",1)";
          })
          .on("click", function(d) {
            var mouse=d3.mouse(this);
            if (svgCourtText) { svgCourtText.remove(); }
            zoomTo((1/3-1)*mouse[0],(1/3-1)*mouse[1],3);
            svgCourtText = svgCourtGroup.insert("text")
              .attr("x",  projection(d.geometry.coordinates)[0])
              .attr("y", projection(d.geometry.coordinates)[1])
              .text(d.properties.name+": "+Math.floor(averageAge(d.properties.court_number)))
            ;
          })
        ;
      });
    });
  });
})(d3,topojson);
