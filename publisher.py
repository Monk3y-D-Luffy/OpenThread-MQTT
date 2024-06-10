from paho.mqtt import client as mqtt_client

broker = "172.18.0.7"  # MQTT broker address
port = 1883  # MQTT broker port
topic = "bulb"  # MQTT topic to publish to

def on_connect(client, userdata, flags, rc):
    """
    Callback function called when the client is connected to the broker.
    If the connection is successful, it subscribes to the topic.
    """
    if rc == 0:
        print("Connected to MQTT broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def main():
    """
    Main function that publishes commands to the MQTT broker.
    """
    client = mqtt_client.Client(client_id="publisher")  # Create a client instance
    client.on_connect = on_connect  # Set the callback function for connection
    client.connect(broker, port)  # Connect to the broker

    client.loop_start()  # Start the MQTT client loop

    while True:
    	command = ''
    	while command!='turn on' and command!='turn off':
    		command = input("Enter command 'turn on' or 'turn off': ")
    	client.publish(topic, f"{command} bulb")  # Publish the command to the topic
    	print(f"Published: {command} bulb")  # Print the published command

    client.loop_stop()  # Stop the MQTT client loop

if __name__ == "__main__":
    main()

