# -*- coding: utf-8 -*-
"""Manage the id for each runtime"""
import os
from datetime import datetime
from typing import Any

from agentscope.utils.tools import _get_timestamp
from agentscope.utils.tools import _get_process_creation_time
from agentscope.utils.tools import _generate_random_code

_RUNTIME_ID_FORMAT = "run_%Y%m%d-%H%M%S_{}"
_RUNTIME_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


class _Runtime:
    """A singleton class used to record the runtime information, which will
    be initialized when the package is imported."""

    project: str
    """The project name, which is used to identify the project."""

    name: str
    """The name for runtime, which is used to identify this runtime."""

    runtime_id: str
    """The id for runtime, which is used to identify the this runtime and
        name the saving directory."""

    pid: int
    """The process id of the runtime."""

    _timestamp: datetime
    """The timestamp of when the runtime is initialized."""

    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        """Create a singleton instance."""
        if not cls._instance:
            cls._instance = super(_Runtime, cls).__new__(
                cls,
                *args,
                **kwargs,
            )
        return cls._instance

    def __init__(self) -> None:
        """Generate random project name, runtime name and default
        runtime_id when the package is initialized. After that, user can set
        them by calling `agentscope.init(project="xxx", name="xxx",
        runtime_id="xxx")`."""

        self.project = _generate_random_code()
        self.name = _generate_random_code(uppercase=False)

        self.pid = os.getpid()
        self._timestamp = _get_process_creation_time()

        # Obtain time from timestamp in string format, and then turn it into
        # runtime ID format
        self.runtime_id = _get_timestamp(
            _RUNTIME_ID_FORMAT,
            self._timestamp,
        ).format(self.name)

    def generate_new_runtime_id(self) -> str:
        """Generate a new random runtime id."""
        return _get_timestamp(_RUNTIME_ID_FORMAT).format(
            _generate_random_code(uppercase=False),
        )

    @property
    def timestamp(self) -> str:
        """Get the current timestamp in specific format."""
        return self._timestamp.strftime(_RUNTIME_TIMESTAMP_FORMAT)

    @staticmethod
    def _flush() -> None:
        """
        Only for unittest usage. Don't use this function in your code.
        Flush the runtime singleton.
        """
        global _runtime
        _runtime = _Runtime()


_runtime = _Runtime()
