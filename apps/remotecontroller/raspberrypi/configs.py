print("Please configure appropriately and then remove this line !")
exit()
###
# RaspberryPI
###

# Lamp
lamp_pin = 23
# servo
servo_pin = 4
servo_frequency = 100

# Path and file names for logging
remote_controller_file_path = "logs/remotecontroller.log"

###
# HCP
###

# these credentials are used from applications with the "push messages to devices" API
hcp_user = "account_username"
hcp_password = "account_password"

# the following values need to be taken from the IoT Cockpit
iot_url = "the_iotmms_app_url"
device_id = "the_id_of_the_device_you_created_in_the_iot_cockpit"
device_token = "the_oauth_token_shown_for_the_created_device"
message_type_id = "the_message_type_id_From_device_you_created_in_the_iot_cockpit"
