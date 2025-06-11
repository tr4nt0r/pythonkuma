"""Python API wrapper for Uptime Kuma."""

from .exceptions import (
    UptimeKumaAuthenticationException,
    UptimeKumaConnectionException,
    UptimeKumaException,
)
from .models import MonitorStatus, MonitorType, UptimeKumaMonitor
from .uptimekuma import UptimeKuma

__version__ = "0.1.0"

__all__ = [
    "MonitorStatus",
    "MonitorType",
    "UptimeKuma",
    "UptimeKumaAuthenticationException",
    "UptimeKumaConnectionException",
    "UptimeKumaException",
    "UptimeKumaMonitor",
]
