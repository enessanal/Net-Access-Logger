import os
import time
import datetime
import requests
import subprocess

DELAY_SECONDS = 30

ping_host = "google.com"
output_path = ""

wan_ip_api = "http://icanhazip.com"


try:
    output_path = os.path.expanduser("~/Desktop/network_status.log")
    with open(output_path, 'a') as f:
        f.write("");
except Exception as exception:
    output_path = "./network_status.log"

if not os.path.exists(output_path):
    output_path = "./network_status.log"


while True:
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        ip = requests.get(wan_ip_api).text.strip()
    except requests.exceptions.RequestException as e:
        ip = "ERROR: Could not retrieve IP: " + str(e)

    ping = subprocess.Popen(
        ["ping", "-n", "5", ping_host],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )

    out, error = ping.communicate()

    with open(output_path, 'a') as f:
        if ping.returncode == 0:
            f.write(f"[OK] {now} - IP: {ip}\n")
        else:
            f.write(f"[ERROR] {now} - Ping did not reach {ping_host} - IP: {ip}\n")
        
        # Ping statistics to the file
        f.write("\n\t---- Ping Statistics ----\n")
        f.write("\t"+out.decode().replace("\n","\t\t"))
        if error:
            f.write("\tERROR:\n")
            f.write("\t"+error.decode().replace("\n","\t\t"))
        f.write("\n\t---- End of Statistics ----\n\n")


    time.sleep(DELAY_SECONDS)
