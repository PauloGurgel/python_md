import logging


def configura_logger():
    root_logger = logging.getLogger('iclinic_finance')
    root_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s: %(name)s - %(threadName)s - [%(levelname)s] - {%(module)s.%(funcName)s:%(lineno)d}  - %(message)s')
    console_handler.setFormatter(formatter)
    root_logger.handlers = [console_handler]

    return root_logger


logger = configura_logger()
