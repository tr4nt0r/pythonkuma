"""Uptime Kuma models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum, StrEnum
from typing import Self

from mashumaro import DataClassDictMixin


class MonitorStatus(IntEnum):
    """Monitor states."""

    DOWN = 0
    UP = 1
    PENDING = 2
    MAINTENANCE = 3


class MonitorType(StrEnum):
    """Monitors type."""

    HTTP = "http"
    PORT = "port"
    PING = "ping"
    KEYWORD = "keyword"
    DNS = "dns"
    PUSH = "push"
    STEAM = "steam"
    MQTT = "mqtt"
    SQLSERVER = "sqlserver"
    JSON_QUERY = "json-query"
    GROUP = "group"
    DOCKER = "docker"
    GRPC_KEYWORD = "grpc-keyword"
    REAL_BROWSER = "real-browser"
    GAMEDIG = "gamedig"
    KAFKA_PRODUCER = "kafka-producer"
    POSTGRES = "postgres"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    RADIUS = "radius"
    REDIS = "redis"
    TAILSCALE_PING = "tailscale-ping"
    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, _: object) -> Self:
        """Handle new and unknown monitor types."""
        return cls.UNKNOWN


@dataclass
class UptimeKumaBaseModel(DataClassDictMixin):
    """UptimeKumaBaseModel."""


@dataclass(kw_only=True)
class UptimeKumaMonitor(UptimeKumaBaseModel):
    """Monitor model for Uptime Kuma."""

    monitor_id: int | None = None
    monitor_cert_days_remaining: int
    monitor_cert_is_valid: bool
    monitor_hostname: str | None = field(
        metadata={"deserialize": lambda v: None if v == "null" else v}
    )
    monitor_name: str
    monitor_port: str | None = field(
        metadata={"deserialize": lambda v: None if v == "null" else v}
    )
    monitor_response_time: int = 0
    monitor_status: MonitorStatus
    monitor_type: MonitorType = MonitorType.HTTP
    monitor_url: str | None = field(
        metadata={"deserialize": lambda v: None if v == "null" else v}
    )


@dataclass
class UptimeKumaVersion(UptimeKumaBaseModel):
    """Uptime Kuma version."""

    version: str = ""
    major: str = ""
    minor: str = ""
    patch: str = ""
