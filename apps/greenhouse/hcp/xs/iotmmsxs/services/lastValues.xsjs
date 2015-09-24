var last_insert_query = 'SELECT TOP 1 "G_CREATED", "C_HUMIDITY", "C_TEMPERATURE" FROM "NEO_<schema_id>"."T_IOT_<message_type_id>" ORDER BY "G_CREATED" DESC';

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
function getLastValues(){
    var measurementsList = [];
    var result = {};
    var connection = $.db.getConnection();
    var statement = null;
    var resultSet = null;
    try {
        // select last
        statement = connection.prepareStatement(last_insert_query);
        resultSet = statement.executeQuery();
        while (resultSet.next()) {
            result.lastAt = resultSet.getString(1).substring(0, 19);
            result.humidity = resultSet.getString(2).substring(0,4);
            result.temperature = resultSet.getString(3).substring(0,4);
            measurementsList.push(result);
        }
    } finally {
        close([resultSet, statement, connection]);
    }
    return result;
}

function doGet() {
    try{
        $.response.contentType = "application/json";
        $.response.setBody(JSON.stringify(getLastValues()));
    } catch(err) {
        $.response.contentType = "text/plain";
        $.response.setBody("Error while executing query: [" + err.message + "]");
        $.response.status = $.net.http.INTERNAL_SERVER_ERROR;
    }
}
doGet();
