import os
import time
import sys
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ======================================================
# Folder where Ubuntu copies alerts.json
# ======================================================

WATCH_FOLDER = r"C:\WazuhShared"


# ======================================================
# Event Handler
# ======================================================

class AlertHandler(FileSystemEventHandler):

    def on_modified(self, event):

        if event.is_directory:
            return

        if event.src_path.endswith("alerts.json"):

            print("\n" + "=" * 70)
            print("New Wazuh alert detected...")
            print("=" * 70 + "\n")

            python = sys.executable
        try:
            # -----------------------------------------
            # Step 1 : Read latest alert
            # -----------------------------------------
            subprocess.run(
                [python, "wazuh\\alert_reader.py"],
                check=True,
                env=os.environ.copy()
            )

            # -----------------------------------------
            # Step 2 : Generate RAG + Llama + PDF
            # -----------------------------------------
            subprocess.run(
                [python, "scripts\\soc_assistant.py"],
                check=True,
                env=os.environ.copy()
            )

            print("\n" + "=" * 70)
            print("SOC Analysis Completed Successfully")
            print("=" * 70)

        except subprocess.CalledProcessError as e:

            print("\nERROR while executing pipeline")
            print(e)

            
                
                


# ======================================================
# Main
# ======================================================

if __name__ == "__main__":

    print("Watching for Wazuh alerts...\n")

    observer = Observer()
    observer.schedule(
        AlertHandler(),
        WATCH_FOLDER,
        recursive=False
    )

    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        observer.stop()

    observer.join()