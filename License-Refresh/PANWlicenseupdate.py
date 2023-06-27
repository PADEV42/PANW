#!/usr/bin/env python3

import paramiko
import time
import getpass

# Prompt the user for credentials
#hostname = input("Enter the IP address: ")
username = input("Enter the username: ")
password = getpass.getpass("Enter the password: ")

# We are going to request the licenses
# This will pull Subs and Support then clean up the admin sessions after the refresh
commands = ['request license fetch', 'q', 'delete admin-sessions']


#Below we are automating the workload as it pulls from the hosts file.
def ssh_to_firewall(host, username, password):
	# Set up the SSH client
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	print('\n' + f"Connecting to the {host}...")
	client.connect(hostname=host, username=username, password=password)
	
	print("Connected successfully. Waiting for the shell prompt...")
	# Wait 10 seconds for the shell prompt
	time.sleep(10)
	
	# Start an interactive shell session and wait 10 seconds
	channel = client.invoke_shell()
	time.sleep(10)
	print("Shell prompt received. Sending the command...")
	
	# Now we will loop through the series of command in the array above "commands"
	for command in commands:
		print(f"Sending command: {command}...")
		# Send the command
		channel.send(command + '\n')
		# Wait for the command to execute
		time.sleep(5)  # Adjust as necessary
		# Receive the output
		output = channel.recv(1024)
		# Print the output
		print("Command executed. Here's the output:\n")
		print(output.decode('utf-8'))
		print("Waiting 5 seconds before the next command...\n")
		time.sleep(5)  # Adjust as necessary
		
	print("Closing the connection...")
	# Close the connection
	client.close()
	print("Connection closed.")


# We are calling the host file that was exported from panormaa
def main():
	# Path to the host file
	host_file = 'hosts.txt'
	
	try:
		# Read the host file
		with open(host_file, 'r') as file:
			hosts = file.readlines()
			
		# Loop through hosts and execute SSH commands
		for host in hosts:
			host = host.strip()  # Remove leading/trailing whitespaces
			ssh_to_firewall(host, username, password)
			print()
	except FileNotFoundError:
		print(f"Host file '{host_file}' not found.")
		
if __name__ == '__main__':
	main()