import subprocess

# Call .py using subprocess
result = subprocess.run(['python3', 'get_connection_status.py'], stdout=subprocess.PIPE)
c = result.stdout.decode('utf-8')

# Remove blank characters from the feedback
c = c.strip()

# Print the feedback from 3.py
print(c)

