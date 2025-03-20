import logging
import os

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
        level=logging.DEBUG,  # nível de log padrão
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # formato do log
        handlers=[
            logging.StreamHandler(),  # imprime no console
        ],
    )
