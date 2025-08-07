import random
from lock_manager import LockManager
from logger import LogManager
from storage_manager import StorageManager
from recovery_manager import RecoveryManager
from transaction_manager import TransactionManager

class SimulationEngine:
    """Drives the cycle-based simulation of transactions."""
    def __init__(self, args):
        self.args = args
        self.cycle = 0
        self.lock_mgr = LockManager()
        self.log_mgr = LogManager()
        self.storage_mgr = StorageManager()
        self.recovery_mgr = RecoveryManager(self.storage_mgr)
        self.txn_mgr = TransactionManager(
            self.lock_mgr, self.log_mgr, self.storage_mgr, args
        )

    def run(self):
        self.recovery_mgr.recover()
        while self.cycle < self.args.max_cycles:
            if random.random() < self.args.start_prob:
                self.txn_mgr.start_transaction()
            for txn in list(self.txn_mgr.active.values()):
                if txn.state == 'ACTIVE' and not txn.blocked:
                    self.txn_mgr.submit_op(txn, self.cycle)
                if txn.blocked:
                    txn.wait_since += 1
                    if txn.wait_since >= self.args.timeout:
                        self.txn_mgr.rollback(txn)
            self.cycle += 1
        self.log_mgr.close()