import uvicorn
from typing import Dict
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


app = FastAPI()


TORTOISE_ORM: Dict = {
    "connections": {
        # 开发环境使用 SQLite（基于文件，无需服务器）
        # "default": "sqlite://db.sqlite3",
        # 生产环境示例：MySQL
        "default": "mysql://lcf:1522@127.0.0.1:3306/fastapi_db"
    },
    "apps": {
        "models": {
            # 模型模块和 Aerich 迁移模型
            "models": ["orm_define_model", "aerich.models"],
            "default_connection": "default",
        }
    },
    # 连接池配置
    # 是否使用时区
    "use_tz": False,
    # 默认时区
    "timezone": "UTC",
    "connection_pool": {
        # 最大连接数
        "max_size": 10,
        # 最小连接数
        "min_size": 1,
        # 空闲连接超时（秒）
        "idle_timeout": 30
    }
}

register_tortoise(app, 
                  config=TORTOISE_ORM, 
                  generate_schemas=True,    # 开发环境自动生成表结构
                  add_exception_handlers=True)


if __name__ == "__main__":
    uvicorn.run("orm_define:app", host="127.0.0.1", port=8000, reload=True)
