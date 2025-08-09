from collections import deque

NUM_ITEMS = 32

class LockManager:
    """Manages shared and exclusive locks on data items."""
    def __init__(self):
        self.table = {
            i: {'granted': set(), 'type': None, 'queue': deque()}
            for i in range(NUM_ITEMS)
        }

    def request(self, tid, did, lock_type, current_cycle):
        entry = self.table[did]
        if entry['type'] is None or (
            lock_type == 'S' and entry['type'] == 'S' and not entry['queue']
        ):
            entry['granted'].add(tid)
            entry['type'] = lock_type if entry['type'] is None else entry['type']
            return True
        entry['queue'].append((tid, lock_type, current_cycle))
        return False

    def release_all(self, tid):
        for did, entry in self.table.items():
            if tid in entry['granted']:
                entry['granted'].remove(tid)
                if not entry['granted']:
                    entry['type'] = None
            if entry['type'] is None and entry['queue']:
                next_tid, next_type, _ = entry['queue'].popleft()
                entry['granted'].add(next_tid)
                entry['type'] = next_type