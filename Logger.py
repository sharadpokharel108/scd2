import datetime
from pathlib import Path

class Logger:
    def __init__(self, script_name="Nightly_Batch", log_path="log"):
        log_path = Path(log_path)
        log_path.mkdir(parents=True, exist_ok=True)

        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        log_file_name = f"{script_name}_{current_time}.log"
        self.log_file = open(log_path / log_file_name, 'w')

    def message(self, msg):
        self.log_file.write(str(datetime.datetime.now()))
        self.log_file.write(": ")
        self.log_file.write(msg)
        self.log_file.write("\n")
        self.log_file.flush()

    def error(self, msg):
        self.message("ERROR: " + msg)

    def close(self):
        self.log_file.close()