import requests
import logging
import colorlog

def setup_logger():
    handler = colorlog.StreamHandler()
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(levelname)s] %(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    handler.setFormatter(formatter)
    logger = logging.getLogger("API Logger")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def get_data(endpoint):
    """Запрашивает данные из API."""
    base_url = "https://api.ataix.kz/api"
    url = f"{base_url}/{endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе {endpoint}: {e}")
        return None

def get_currencies():
    """Получает список валют."""
    data = get_data("currencies")
    if data:
        logger.info(f"Всего валют: {len(data)}")
        for currency in data:
            print(currency)

def get_symbols():
    """Получает список торговых пар."""
    data = get_data("symbols")
    if data:
        logger.info(f"Всего торговых пар: {len(data)}")
        for symbol in data:
            print(symbol)

def get_prices():
    """Получает цены всех монет и токенов."""
    data = get_data("prices")
    if data:
        logger.info("Текущие цены монет и токенов:")
        print(data)  # Отладочный вывод

        if isinstance(data, dict) and "result" in data:
            prices = data["result"]
            if isinstance(prices, list):
                for item in prices:
                    if isinstance(item, dict) and "symbol" in item and "price" in item:
                        print(f"{item['symbol']}: {item['price']}")
                    else:
                        logger.warning(f"Неожиданный формат элемента: {item}")
            else:
                logger.error("Поле 'result' не является списком!")
        else:
            logger.error("API вернуло неожиданный формат данных!")


if __name__ == "__main__":
    logger = setup_logger()
    get_currencies()
    get_symbols()
    get_prices()