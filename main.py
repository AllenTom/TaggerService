import uvicorn
from server import app
from reg import register_service
import logging


def main():
    # 创建 Consul 客户端
    register_service()
    
    # 启动服务
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
