import csv
from log_manager import LOG_FILE

class RecoveryManager:
    """Replays log to recover database state on startup."""
    def __init__(self, storage):
        self.storage = storage

    def recover(self):
        self.storage.load()
        with open(LOG_FILE, 'r') as f:
            reader = csv.reader(f)
            active = {}
            for row in reader:
                tid, op = int(row[0]), row[1]
                if op == 'S': active[tid] = True
                elif op == 'F':
                    did, new = int(row[2]), row[3]
                    self.storage.buffer[did] = new
                elif op in ('R', 'C'):
                    active[tid] = False
        self.storage.flush()