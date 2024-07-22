import dataclasses
import typing


@dataclasses.dataclass
class QueueDTO:
    name: str
    callback: typing.Callable
    auto_decode: bool = True
    no_ack: bool = True
