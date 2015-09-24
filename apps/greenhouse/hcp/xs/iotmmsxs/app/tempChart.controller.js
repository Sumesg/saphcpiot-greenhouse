sap.ui.controller("app.tempChart", {
    /**
    * Called when a controller is instantiated and its View controls (if available) are already created.
    * Can be used to modify the View before it is displayed, to bind event handlers and do other one-time initialization.
    * @memberOf @memberOf app.tempChart
    */
    onInit: function(oEvent) {
        var oModel = new sap.ui.model.json.JSONModel();
        oModel.loadData("services/measurements.xsjs", null, false);
        oModel.setSizeLimit(10000);
        this.getView().setModel(oModel);

        var data = oModel.getData();

        /************************************************/
        var grid = this.getView().byId("GeneralInfoTemperature");
        grid.setModel(this._getGridModel(data));

        /************************************************/
        var oVizFrame = this.getView().byId("idVizFrameLine");
        oVizFrame.setDataset(this._createDataSet());
        oVizFrame.setModel(this.oModel);
        oVizFrame.setVizProperties(this._createVizProperties(data));
        oVizFrame.addFeed(this._createFeedValueAxis());
        oVizFrame.addFeed(this._createFeedCategoryAxis());

        var oPopOver = this.getView().byId("idPopOver");
        oPopOver.connect(oVizFrame.getVizUid());

        /************************************************/
        var oVizFrameAverageTemperatureByDay = this.getView().byId("idVizFrameColumnAverageTemperatureByDay");
        var avgByDay = this._createAvgByDayData(data);
        var averageByDayModel = new sap.ui.model.json.JSONModel({result: avgByDay});

        var averageByDayDataset = this._createAvgByDayDataSet();
        averageByDayDataset.setModel(averageByDayModel);

    		oVizFrameAverageTemperatureByDay.setDataset(averageByDayDataset);
    		oVizFrameAverageTemperatureByDay.setModel(averageByDayModel);

    		oVizFrameAverageTemperatureByDay.setVizProperties(this._createVizPropertiesAvgTempByDay(avgByDay));

        oVizFrameAverageTemperatureByDay.addFeed(this._createFeedValueAxisAvgTempByTem());
        oVizFrameAverageTemperatureByDay.addFeed(this._createFeedCategoryAxisAvgTempByDay());
        oVizFrameAverageTemperatureByDay.addFeed(this._createFeedColorAvgByDay());

        var oPopOverAverageTemperatureByDay = this.getView().byId("idPopAverageTemperatureByDay");
        oPopOverAverageTemperatureByDay.connect(oVizFrameAverageTemperatureByDay.getVizUid());

        /************************************************/
        var oVizFrameTemperatureMinMax = this.getView().byId("idVizFrameColumnTemperatureMinMax");

    		var minMaxCurrentModel = new sap.ui.model.json.JSONModel(this._getMinMaxCurrent(data));
    		var minMaxDataset = this._createMinMaxDataset();

    		minMaxDataset.setModel(minMaxCurrentModel);

        oVizFrameTemperatureMinMax.setDataset(minMaxDataset);
        oVizFrameTemperatureMinMax.setModel(minMaxCurrentModel);

        oVizFrameTemperatureMinMax.setVizProperties(this._createMinMaxVizProperties());

        oVizFrameTemperatureMinMax.addFeed(this._createFeedValueAxisMinMax());
        oVizFrameTemperatureMinMax.addFeed(this._createFeedCategoryAxisMinMax());
        oVizFrameTemperatureMinMax.addFeed(this._createFeedColorMinMax());

        var oPopOverTemperatureMinMax = this.getView().byId("idPopOverTemperatureMinMax");
        oPopOverTemperatureMinMax.connect(oVizFrameTemperatureMinMax.getVizUid());
    },

    _getMinMaxCurrent: function(obj) {
        var max = _.max(obj, function(v){ return v.temperature; });
        max.type = 'max';

        var min = _.min(obj, function(v){ return v.temperature; });
        min.type = "min";

        var current = _.last(obj);
        current.type = "current";

        return [ min, current, max];
    },

    _getGridModel: function(obj) {
        var gridData = {
            name: "AM2302",
            type: "Temperature/Humidity",
            url: "https://www.google.it/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=am2302",
            gateway: "RaspberryPI B+",
            count: _.size(obj),
            first: _.first(obj).lastAt,
            last: _.last(obj).lastAt
        };
        var _model = new sap.ui.model.json.JSONModel();
        _model.setData(gridData);
        return _model;
    },

    _createDataSet: function() {
        return new sap.viz.ui5.data.FlattenedDataset({
            dimensions: [
                { name : 'Days', value : "{lastAt}" }
            ],
            measures : [
                { name : 'Temperature (°C)', value : '{temperature}' }
            ],
            data : { path : "/" }
        });
    },

    _createFeedValueAxis: function() {
        return new sap.viz.ui5.controls.common.feeds.FeedItem({
            'uid': "valueAxis",
            'type': "Measure",
            'values': ["Temperature (°C)"]
        });
    },

    _createFeedCategoryAxis: function() {
        return new sap.viz.ui5.controls.common.feeds.FeedItem({
            'uid': "categoryAxis",
            'type': "Dimension",
            'values': ["Days"]
        });
    },

    _createVizProperties: function(obj) {
        var lSize = _.size(obj);
        var xAxisUpperLimit = (lSize <= 10) ? lSize - Math.floor(lSize/4) : lSize - Math.floor(lSize/10);

        return {
            plotArea: {
                dataLabel: {
                    visible: false
                },
                window: {
                    end: {
                        categoryAxis: {
                            'Days': obj[xAxisUpperLimit - 1].lastAt
                        }
                    }
                }
            },
            legend: {
                title: { visible: false }
            },
            title: {
                visible: true,
                text: 'Temperature by Days'
            }
        };
    },

    _createAvgByDayData: function(obj) {
        // Grouped by Day
        var groupByDay = _.groupBy(obj, function(item) {
            return item.lastAt.substring(0,10);
        });

        var averageByDay = [];
        _.each(groupByDay, function(value, key, list){
            var result = {};
            result.day = key;
            result.average = _.mean(_.map(value, function(i) { return parseFloat(i.temperature); })).toFixed(1);
            averageByDay.push(result);
        });
        return averageByDay;
    },

    _createAvgByDayDataSet: function() {
        return new sap.viz.ui5.data.FlattenedDataset({
            dimensions: [
                { name : 'Days', value : "{day}" }
            ],
            measures : [
                { name : 'Temp (°C)', value : '{average}' }
            ],
            data : { path : "/result" }
        });
    },

    _createFeedValueAxisAvgTempByTem: function() {
        return new sap.viz.ui5.controls.common.feeds.FeedItem({
            'uid': "valueAxis",
            'type': "Measure",
            'values': ["Temp (°C)"]
        });
    },

    _createFeedCategoryAxisAvgTempByDay: function() {
        return new sap.viz.ui5.controls.common.feeds.FeedItem({
            'uid': "categoryAxis",
            'type': "Dimension",
            'values': ["Days"]
        });
    },

    _createFeedColorAvgByDay: function() {
        return new sap.viz.ui5.controls.common.feeds.FeedItem({
            'uid': "color",
            'type': "Dimension",
            'values': ["Days"]
        });
    },

    _createVizPropertiesAvgTempByDay: function(obj) {
        var lSize = _.size(obj);

        return {
            valueAxis: {
                label: { formatString: 'u' }
            },
            categoryAxis: {
                title: { visible: false }
            },
            plotArea: {
                dataLabel: { visible: true }
            },
            window: {
                end: {
                    categoryAxis: {
                        'Days': obj[lSize - 1].lastAt
                    }
                }
            },
            legend: {
                title: { visible: false }
            },
            title: {
                visible: true,
                text: 'Average By Day'
            }
        };
    },

    _createMinMaxDataset: function() {
        return new sap.viz.ui5.data.FlattenedDataset({
            dimensions: [
                { name : 'Days', value : "{lastAt}" },
                { name : 'Type', value : "{type}" }
            ],
            measures : [
                { name : 'Temp (°C)', value : '{temperature}' }
            ],
            data : { path : "/" }
        });
    },

    _createFeedValueAxisMinMax: function() {
        return new sap.viz.ui5.controls.common.feeds.FeedItem({
            'uid': "valueAxis",
            'type': "Measure",
            'values': ["Temp (°C)"]
        });
    },

    _createFeedCategoryAxisMinMax: function() {
        return new sap.viz.ui5.controls.common.feeds.FeedItem({
            'uid': "categoryAxis",
            'type': "Dimension",
            'values': ["Days"]
        });
    },

    _createFeedColorMinMax: function() {
        return new sap.viz.ui5.controls.common.feeds.FeedItem({
            'uid': "color",
            'type': "Dimension",
            'values': ["Type"]
        });
    },

    _createMinMaxVizProperties: function() {
        return {
            valueAxis: {
                label: { formatString: 'u' }
            },
            categoryAxis: {
                title: { visible: false }
            },
            plotArea: {
                dataLabel: { visible: true }
            },
            legend: {
                title: { visible: false }
            },
            title: {
                visible: true,
                text: 'Min-Max-Current'
            }
        };
    },

	  onNavBack: function() {
        app.back();
    }

    /**
    * Similar to onAfterRendering, but this hook is invoked before the controller's View is re-rendered
    * (NOT before the first rendering! onInit() is used for that one!).
    * @memberOf app.tiles
    */
    //onBeforeRendering: function() {
    //
    //},

    /**
    * Called when the View has been rendered (so its HTML is part of the document). Post-rendering manipulations of the HTML could be done here.
    * This hook is the same one that SAPUI5 controls get after being rendered.
    * @memberOf app.tiles
    */
    //onAfterRendering: function() {
    //
    //},
    /**
    * Called when the Controller is destroyed. Use this one to free resources and finalize activities.
    * @memberOf app.tiles
    */
    //onExit: function() {
    //
    //}
});
