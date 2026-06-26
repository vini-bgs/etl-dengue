from loguru import logger
from sys import stderr

logger.add(
    sink=stderr, format="{time} <r>{level}</r> <g>{message}</g> {file}", level="INFO"
)

logger.add(
    "logs.log",  # Arquivo onde os logs serão salvos
    format="{time} {level} {message} {file}",
    level="INFO",
)

# Exemplo de uso do logger
logger.info("Este é um log de informação.")
logger.error("Este é um log de erro.")
