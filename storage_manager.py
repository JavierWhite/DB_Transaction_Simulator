NUM_ITEMS = 32
DB_FILE = 'db'

class StorageManager:
    """Manages in-memory buffer and disk persistence."""
    def __init__(self):
        self.buffer = ['0'] * NUM_ITEMS
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, 'w') as f:
                f.write('0' * NUM_ITEMS)

    def load(self):
        with open(DB_FILE, 'r') as f:
            self.buffer = list(f.read().strip())

    def flush(self):
        with open(DB_FILE, 'w') as f:
            f.write(''.join(self.buffer))