import logging

_LOG_FORMAT = '[%(asctime)s %(name)-20.20s %(levelname)7.7s] %(message)s'


def configure_logging_with_arguments(
        is_verbose=False, log_filepath=None, use_buffered_logs=False):

    logger = logging.getLogger()

    if is_verbose is True:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)

    logging.basicConfig(format=_LOG_FORMAT)

def configure_logging_with_commandline(args):

    configure_logging_with_arguments(
        is_verbose=args.is_verbose,
        log_filepath=args.log_filepath,
        use_buffered_logs=args.use_buffered_logs)
