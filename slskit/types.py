from dataclasses import dataclass
from typing import Any, Dict

AnyDict = Dict[str, Any]


@dataclass(frozen=True)
class Result:
    valid: bool
    value: Any


class MinionDict(Dict[str, Result]):
    @property
    def all_valid(self) -> bool:
        return all(result.valid for result in self.values())

    @property
    def output(self) -> AnyDict:
        return {minion_id: result.value for minion_id, result in self.items()}
