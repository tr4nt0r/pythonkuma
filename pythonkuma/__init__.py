"""Python API wrapper for Uptime Kuma."""

from .exceptions import (
    UptimeKumaAuthenticationException,
    UptimeKumaConnectionException,
    UptimeKumaException,
)
from .models import MonitorType, UptimeKumaApiResponse, UptimeKumaMonitor
from .uptimekuma import UptimeKuma

__version__ = "0.0.0rc1"

__all__ = [
    "MonitorType",
    "UptimeKuma",
    "UptimeKumaApiResponse",
    "UptimeKumaAuthenticationException",
    "UptimeKumaConnectionException",
    "UptimeKumaException",
    "UptimeKumaMonitor",
]
