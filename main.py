from src.logger import logger
from src.settings import settings


def main() -> None:
    logger.info(settings)


if __name__ == "__main__":
    main()
