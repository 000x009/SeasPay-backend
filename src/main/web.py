import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dishka.integrations.fastapi import setup_dishka

from src.main.di import get_di_container
from src.presentation import include_all_routers, include_exception_handlers


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

def create_app() -> FastAPI:
    app = FastAPI()
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://176.124.214.52:5173",
        "https://seaspayment.com",
        "https://www.seaspayment.com",
        "http://seaspayment.com",
        "http://www.seaspayment.com",
        "https://testnet-pay.crypt.bot/",
        "https://pay.crypt.bot/",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    include_all_routers(app)
    include_exception_handlers(app)
    setup_dishka(get_di_container(), app)

    return app


app = create_app()
