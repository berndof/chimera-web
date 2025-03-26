import logging

logging.basicConfig(
    level=logging.DEBUG,  # nível de log padrão
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # formato do log
    handlers=[
        logging.StreamHandler(),  # imprime no console
    ],
)
