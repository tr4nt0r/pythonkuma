"""Uptime Kuma exceptions."""


class UptimeKumaException(Exception):
    """Base Uptime Kuma exception."""


class UptimeKumaConnectionException(UptimeKumaException):
    """Uptime Kuma connection exception."""


class UptimeKumaAuthenticationException(UptimeKumaException):
    """Uptime Kuma authentication exception."""


class UptimeKumaParseException(UptimeKumaException):
    """Exception raised when parsing of Prometheus metrics fails."""


class UpdateException(Exception):
    """Exception raised for errors fetching latest release from github."""
