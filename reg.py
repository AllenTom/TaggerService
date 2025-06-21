import consul
from typing import Optional
import logging

def register_service():
    c = consul.Consul()
    c.agent.service.register(
        name="tagger-service",
        service_id="tagger-service",
        address="127.0.0.1",
        port=8000,
        check={
            "http": "http://host.docker.internal:8000/health",  # 健康检查的HTTP端点
            "interval": "10s",                       # 检查间隔
            "timeout": "5s",                         # 超时时间
            "deregister_critical_service_after": "30s"  # 服务不健康30秒后自动注销
        }
    )
