
import csv
import os
from datetime import datetime
from logger import LOG_FILE

class RecoveryManager:
    """Replays log to recover database state on startup."""
    def __init__(self, storage):
        self.storage = storage

    def recover(self, rotate_if_clean: bool = True) -> bool:
        self.storage.load()
        if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
            return False
        
        committed = set()
        active = set()
        records = []
        with open(LOG_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
  
                records.append(row)
                tid, op = int(row[0]), row[1]
                
                if op == 'C' or op == 'R':
                    committed.add(tid) if op == 'C' else None 
                    if tid in active:
                        active.remove(tid)

        for row in records:
            tid = int(row[0])
            op = row[1]
            if op == 'F' and tid in committed:
                did = int(row[2])
                new = row[3]
                self.storage.buffer[did] = new

        self.storage.flush()

        had_inflight =len(active) > 0
        if rotate_if_clean and not had_inflight:
            transaction_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            rotated =f"{LOG_FILE}.{transaction_time}"
            try:
                os.replace(LOG_FILE, rotated)
                open(LOG_FILE, 'w').close()
                print(f"[recovery] clean log detected. Rotated to {rotated}.")
            except OSError as e:
                print(f"[recovery] Log rotation failed: {e}")
        return had_inflight
    