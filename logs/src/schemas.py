from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import date, time


class ResourceEnum(str, Enum):
    nginx = "nginx"
    service = "service"

class AddToEnum(str, Enum):
    db = "db"
    github = "github"

class ConvertToEnum(str, Enum):
    csv = "csv"
    json = "json"


class NginxLog(BaseModel):
    client_ip: str = Field(description="Client IP address")
    remote_user: Optional[str] = Field(
        default=None,
        description="Authenticated user name (Basic Auth)"
    )
    ident_user: Optional[str] = Field(
        default=None,
        description="Identd user (rarely used)"
    )
    log_date: date = Field(description="Request date")
    log_time: time = Field(description="Request time UTC")
    method: str = Field(description="HTTP request method")
    uri: str = Field(description="Request URI including query string")
    protocol: str = Field(description="HTTP protocol version")
    status: int = Field(
        description="HTTP response status code returned by nginx"
    )
    referer: Optional[str] = Field(
        default=None,
        description="HTTP Referer header"
    )
    user_agent: Optional[str] = Field(
        default=None,
        description="Client User-Agent string"
    )
    request_length: int = Field(
        description="Total size of the HTTP request in bytes"
    )
    request_time: float = Field(
        description="Time spent processing the request by nginx (seconds)"
    )
    upstream_name: Optional[str] = Field(
        default=None,
        description="Upstream name or service identifier"
    )
    alternative_upstream: Optional[str] = Field(
        default=None,
        description="Fallback or alternative upstream (if any)"
    )
    upstream_addr: Optional[str] = Field(
        default=None,
        description="Backend address in IP:PORT format"
    )
    upstream_response_length: Optional[int] = Field(
        default=None,
        description="Number of attempts to connect to the upstream"
    )
    upstream_response_time: Optional[float] = Field(
        default=None,
        description="Time taken to receive response from upstream (seconds)"
    )
    upstream_status: Optional[int] = Field(
        default=None,
        description="HTTP status code returned by the upstream"
    )
    request_id: Optional[str] = Field(
        default=None,
        description="Unique request identifier for tracing"
    )