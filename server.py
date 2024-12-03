from fastapi import FastAPI
import uvicorn
from routers import routers

class Server:
    def __init__(self):
        self.app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

        # Подключение всех роутеров с префиксами
        for router, prefix in routers:
            self.app.include_router(router, prefix=f"/api/{prefix}", tags=[prefix])

    def run(self, host="127.0.0.1", port=8000):
        uvicorn.run(self.app, host=host, port=port)

if __name__ == "__main__":
    server = Server()
    server.run()