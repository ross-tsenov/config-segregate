def test_logger_logging() -> None:
    """Test if the logger correctly logs a message."""
    from src.logger import logger

    test_message = "This is a test message"
    logger.info(test_message)
    logger.setLevel("DEBUG")
