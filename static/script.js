dojo.registerModulePath("pokazania", "/static");

dojo.addOnLoad(function() {
    chart = new dojox.charting.Chart2D('chart');
    chart.addPlot("elec",
        {
            type: "StackedAreas"
            ,markers: true
            ,areas: false
            ,tension: "S"
            ,fill:false
            ,vAxis: "y"
        });
    chart.addPlot("water", {type: "StackedAreas",
        markers: true
        ,areas: false
        ,tension: "S"
        ,fill:false
        ,vAxis: "y"
    });
    chart.addPlot("gaz", {type: "Lines",
        markers: true
        ,tension: "S"
        ,vAxis: "other y"
    });
    chart.addAxis("other y", {leftBottom: false,vertical:true,title:'Газ',titleFont: "normal normal normal 12pt Arial"});
    var tip = new dojox.charting.action2d.Tooltip(chart, "elec");
    var magnify = new dojox.charting.action2d.Magnify(chart, "elec");

    var tip = new dojox.charting.action2d.Tooltip(chart, "water");
    var magnify = new dojox.charting.action2d.Magnify(chart, "water");

    var tip = new dojox.charting.action2d.Tooltip(chart, "gaz");
    var magnify = new dojox.charting.action2d.Magnify(chart, "gaz");

    chart.setTheme(dojox.charting.themes.Claro);
    chart.addAxis("y", {vertical: true});
    var selectableLegend = false;

    dijit.byId('slider').onChange = function(value) {
        chart.setWindow(2, 1, value * 0.01 * chart.plotArea.width, value * 0.01 * chart.plotArea.width + chart.plotArea.width/10).render();
    }

    dojo.declare('dojox.grid.DataGrid', dojox.grid.DataGrid, {
        constructor:function() {
            grid = this;
            dojo.connect(this, 'onRowClick', function(event) {
                console.log(event);
            });
        },
        chartRender:function() {
            var grid = this;
            var j = 0;
            var a = new dojox.charting.DataSeries(
                grid.store, {query: {count:25}
                }, function(store, item) {
                    return {text:store.getValue(item, 'date'),
                        value:j++}
                })
            dojo.connect(a, "_onFetchComplete", function(asda) {
                chart.addAxis("x", {labels:a.data});
//                console.log('render',asda)
                chart.render();
            });
            chart.addSeries(grid.store.url,
                new dojox.charting.DataSeries(
                    grid.store, {query: {count:25}
                    }, function(store, item) {
                        return store.getValue(item, 'elec4') < 100 ? parseInt(store.getValue(item, 'elec4')) : 0
                    }), {plot:'elec',color:'yellow' });
            chart.addSeries(grid.store.url + 1,
                new dojox.charting.DataSeries(
                    grid.store, {query: {count:25}
                    }, function(store, item) {
                        return store.getValue(item, 'elec16') < 100 ? parseInt(store.getValue(item, 'elec16')) : 0
                    }), {plot:'elec',color:'orange' });
            chart.addSeries(grid.store.url + 2,
                new dojox.charting.DataSeries(
                    grid.store, {query: {count:25}
                    }, function(store, item) {
                        return store.getValue(item, 'iwater') < 100 ? parseInt(store.getValue(item, 'iwater')) : 0
                    }), {plot:'water',color:'#67CDDC' });
            chart.addSeries(grid.store.url + 3,
                new dojox.charting.DataSeries(
                    grid.store, {query: {count:25}
                    }, function(store, item) {
                        return store.getValue(item, 'uwater') < 100 ? parseInt(store.getValue(item, 'uwater')) : 0
                    }), { plot:'water',color:'#00A9E0' });
            chart.addSeries(grid.store.url + 'gaz',
                new dojox.charting.DataSeries(
                    grid.store, {query: {count:25}
                    }, function(store, item) {
                        return store.getValue(item, 'gaz') < 9000 ? parseInt(store.getValue(item, 'gaz')) : 0
                    }), { plot:'gaz',color:'#98C73D' });
            chart.render();
        },
        postCreate: function() {
            this._placeholders = [];
            this._setHeaderMenuAttr(this.headerMenu);
            this._setStructureAttr(this.structure);
            this._click = [];
            this.inherited(arguments);
            if (this.domNode && this.autoWidth && this.initialWidth) {
                this.domNode.style.width = this.initialWidth;
            }
            if (this.domNode && !this.editable) {
                // default value for aria-readonly is false, set to true if grid is not editable
                dojo.attr(this.domNode, "aria-readonly", "true");
            }
//        console.log('postCreate')
            var grid = this;

            if (grid.store.url.split('/')[2] == 'energy') {
                this.chartRender();
            }
        }
    });

    chart.setWindow(2, 1, 143, 343).render();
});