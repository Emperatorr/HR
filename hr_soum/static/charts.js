colors = ["#7cb5ec", "#f7a35c", "#90ee7e", "#7798BF", "#aaeeee", "#ff0066", "#7798BF", "#aaeeee"] ;

// Fetch data and display
function fetchDataAndPrintChart (url, chartOptions, isFieldData=false) {
    $.ajax({
        url: url,
        async: true,
      })
      .done(function (data) {
          if (isFieldData){
            chartOptions.series[0].data = data ;
          } else {
            chartOptions.series = data ;
          }

          if (chartOptions.chart.type === "pie") {
           // on selectione et met a l'ecart le premier element du chart
               chartOptions.series[0].data[0].sliced = true;
               chartOptions.series[0].data[0].selected = true;
           }

          for (var i = 0; i < data.length; i++){
            if (data[i].names){
                chartOptions.xAxis.categories = data[i].names;
            }
          }
        
        var chart = new Highcharts.Chart(chartOptions);
      })
}

// Number of travel by ministry chart 1
function number_of_travels_by_ministry() {
    chartOptions = {
        colors: colors,
        chart: {
            renderTo: 'chart1',
            type: 'pie'
        },
        legend: {enabled: false},
        title: {text: 'Nombre de voyage'},
        tooltip: { pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'},
        subtitle: {text: 'Nombre total de voyage par ministere'},
        xAxis: {
            categories: ['Les voyages'],
            labels: { x: -10}
        },
        yAxis: {
            allowDecimals: false,
            title: {
                text: 'Nombre de voyage'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    filter: {
                        property: 'percentage',
                        operator: '>',
                        value: 4
                    }
                }
            }
        },
        series: []
    } //option

    var url = serverURl + "?chart=travel_by_ministry" ;
    data = fetchDataAndPrintChart(url, chartOptions);
}

// Price of travels by ministry chart 2
function price_of_travels_by_ministry() {
    chartOptions = {
        chart: {
            renderTo: 'chart2',
            type: 'column'
        },
        legend: {
            align: 'right',
            verticalAlign: 'middle',
            layout: 'vertical'
        },
        title: {text: 'Prix des voyages'},
        subtitle: {text: 'Prix cumule des voyages par ministere'},
        xAxis: { 
            categories: Highcharts.getOptions().series,
            labels: { x: -10}
        },
        yAxis: {
            allowDecimals: false,
            title: {
                text: 'Les prix'
            }
        },
        series: []
    } //option

    var url = serverURl + "?chart=price_by_ministry" ;
    data = fetchDataAndPrintChart(url, chartOptions);
}

// Categorie of travels by ministry chart 2
function categories_of_traveler_by_ministry() {
    chartOptions = {
        chart: {
            renderTo: 'chart3',
            type: 'column'
        },
        legend: {
            align: 'right',
            verticalAlign: 'middle',
            layout: 'vertical'
        },
        title: {text: 'Categories des voyageurs'},
        subtitle: {text: 'Categorie des voyageurs par ministeres'},
        xAxis: {
            categories: Highcharts.getOptions().series,
            labels: { x: -10}
        },
        yAxis: {
            allowDecimals: false,
            title: {
                text: 'Nombre des voyageurs'
            }
        },
        series: []
    } //option

    var url = serverURl + "?chart=travelers_by_categories" ;
    data = fetchDataAndPrintChart(url, chartOptions);
}

// 
function document_submission_of_travels_by_ministry() {
    chartOptions = {
        chart: {
            renderTo: 'chart4',
            type: 'column'
        },
        legend: {
            align: 'right',
            verticalAlign: 'middle',
            layout: 'vertical'
        },
        title: {text: 'Livraison des ordres de mission'},
        subtitle: {text: 'Livraison des ordres de mission'},
        xAxis: { 
            categories: Highcharts.getOptions().series,
            labels: { x: -10}
        },
        yAxis: {
            allowDecimals: false,
            title: {
                text: "Nombre d'ordre de mission"
            }
        },
        series: []
    } //option

    var url = serverURl + "?chart=document_submission" ;
    data = fetchDataAndPrintChart(url, chartOptions);
}

function documents_submission_of_travels_by_ministry() {
    chartOptions = {
        chart: {
            renderTo: 'chart5',
            type: 'column'
        },
        legend: {
            align: 'right',
            verticalAlign: 'middle',
            layout: 'vertical'
        },
        title: {text: 'Disponibilite des ordres de missions'},
        subtitle: {text: 'Disponibilite des ordres de missions'},
        xAxis: { 
            categories: Highcharts.getOptions().series,
            labels: { x: -10}
        },
        yAxis: {
            allowDecimals: false,
            title: {
                text: "Nombre d'ordre mission"
            }
        },
        series: []
    } //option

    var url = serverURl + "?chart=documents_submission_by_ministry";
    data = fetchDataAndPrintChart(url, chartOptions);
}

function approuve_of_traveler_by_ministry() {
    chartOptions = {
        chart: {
            renderTo: 'chart6',
            type: 'column'
        },
        legend: {
            align: 'right',
            verticalAlign: 'middle',
            layout: 'vertical'
        },
        title: {text: 'Status des missions'},
        subtitle: {text: 'Status des missions'},
        xAxis: {
            categories: Highcharts.getOptions().series,
            labels: { x: -10}
        },
        yAxis: {
            allowDecimals: false,
            title: {
                text: 'Nombre des missions'
            }
        },
        series: []
    } //option

    var url = serverURl + "?chart=approuve_by_ministry" ;
    data = fetchDataAndPrintChart(url, chartOptions);
}


// remove all series in the charts
function remove_series() {
    var all_span = $("tspan:contains('Series')");
    all_span.each(function() {
        $(this).parent().parent().remove();
    });
}

// then we call the function once the page is fully loaded
$(document).ready(function () {
    serverURl = "/fr/les-donnees-de-statistique";
    // chart_travels_by_ministry();
    // travels();
    number_of_travels_by_ministry();
    price_of_travels_by_ministry();
    categories_of_traveler_by_ministry();
    document_submission_of_travels_by_ministry();
    documents_submission_of_travels_by_ministry();
    approuve_of_traveler_by_ministry();
    // let's wait 0.5 seconds before cleaning the charts
    window.setTimeout(remove_series, 500);
});
