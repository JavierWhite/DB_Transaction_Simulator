from dataclasses import dataclass, field, fields
    
@dataclass
class Transaction:
    tid: int
    state: str ='ACTIVE'
    operation_executed: int =0
    blocked: bool = False
    wait_since: int = 0
    local_changes: dict = field(default_factory=dict)
    history: list = field(default_factory=list)

    
