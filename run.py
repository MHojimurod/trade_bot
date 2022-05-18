from concurrent.futures import thread
import subprocess
from threading import Thread

# Path to a Python interpreter that runs any Python script
# under the virtualenv /path/to/virtualenv/
python_bin = "venv/Scripts/python.exe"

# Path to the script that must run under the virtualenv
script_file = "manage.py"

for i in [[python_bin, script_file, "runserver"], [python_bin, script_file, "bot"], [python_bin, script_file, "socket"]]:
    print(i[2])
    Thread(target=subprocess.Popen, args=(i,)).start()

while True:
    pass