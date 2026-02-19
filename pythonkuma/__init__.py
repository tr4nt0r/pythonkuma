"""Python API wrapper for Uptime Kuma."""

from .exceptions import (
    UpdateException,
    UptimeKumaAuthenticationException,
    UptimeKumaConnectionException,
    UptimeKumaException,
    UptimeKumaParseException,
)
from .models import MonitorStatus, MonitorType, UptimeKumaMonitor, UptimeKumaVersion
from .update import UpdateChecker
from .uptimekuma import UptimeKuma

__version__ = "0.5.0"

__all__ = [
    "MonitorStatus",
    "MonitorType",
    "UpdateChecker",
    "UpdateException",
    "UptimeKuma",
    "UptimeKumaAuthenticationException",
    "UptimeKumaConnectionException",
    "UptimeKumaException",
    "UptimeKumaMonitor",
    "UptimeKumaParseException",
    "UptimeKumaVersion",
]
