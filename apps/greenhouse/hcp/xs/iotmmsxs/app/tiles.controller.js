sap.ui.controller("app.tiles", {
    /**
    * Called when a controller is instantiated and its View controls (if available) are already created.
    * Can be used to modify the View before it is displayed, to bind event handlers and do other one-time initialization.
    * @memberOf @memberOf app.tiles
    */
    //onInit: function() {
    //
    //},
    /**
    * Similar to onAfterRendering, but this hook is invoked before the controller's View is re-rendered
    * (NOT before the first rendering! onInit() is used for that one!).
    * @memberOf app.tiles
    */
    onBeforeRendering: function() {
        var data =   {
            "lastAt": "",
            "temperature": 0,
            "humidity": 0
        };
        var oModel = new sap.ui.model.json.JSONModel();
        oModel.setData(data);
        sap.ui.getCore().setModel(oModel, "tileModel");
    },


    getLast: function() {
        var url = "services/lastValues.xsjs";
        var _oModel = new sap.ui.model.json.JSONModel();
        _oModel.loadData(url, null, false);

        var data = {
            "lastAt": _oModel.getData().lastAt,
            "temperature": _oModel.getData().temperature,
            "humidity": _oModel.getData().humidity
        };

        this.oModel =  sap.ui.getCore().getModel("tileModel");
        this.oModel.setData(data);
        this.oModel.refresh();
    }

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
