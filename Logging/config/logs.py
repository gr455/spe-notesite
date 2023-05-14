import subprocess, time
from datetime import datetime

months = {"May":"05"}

while (True):
    # Run the command and capture its output
    time.sleep(10)
    output = subprocess.check_output('kubectl logs notesite-78b9b6f4b5-s5wkh', shell=True)

    # Open a file and write the output to it
    with open('backend1.log', 'w') as f:
        f.write(output.decode('utf-8'))

    filename = 'backend1.log'

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
        date = date_fields[0][1:] + "/" + month + "/" + date_fields[2][:-1]
        time_field = fields[1]
        time_fields = time_field.split(":")
        # print(date_fields[2][:len(date_fields[2])-1])
        dt = datetime(int(date_fields[2][:len(date_fields[2])]), int(month), int(date_fields[0][1:]), int(time_fields[0]), int(time_fields[1]), int(time_fields[2][:-1]))
        
        dt = dt.isoformat()
        dt += ".000Z"
        for j in range(2, len(fields)):
            fields[j] = fields[j].replace("\"", "")
                
            dt += " " + fields[j]
        lines[i] = dt

    # Write the modified contents back to the file
    with open(filename, 'w') as f:
        f.writelines(lines)

