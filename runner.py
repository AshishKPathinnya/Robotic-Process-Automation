# runner.py

import subprocess
import time

def run_gmail_script():
    subprocess.run(["python", "gmail.py"])

def run_zoomlog_script():
    subprocess.run(["python", "zoomlog.py"])

if __name__ == "__main__":
    # Step 1: Run gmail.py to create the 'email_1.py' file
    run_gmail_script()

    # Wait for 5 seconds to allow some time for email_1.py to be created
    time.sleep(5)

    # Step 2: Run zoomlog.py to use the credentials from 'email_1.py'
    run_zoomlog_script()

    # Wait for 2 seconds to allow some time for urlsend.py to be created
    time.sleep(2)
