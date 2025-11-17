"""幫助函數"""

import json
from typing import Any, Dict, Optional


def parse_json(data: Any) -> Dict[str, Any]:
    """
    解析 JSON 數據
    
    Args:
        data: JSON 字符串或字典
        
    Returns:
        解析後的字典
        
    Raises:
        ValueError: 如果 JSON 格式無效
    """
    if isinstance(data, dict):
        return data
    
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"無效的 JSON: {str(e)}")
    
    raise ValueError(f"無法解析數據類型: {type(data)}")


def flatten_dict(data: Dict[str, Any], parent_key: str = "", sep: str = "_") -> Dict[str, Any]:
    """
    將嵌套字典扁平化
    
    Example:
        >>> data = {"a": {"b": {"c": 1}}, "d": 2}
        >>> flatten_dict(data)
        {'a_b_c': 1, 'd': 2}
    
    Args:
        data: 嵌套字典
        parent_key: 父鍵名（遞歸使用）
        sep: 分隔符
        
    Returns:
        扁平化後的字典
    """
    items = []
    
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        elif isinstance(v, list):
            # 列表轉換為 JSON 字符串
            items.append((new_key, json.dumps(v)))
        else:
            items.append((new_key, v))
    
    return dict(items)


def extract_nested_value(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """
    從嵌套字典中提取值
    
    Example:
        >>> data = {"a": {"b": {"c": 1}}}
        >>> extract_nested_value(data, "a.b.c")
        1
        >>> extract_nested_value(data, "a.b.d", "default")
        'default'
    
    Args:
        data: 字典
        path: 路徑，使用點分隔（如 "a.b.c"）
        default: 默認值
        
    Returns:
        提取的值或默認值
    """
    keys = path.split(".")
    current = data
    
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
            if current is None:
                return default
        else:
            return default
    
    return current


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    安全地獲取字典值
    
    Args:
        data: 字典
        key: 鍵名
        default: 默認值
        
    Returns:
        值或默認值
    """
    if not isinstance(data, dict):
        return default
    
    return data.get(key, default)


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    合併多個字典
    
    後面的字典會覆蓋前面的重複鍵
    
    Args:
        dicts: 要合併的字典
        
    Returns:
        合併後的字典
    """
    result = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result

