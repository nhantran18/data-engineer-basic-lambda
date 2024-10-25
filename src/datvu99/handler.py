import logging
import traceback

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def trigger_handler_events(event, context):
    try:
        logger.info(f"EVENT: {event}")
        logger.info(f"CONTEXT: {context}")

        logger.info(f"test update code")

        return {"status": "SUCCESS"}
    except Exception as ex:
        logger.error(f'FATAL ERROR: {ex} %s')
        logger.error('TRACEBACK:')
        logger.error(traceback.format_exc())

        return {"status": "FAIL", "error": f"{ex}"}
