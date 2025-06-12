"""Python API wrapper for Uptime Kuma."""

from .exceptions import (
    UptimeKumaAuthenticationException,
    UptimeKumaConnectionException,
    UptimeKumaException,
)
from .models import MonitorStatus, MonitorType, UptimeKumaMonitor, UptimeKumaVersion
from .uptimekuma import UptimeKuma

__version__ = "0.2.0rc1"

__all__ = [
    "MonitorStatus",
    "MonitorType",
    "UptimeKuma",
    "UptimeKumaAuthenticationException",
    "UptimeKumaConnectionException",
    "UptimeKumaException",
    "UptimeKumaMonitor",
    "UptimeKumaVersion",
]
