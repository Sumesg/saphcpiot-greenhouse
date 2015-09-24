sap.ui.jsview("app.tiles", {
    /** Specifies the Controller belonging to this View.
    * In the case that it is not implemented, or that "null" is returned, this View does not have a Controller.
    * @memberOf app.tiles
    */
    getControllerName : function() {
        return "app.tiles";
    },
    /** Is initially called once after the Controller has been instantiated. It is the place where the UI is constructed.
    * Since the Controller is given to this method, its event handlers can be attached right away.
    * @memberOf app.tiles
    */
    createContent : function(oController) {
        var temperatureTile = new sap.m.StandardTile("temperatureTile", {
            title : "AM2302",
            numberUnit : "Celsius",
            infoState : "Success",
            icon : sap.ui.core.IconPool.getIconURI("temperature"),
            number: "{tileModel>/temperature}",
            info: "{tileModel>/lastAt}",
            press : function(oEvent) { app.to("idTemperatureChartPage"); }
        });

        var humidityTile = new sap.m.StandardTile("humidityTile", {
            title : "AM2302",
            numberUnit : "Percentage",
            infoState : "Success",
            icon : sap.ui.core.IconPool.getIconURI("heating-cooling"),
            number: "{tileModel>/humidity}",
            info: "{tileModel>/lastAt}",
            press : function(oEvent) { app.to("idHumidityChartPage"); }
        });

        var tileContainer = new sap.m.TileContainer("idMainTiles", {
            height: "500px",
            tiles: [  temperatureTile, humidityTile ]
        });

        //Polling implementation
        setInterval(oController.getLast, 4000);

        // create the page holding the List
        return new sap.m.Page({
            title: "IoT Greenhouse @ SAP Demo Center - SAP Italy",
            content : [ tileContainer ]
        });
    }

});
