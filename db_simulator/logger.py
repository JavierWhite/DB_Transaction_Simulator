import os
import csv

LOG_FILE = 'log'
FLUSH_THRESHOLD = 25

class LogManager:
    """Handles write-ahead logging in CSV format."""
    def __init__(self):
        self.write_count = 0
        if not os.path.exists(LOG_FILE):
            open(LOG_FILE, 'w').close()
        self.log_fp = open(LOG_FILE, 'a', newline='')
        self.writer = csv.writer(self.log_fp)

    def record(self, record):
        self.writer.writerow(record)
        self.log_fp.flush()
        if record and record[-1] == 'F':
            self.write_count += 1

    def close(self):
        self.log_fp.close()