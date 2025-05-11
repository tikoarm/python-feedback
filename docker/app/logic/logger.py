import logging
import os


def setup_logger():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    info_handler = logging.FileHandler("logs/info.log")
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    warning_handler = logging.FileHandler("logs/warning.log")
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(formatter)

    error_handler = logging.FileHandler("logs/error.log")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
    logger.addHandler(error_handler)
