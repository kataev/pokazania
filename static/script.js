dojo.registerModulePath("pokazania", "/static");



dojo.addOnLoad(function(){
    chart = new dojox.charting.Chart2D('chart', null);
    chart.addPlot("default",
            {
                type: "StackedAreas",
                markers: true,
                areas: true,
                tension: "S"
            });
//    chart.addPlot("elec", {type: "StackedAreas"});

    var tip = new dojox.charting.action2d.Tooltip(chart, "default");
    var magnify = new dojox.charting.action2d.Magnify(chart, "default");
    chart.setTheme(dojox.charting.themes.Claro);
    chart.addAxis("y", {vertical: true });
    selectableLegend = false;



dojo.declare('dojox.grid.DataGrid',dojox.grid.DataGrid,{
    constructor:function(){
        grid = this;
        console.log(this);
        dojo.connect(this,'onRowClick',function(event){
            console.log(event);
        });
    },
    postCreate: function(){
			this._placeholders = [];
			this._setHeaderMenuAttr(this.headerMenu);
			this._setStructureAttr(this.structure);
			this._click = [];
			this.inherited(arguments);
			if(this.domNode && this.autoWidth && this.initialWidth){
				this.domNode.style.width = this.initialWidth;
			}
			if (this.domNode && !this.editable){
				// default value for aria-readonly is false, set to true if grid is not editable
				dojo.attr(this.domNode,"aria-readonly", "true");
			}
        console.log('postCreate')
        var grid = this;

        if (grid.store.url.split('/')[2]=='energy'){

        chart.addAxis("x");
        var i=0;

        grid.store.fetch()

        var s = chart.addSeries(grid.store.url,
                    new dojox.charting.DataSeries(
                            grid.store, {query: {id: "*"}
                                    }, function(store, item) {
                                return store.getValue(item, 'elec4') < 100 ? parseInt(store.getValue(item, 'elec4')) : 0
                            }),{ stroke: "red", fill: "pink" });
        var j=0;
        var d = chart.addSeries(grid.store.url+1,
                    new dojox.charting.DataSeries(
                            grid.store, {query: {id: "*"}
                                    }, function(store, item) {
                                return store.getValue(item, 'elec16') < 100 ? parseInt(store.getValue(item, 'elec16')) : 0
                            }),{ stroke: "green", fill: "lightgreen" });
            console.log(chart, s)
            chart.render();
        }
		}
});
});