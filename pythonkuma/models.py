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

    # General monitor type
    HTTP = "http"
    KEYWORD = "keyword"
    PORT = "port"
    PING = "ping"
    DNS = "dns"
    DOCKER = "docker"
    SYSTEM_SERVICE = "system-service"
    REAL_BROWSER = "real-browser"
    # Special
    GROUP = "group"
    # Passive monitor type
    PUSH = "push"
    MANUAL = "manual"
    # Specific monitor type
    GLOBALPING = "globalping"
    GRPC_KEYWORD = "grpc-keyword"
    JSON_QUERY = "json-query"
    KAFKA_PRODUCER = "kafka-producer"
    MQTT = "mqtt"
    RABBIT_MQ = "rabbitmq"
    SIP_OPTIONS = "sip-options"
    SMTP = "smtp"
    SNMP = "snmp"
    TAILSCALE_PING = "tailscale-ping"
    WEBSOCKET_UPGRADE = "websocket-upgrade"
    # Database monitor type
    SQLSERVER = "sqlserver"
    MONGODB = "mongodb"
    MYSQL = "mysql"
    ORACLEDB = "oracledb"
    POSTGRES = "postgres"
    REDIS = "redis"
    RADIUS = "radius"
    # Game server
    GAMEDIG = "gamedig"
    STEAM = "steam"
    # other
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
    monitor_cert_days_remaining: int | None = None
    monitor_cert_is_valid: bool | None = None
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
    monitor_uptime_ratio_1d: float | None = None
    monitor_uptime_ratio_30d: float | None = None
    monitor_uptime_ratio_365d: float | None = None

    monitor_response_time_seconds_1d: float | None = None
    monitor_response_time_seconds_30d: float | None = None
    monitor_response_time_seconds_365d: float | None = None

    monitor_tags: list[str]


@dataclass
class UptimeKumaVersion(UptimeKumaBaseModel):
    """Uptime Kuma version."""

    version: str = ""
    major: str = ""
    minor: str = ""
    patch: str = ""
