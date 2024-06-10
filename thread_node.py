import os
import pexpect
import time

# Command to execute (absolute path)
command_path = os.path.expanduser('~/openthread/build/simulation/examples/apps/cli/ot-cli-ftd')
command = f'/bin/bash -c "{command_path} 2"'

# Start the process
child = pexpect.spawn(command)

# Function to read non-blocking output
def read_output(child):
    try:
        while True:
            output = child.read_nonblocking(size=1024, timeout=0.1).decode('utf-8')
            if output:
                print(output, end='')
                return output  # Return the output for further processing
    except pexpect.exceptions.TIMEOUT:
        pass  # If timeout is reached, do nothing

# Send a command and read the output
def send_command(child, command):
    child.sendline(command)  # Send the command
    time.sleep(0.5)  # Wait a bit to allow the command to generate output
    return read_output(child)  # Read and return the available output

# Send initial commands
commands = [
    'dataset networkkey 00112233445566778899aabbccddeeff',
    'dataset commit active',
    'ifconfig up',
    'thread start'
]

for cmd in commands:
    send_command(child, cmd)  # Send each command and read the output

# Function to check the state until it becomes "child" or "router"
def wait_for_state_change(child):
    while True:
        output = send_command(child, 'state')  # Send the 'state' command and read the output
        if output and ('child' in output or 'router' in output):
            break
        time.sleep(1)  # Wait a bit before sending the 'state' command again

# Wait for the state to change
wait_for_state_change(child)

# Send the final commands
send_command(child, 'mqtt start')
send_command(child, 'mqtt connect 172.18.0.8 10000')
send_command(child, 'mqtt subscribe bulb')
state = 'off'
send_command(child, 'mqtt register status')

while True:
    output = read_output(child)
    if output is not None:
        if 'on' in output:
            state = 'on'
            print('bulb on')
            send_command(child, 'mqtt publish @2 0 bulb_on')
        elif 'off' in output:
            state = 'off'
            print('bulb off')
            send_command(child, 'mqtt publish @2 0 bulb_off')

# Read any final output
read_output(child)

# Close the process
child.close()

