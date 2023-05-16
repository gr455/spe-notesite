import subprocess, time

months = {"May":"05"}

while (True):
    # Run the command and capture its output
    time.sleep(10)
    output = subprocess.check_output('kubectl logs notesite-78b9b6f4b5-s5wkh', shell=True)

    # Open a file and write the output to it
    with open('ScriptLogs.log', 'w') as f:
        f.write(output.decode('utf-8'))

    filename = 'ScriptLogs.log'

    # Read the contents of the file into a list
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Remove the lines you don't want to keep
    lines_to_remove = []
    for i in range(len(lines)):
        if lines[i][0] != '[':
            lines_to_remove.append(i)

    lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]

    for i in range(len(lines)):
        fields = lines[i].split(" ")
        date = fields[0]
        date_fields = date.split("/")
        month = months[date_fields[1]]
        date = date_fields[0] + "/" + month + "/" + date_fields[2]
        for j in range(1, len(fields)):
            date += " " + fields[j]
        lines[i] = date

    # Write the modified contents back to the file
    with open(filename, 'w') as f:
        f.writelines(lines)

