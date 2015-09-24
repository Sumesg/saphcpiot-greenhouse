var select_all_measurements = 'SELECT "G_CREATED", "C_HUMIDITY", "C_TEMPERATURE" FROM "NEO_<schema_id>"."T_IOT_<message_type_id>" ORDER BY "G_CREATED" ASC';

function close(closables) {
    var closable;
    var i;
    for (i = 0; i < closables.length; i++) {
        closable = closables[i];
        if(closable) {
            closable.close();
        }
    }
}
function getSensorValues(){
    var measurementsList = [];
    var connection = $.db.getConnection();
    var statement = null;
    var resultSet = null;
    try {
        statement = connection.prepareStatement(select_all_measurements);
        resultSet = statement.executeQuery();
        var measurement;

        while (resultSet.next()) {
            measurement = {};
            measurement.lastAt = resultSet.getString(1).substring(0, 19);
            measurement.humidity = resultSet.getString(2).substring(0,4);
            measurement.temperature = resultSet.getString(3).substring(0,4);
            measurementsList.push(measurement);
        }
    } finally {
        close([resultSet, statement, connection]);
    }
    return measurementsList;
}

function doGet() {
    try{
        $.response.contentType = "application/json";
        $.response.setBody(JSON.stringify(getSensorValues()));
    } catch(err) {
        $.response.contentType = "text/plain";
        $.response.setBody("Error while executing query: [" + err.message + "]");
        $.response.returnCode = 200;
    }
}
doGet();
