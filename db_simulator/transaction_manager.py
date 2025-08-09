import random
from logger import FLUSH_THRESHOLD
from transaction import Transaction

class TransactionManager:
    """Coordinates transaction lifecycle, logging, and operations."""
    def __init__(self, lock_mgr, log_mgr, storage_mgr, args):
        self.lock_mgr = lock_mgr
        self.log_mgr = log_mgr
        self.storage_mgr = storage_mgr
        self.args = args
        self.active = {}
        self.next_tid = 0

    def start_transaction(self):
        tid = self.next_tid
        self.next_tid += 1
        txn = Transaction(tid)
        self.active[tid] = txn
        self.log_mgr.record((tid, 'S'))
        txn.history.append(('S',))
        return txn

    def submit_op(self, txn, current_cycle):
        did = random.randrange(32)
        if txn.ops_executed >= self.args.tx_size:
            return self.commit(txn)
        if random.random() < self.args.rollback_prob:
            return self.rollback(txn)
        if random.random() < self.args.write_prob:
            return self._write(txn, did)
        return self._read(txn, did)

    def _read(self, txn, did):
        if self.lock_mgr.request(txn.tid, did, 'S', None):
            txn.ops_executed += 1
            txn.history.append(('R', did))
        else:
            txn.blocked = True

    def _write(self, txn, did):
        if self.lock_mgr.request(txn.tid, did, 'X', None):
            old = self.storage_mgr.buffer[did]
            new = '1' if old == '0' else '0'
            self.storage_mgr.buffer[did] = new
            self.log_mgr.record((txn.tid, 'F', did, new, 'F'))
            txn.history.append(('W', did, new))
            txn.ops_executed += 1
            if self.log_mgr.write_count >= FLUSH_THRESHOLD:
                self.storage_mgr.flush()
                self.log_mgr.write_count = 0
        else:
            txn.blocked = True

    def rollback(self, txn):
        self.log_mgr.record((txn.tid, 'R'))
        self.lock_mgr.release_all(txn.tid)
        txn.state = 'ABORTED'
        txn.history.append(('R',))


    def commit(self, txn):
        self.log_mgr.record((txn.tid, 'C'))
        self.lock_mgr.release_all(txn.tid)
        txn.state = 'COMMITTED'
        txn.history.append(('C',))
        