import logging
import sys
from loguru import logger
import json
from datetime import datetime
from pathlib import Path

__LOGGING_PATH__ = Path(__file__).parent.joinpath("logs")


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


class FastApiLogger:

    @classmethod
    def make_logger(cls, config_path: Path):
        config = cls.load_logging_config(config_path)
        logging_config = config.get('logger')
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d_%I:%M:%S %p")
        log_file_name = str(__LOGGING_PATH__.joinpath(f'log_{dt_string}.log'))

        log = cls.customize_logging(
            filepath=log_file_name,
            level=logging_config.get('level'),
            retention=logging_config.get('retention'),
            rotation=logging_config.get('rotation'),
            format=logging_config.get('format')
        )
        return log

    @classmethod
    def customize_logging(
            cls,
            filepath: Path,
            level: str,
            rotation: str,
            retention: str,
            format: str,
    ):
        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ['uvicorn',
                     'uvicorn.error',
                     'fastapi'
                     ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)

    @classmethod
    def load_logging_config(cls, config_path):
        with open(config_path) as config_file:
            config = json.load(config_file)
        return config
