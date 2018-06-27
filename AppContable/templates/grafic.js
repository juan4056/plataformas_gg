$(function(){
    var dataSource = [];

    $ajax({
        url: 'http://127.0.0.1:5000/datos',
        dataType: 'json',
        succes:(function(data){
            dataSource=data
        });
    })



    $("#chartContainer").dxPieChart({
        dataSource: dataSource,
        palette: "bright",
        series:{
            argumentField: "gasto",
            valueField: "cantidad",
            innerRadius: 0.3,
            label: {
                visible: true,
                connector:{visible:true},
                customizeText: function(point){
                    return point.percentText;
                }
            }
        },
        tooltip: {
            enabled:true,
            percentPrecision: 2,
            customizeTooltip: function (arg) {
                var percentText = Globalize.formatNumber(arg.percent, {
                    style: "percent",
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });

                return {
                    text: " S/. " + arg.valueText + " - " + percentText
                };
            }
        },

    });
});