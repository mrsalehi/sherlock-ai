import argparse
import yaml
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# def _flatten_config(d, parent_key='', sep='.'):
#     """
#     Utility function to flatten a nested dict.
#     Flatten the configuration: Convert your nested/hierarchical configuration into a flat structure, 
#     e.g., from { 'model': { 'name': 'test' } } to { 'model.name': 'test' }. 
#     """
#     items = {}
#     for k, v in d.items():
#         new_key = f"{parent_key}{sep}{k}" if parent_key else k
#         if isinstance(v, dict):
#             items.update(_flatten_config(v, new_key, sep=sep))
#         else:
#             items[new_key] = v
#     return items

def update_nested_dict(d, keys, value):
    """Update the nested dictionary `d` by setting `value` at the given `keys`."""
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value


def read_config_from_yaml(file_path):
    with open(file_path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            logger.error(exc)


def dict_to_namespace(d):
    """Converts a nested dictionary into a nested Namespace."""
    namespace = argparse.Namespace()
    for key, value in d.items():
        if isinstance(value, dict):
            setattr(namespace, key, dict_to_namespace(value))
        else:
            setattr(namespace, key, value)
    return namespace


def override_config_with_parsed_args(config, parsed_args):
    for key, value in vars(parsed_args).items():
        if value is not None:
            keys = key.split('.')
            update_nested_dict(config, keys, value)

    return dict_to_namespace(config)


def read_env_var(var_name):
    """Read environment variable."""
    try:
        return os.environ[var_name]
    except KeyError:
        logger.error(f"Environment variable {var_name} not set.")
        raise