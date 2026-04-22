"""
Configuration Management for Agentic AI Performance Engineering
"""
import os
from typing import Dict, Any, Optional
import yaml
from pathlib import Path


class Config:
    """Configuration handler for the project"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to config.yaml file
        """
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__), 
                'config.yaml'
            )
        
        self.config_path = config_path
        self.config = self._load_config()
        self._load_env_variables()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Config file not found at {self.config_path}")
            return {}
    
    def _load_env_variables(self):
        """Load environment variables and override config"""
        from dotenv import load_dotenv
        load_dotenv()
        
        # LLM Configuration
        if os.getenv('LLM_MODEL'):
            self.config['llm']['model'] = os.getenv('LLM_MODEL')
        if os.getenv('OPENAI_API_KEY'):
            self.config['llm']['openai_api_key'] = os.getenv('OPENAI_API_KEY')
        if os.getenv('ANTHROPIC_API_KEY'):
            self.config['llm']['anthropic_api_key'] = os.getenv('ANTHROPIC_API_KEY')
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by key"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration"""
        return self.config


# Global configuration instance
_config_instance = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get or create global config instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance


def create_required_directories():
    """Create required project directories"""
    directories = [
        './data',
        './logs',
        './results',
        './results/reports',
        './results/recommendations',
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
