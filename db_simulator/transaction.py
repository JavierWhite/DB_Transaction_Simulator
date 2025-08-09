from dataclasses import dataclass, field
    
@dataclass
class Transaction:
    tid: int
    state: str ='ACTIVE'
    ops_executed: int = 0
    blocked: bool = False
    wait_since: int = 0
    history: list = field(default_factory=list)

    
