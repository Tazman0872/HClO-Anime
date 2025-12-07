"""
Utility functions for the Config Manager module.
"""

import yaml
from pathlib import Path
from typing import Dict, Any


def create_default_config() -> Dict[str, Any]:
    """
    Create a default configuration dictionary.
    
    Returns:
        dict: Default configuration
    """
    # Try to load from default_config.yaml in the same directory
    default_config_path = Path(__file__).parent / "default_config.yaml"
    
    if default_config_path.exists():
        try:
            with open(default_config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file) or {}
        except Exception:
            # If YAML file is invalid, return basic default
            return None
    

def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration structure.
    
    Args:
        config (dict): Configuration to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Basic validation - you can customize this based on your needs
    required_keys = ['app', 'database', 'server']
    return all(key in config for key in required_keys)


def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two configuration dictionaries.
    
    Args:
        base_config (dict): Base configuration
        override_config (dict): Configuration to merge in
        
    Returns:
        dict: Merged configuration
    """
    def deep_merge(base: Dict, override: Dict) -> Dict:
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                deep_merge(base[key], value)
            else:
                base[key] = value
        return base
    
    import copy
    result = copy.deepcopy(base_config)
    deep_merge(result, override_config)
    return result


def get_nested_value(config: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    Get a nested value from configuration using dot notation.
    
    Args:
        config (dict): Configuration dictionary
        key_path (str): Dot-separated key path (e.g., 'database.host')
        default (Any): Default value if path doesn't exist
        
    Returns:
        Any: Value at the specified path or default
    """
    keys = key_path.split('.')
    value = config
    
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default


def set_nested_value(config: Dict[str, Any], key_path: str, value: Any) -> None:
    """
    Set a nested value in configuration using dot notation.
    
    Args:
        config (dict): Configuration dictionary to modify
        key_path (str): Dot-separated key path (e.g., 'database.host')
        value (Any): Value to set
    """
    keys = key_path.split('.')
    current = config
    
    # Navigate to the parent of the target key
    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    
    # Set the final value
    current[keys[-1]] = value