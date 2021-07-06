import sys

stdin_fileno = sys.stdin

# Keeps reading from stdin and quits only if the word 'exit' is there
# This loop, by default does not terminate, since stdin is open
for line in stdin_fileno:
    # Remove trailing newline characters using strip()
    if 'exit' == line.strip():
        print('Found exit. Terminating the program')
        exit(0)
    else:
        print('Message from sys.stdin: ---> {} <---'.format(line))

stdout_fileno = sys.stdout

sample_input = ['Hi', 'Hello', 'exit']

for ip in sample_input:
    # Prints to stdout
    stdout_fileno.write(ip + '\n')

import sys

stdout_fileno = sys.stdout
stderr_fileno = sys.stderr

sample_input = ['Hi', 'Hello', 'exit']

for ip in sample_input:
    # Prints to stdout
    stdout_fileno.write(ip + '\n')
    # Tries to add an Integer with string. Raises an exception
    try:
        ip = ip + 100
    # Catch all exceptions
    except:
        stderr_fileno.write('Exception Occurred!\n')