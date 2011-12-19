/*
 * User: bteam
 * Date: 16.12.11
 * Time: 10:39
 */
var Model = Backbone.Model.extend({
    initialize:function(){
        this.set({date:Highcharts.dateFormat('%Y-%m-%d',this.get('udate')*1+1000*60*60*6)});
    }
});

var Energy = Backbone.Collection.extend({
    model:Model,
    url:'api/energys'
});

var energy = new Energy;
energy.reset(energy_preload);

var EnergyView = Backbone.View.extend({
    tagName:'table',
    className:'energy',
    template:_.template($('#energy_template').html()),
    render:function(){
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }
});


var Router = Backbone.Router.extend({
    routes:{ '':'root' },
    root:function () {
        $('#tables').css({width:energy.length*80+'px'})
        energy.each(function(m){
            console.log('each')
            var view = new EnergyView({model:m});
            $('#tables').append(view.render().el);
        });
    }
});


$(function(){
    new Router;
    Backbone.history.start();
})