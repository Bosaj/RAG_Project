from .DataController import DataController
from .ProjectController import ProjectController

__all__ = [
    "DataController",
    "NLPController",
    "ProcessController",
    "ProjectController",
]


def __getattr__(name):
    if name == "NLPController":
        from .NLPController import NLPController

        return NLPController
    if name == "ProcessController":
        from .ProcessController import ProcessController

        return ProcessController
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
