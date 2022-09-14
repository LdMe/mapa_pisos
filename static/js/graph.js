
/* var graphs = {{graphJSON | safe}};
  var layout = {
    
    yaxis: {fixedrange: true},
    xaxis : {fixedrange: true}
    };
  Plotly.plot('chart',graphs,layout);
  var barras = {{bars | safe}};
  Plotly.plot('bars',barras,layout);
 */
  // define function to plot graph
  function plotGraph(graphs,barras){
    var layout = {
    
      yaxis: {fixedrange: true},
      xaxis : {fixedrange: true}
      };
    Plotly.plot('chart',graphs,layout);
    Plotly.plot('bars',barras,layout);
    
  }