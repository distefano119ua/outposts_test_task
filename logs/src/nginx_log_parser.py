from pydantic import ValidationError, create_model
from datetime import datetime, date, time
from typing import Optional, List
import re

from .schemas import NginxLog

LOG_PATTERN = re.compile(
    r'(?P<client_ip>\S+)\s+'                  # 1) client IP
    r'(?P<ident_user>\S+)\s+'                 # 2) ident user
    r'(?P<remote_user>\S+)\s+'                # 3) remote user
    r'\[(?P<timestamp>[^\]]+)\]\s+'           # 4) [time]
    r'"(?P<method>\S+)\s+'                    # 5) "METHOD
    r'(?P<uri>\S+)\s+'                        # 6) URI
    r'(?P<protocol>[^"]+)"\s+'                # 7) PROTOCOL"
    r'(?P<status>\d+)\s+'                     # 8) status
    r'(?P<body_bytes_sent>\d+)\s+'            # 9) body bytes sent
    r'"(?P<referer>[^"]*)"\s+'                # 10) "referer"
    r'"(?P<user_agent>[^"]*)"\s+'             # 11) "user agent"
    r'(?P<request_length>\d+)\s+'             # 12) request length
    r'(?P<request_time>[\d.]+)\s+'            # 13) request time
    r'\[(?P<upstream_name>[^\]]*)\]\s+'       # 14) [upstream name]
    r'\[(?P<alt_upstream>[^\]]*)\]\s+'        # 15) [alt upstream]
    r'(?P<upstream_addr>\S+)\s+'              # 16) upstream addr
    r'(?P<upstream_response_length>\d+)\s+'   # 17) upstream response length (у тебя это НЕ attempts)
    r'(?P<upstream_response_time>[\d.]+)\s+'  # 18) upstream response time
    r'(?P<upstream_status>\d+)\s+'            # 19) upstream status
    r'(?P<request_id>\S+)\s*$'                # 20) request id
)


def match_logs(logs: list[str]) -> list[dict]:
    result = []
    for line in logs:
        m = LOG_PATTERN.match(line)
        if not m:
            #TODO add logging
            #raise ValueError(f"Invalid log line: {line}")
            continue

        result.append(m.groupdict())
    return result


def normalize_logs(logs: list[dict]) -> list[dict]:
    result = []

    #Currnetly for normalizing timestamp
    for log in logs:
        raw_ts = log.get("timestamp")
        if not raw_ts:
            #ADD logging
            print(f'Absent timestamp for request_id: {log.get("request_id")}', flush=True)
            continue

        dt = datetime.strptime(raw_ts, "%d/%b/%Y:%H:%M:%S %z")

        log['log_date'] = dt.date()
        log['log_time'] = dt.time()
        del log["timestamp"]
        result.append(log)

    return result


def validate_logs(logs: list[dict]) -> List[NginxLog]:
    result: List[NginxLog] = []

    for log in logs:
        try:
            result.append(NginxLog(**log))
        #TO DO add logging for validation errors
        except ValidationError as e:
            print('Validation error:', flush=True)
            print(e, flush=True)
            continue
        # TO DO add logging for exception errors
        except Exception:
            continue
    return result


def parse_nginx_logs(logs) -> List[NginxLog]:

    data = match_logs(logs)
    noramalized_data = normalize_logs(data)
    validated_data = validate_logs(noramalized_data)
    return validated_data


def make_fields_model():
    return create_model(
        "NginxLogFields",
        **{
            name: (Optional[bool], None) for name in NginxLog.model_fields.keys()
        }
    )

NginxLogFields = make_fields_model()