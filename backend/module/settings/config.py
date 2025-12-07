"""
Configuration Manager module for handling YAML configuration files.

This module provides a ConfigManager class that can read, write, and manage
YAML configuration files with automatic creation of default files.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Union
import logging

from .utils import create_default_config

logger = logging.getLogger(__name__)


class configManager:
    """
    A class to manage YAML configuration files.
    
    Features:
    - Load configuration from YAML file
    - Save configuration to YAML file
    - Create default configuration if file doesn't exist
    - Get and set configuration values using dot notation
    """
    
    def __init__(self, config_path: Union[str, Path], default_config: Optional[Dict] = None):
        """
        Initialize the ConfigManager.
        
        Args:
            config_path (str or Path): Path to the configuration file
            default_config (dict, optional): Default configuration dictionary
        """
        self.config_path = Path(config_path)
        self.default_config = default_config or {}
        
        # Load or create the configuration
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or create default if file doesn't exist.
        
        Returns:
            dict: The loaded configuration
        """
        if not self.config_path.exists():
            logger.info(f"Configuration file does not exist: {self.config_path}")
            logger.info("Creating default configuration file...")
            
            # Create directory if it doesn't exist
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Use provided default config or create from default file
            if self.default_config:
                config = self.default_config
            else:
                config = create_default_config()
            
            self._save_config(config)
            logger.info(f"Default configuration created at: {self.config_path}")
            return config
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file) or {}
            logger.info(f"Configuration loaded from: {self.config_path}")
            return config
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading configuration file: {e}")
            raise
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """
        Save configuration to file.
        
        Args:
            config (dict): Configuration dictionary to save
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as file:
                yaml.dump(config, file, default_flow_style=False, allow_unicode=True, indent=2)
            logger.info(f"Configuration saved to: {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving configuration file: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key (str): Configuration key (e.g., 'database.host')
            default (Any): Default value if key doesn't exist
            
        Returns:
            Any: Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value using dot notation.
        
        Args:
            key (str): Configuration key (e.g., 'database.host')
            value (Any): Value to set
        """
        keys = key.split('.')
        config = self._config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        # Set the final value
        config[keys[-1]] = value
    
    def update(self, new_config: Dict[str, Any]) -> None:
        """
        Update the configuration with new values.
        
        Args:
            new_config (dict): New configuration values to merge
        """
        def deep_merge(base: Dict, update: Dict) -> Dict:
            """Deep merge two dictionaries."""
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value
            return base
        
        deep_merge(self._config, new_config)
    
    def save(self) -> None:
        """Save the current configuration to file."""
        self._save_config(self._config)
    
    def reload(self) -> None:
        """Reload the configuration from file."""
        self._config = self._load_config()
    
    def reset_to_default(self) -> None:
        """Reset configuration to default values."""
        if self.default_config:
            self._config = self.default_config.copy()
        else:
            self._config = create_default_config()
        self.save()
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get the current configuration dictionary."""
        return self._config.copy()
    
    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access."""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Allow dictionary-style assignment."""
        self.set(key, value)
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists in configuration."""
        return self.get(key) is not None


# Example usage and testing
if __name__ == "__main__":
    # Example usage
    import tempfile
    
    # Create a temporary config file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        temp_config_path = f.name
    
    try:
        # Initialize config manager
        config = configManager(temp_config_path)
        
        # Set some values
        config.set('database.host', 'localhost')
        config.set('database.port', 5432)
        config.set('database.name', 'myapp')
        config.set('app.debug', True)
        config.set('app.name', 'My Application')
        
        # Get values
        print("Database host:", config.get('database.host'))
        print("App name:", config.get('app.name'))
        print("App debug:", config.get('app.debug'))
        
        # Dictionary-style access
        config['server.host'] = '0.0.0.0'
        config['server.port'] = 8000
        print("Server host:", config['server.host'])
        
        # Save configuration
        config.save()
        
        # Reload and verify
        config.reload()
        print("Reloaded server port:", config.get('server.port'))
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_config_path):
            os.remove(temp_config_path)