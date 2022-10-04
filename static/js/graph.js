
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
  function plotGraph(graphs=null,barras=null){
    var layout = {
    
      yaxis: {fixedrange: true},
      xaxis : {fixedrange: true}
      };
    if(graphs != null){
      Plotly.purge('chart');
      Plotly.plot('chart',graphs,layout);
    }
    if(barras != null){
      Plotly.purge('bars');
      Plotly.plot('bars',barras,layout);
    }
    
  }