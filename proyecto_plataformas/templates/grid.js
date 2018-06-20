$(function(){
    var datasource=[{
    'id':1,
    'nombre': 'luz y agua',
    'cantidad':130
    },{
    'id':2,
    'nombre': 'transporte',
    'cantidad' : 250
    },{
    'id': 3,
    'nombre': 'Comida',
    'cantidad' : 300
    },{
    'id':4,
    'nombre':'Otros',
    'cantidad':230
    }];


    &("#gridContainer").dxDatagrid({
        dataSource: datasource,
        columns:[
            'nombre',
            'cantidad',
            {
                dataField: "Title",
                width: 150
            }
        ],
        paging: {pageSize:6},
        editing: {
            editEnabled: true,
            removeEnabled: true,
            insertEnabled: true
        }
    })
    }