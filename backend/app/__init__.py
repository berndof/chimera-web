import logging
import os
from app import models

if os.getenv("ENV") == "dev" or os.getenv("ENV") == "test":
    logging.basicConfig(
        level=logging.DEBUG,  # nível de log padrão
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # formato do log
        handlers=[
            logging.StreamHandler(),  # imprime no console
        ],
    )
else:
    logging.basicConfig(
        level=logging.WARN,  # nível de log padrão
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # formato do log
        handlers=[
            logging.StreamHandler(),  # imprime no console
        ],
    )
