"""
Configuration management for expert proverb sources.
"""
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

CONFIG_FILE = Path(__file__).parent / 'expert_sources.yaml'


def load_config() -> Dict[str, Any]:
    """Load the expert sources configuration file.
    
    Returns:
        Dictionary containing configuration for all expert sources
    """
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_source_config(source_name: str) -> Dict[str, Any]:
    """Get configuration for a specific expert source.
    
    Args:
        source_name: Identifier for the expert source (e.g., 'ireri')
        
    Returns:
        Dictionary containing configuration for the specified source
        
    Raises:
        ValueError: If source_name is not found in configuration
    """
    config = load_config()
    
    if source_name not in config.get('sources', {}):
        available = ', '.join(config.get('sources', {}).keys())
        raise ValueError(
            f"Unknown source '{source_name}'. "
            f"Available sources: {available}"
        )
    
    return config['sources'][source_name]


def get_default_config() -> Dict[str, Any]:
    """Get default configuration shared across all sources.
    
    Returns:
        Dictionary containing default configuration
    """
    config = load_config()
    return config.get('defaults', {})


def list_available_sources() -> list:
    """List all available expert sources.
    
    Returns:
        List of source identifiers
    """
    config = load_config()
    return list(config.get('sources', {}).keys())


def get_output_path(
    source_name: str, 
    output_type: str, 
    base_dir: Optional[str] = None
) -> Path:
    """Get output file path for a source and output type.
    
    Args:
        source_name: Expert source identifier
        output_type: Type of output ('raw_csv', 'gold_standard_csv', 
                     'metadata_json', 'report_md')
        base_dir: Optional base directory override
        
    Returns:
        Path object for the output file
    """
    source_config = get_source_config(source_name)
    defaults = get_default_config()
    
    # Get filename from source config
    filename = source_config['output'][output_type]
    
    # Determine directory based on output type
    if output_type == 'raw_csv':
        dir_key = 'raw'
    else:
        dir_key = 'evaluation'
    
    if base_dir:
        directory = Path(base_dir)
    else:
        directory = Path(defaults['output_directories'][dir_key])
    
    return directory / filename
