"""日誌工具"""

import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logger(name: str = "dataflow", level: str = "INFO"):
    """
    設置 JSON 日誌記錄器
    
    Args:
        name: Logger 名稱
        level: 日誌級別 (DEBUG, INFO, WARNING, ERROR)
    """
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    # 移除現有的 handlers
    logger.handlers.clear()
    
    # JSON 格式 handler (標準輸出)
    json_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter()
    json_handler.setFormatter(formatter)
    logger.addHandler(json_handler)
    
    # 文本格式 handler (標準錯誤)
    text_handler = logging.StreamHandler(sys.stderr)
    text_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    text_handler.setFormatter(text_formatter)
    text_handler.setLevel(logging.WARNING)
    logger.addHandler(text_handler)
    
    return logger




