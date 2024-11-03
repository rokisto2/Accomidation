from fastapi import FastAPI
from routers import routers

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

# Подключение всех роутеров с префиксами
for router, prefix in routers:
    app.include_router(router, prefix=f"/api/{prefix}", tags=[prefix])
