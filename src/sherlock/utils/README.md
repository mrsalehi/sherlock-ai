##Sherlock Configuration
Configuration in Sherlock is easy:

1. You can read the config from `yaml` files which are most likely located under `config/` directory. You can also create a config under `src/sherlock/**` if it's more conveneint for you. Use `read_config_from_yaml` function in `sherlock/utils/conf_utils.py` to load the config. This will result in a `dict` object. To convert the `dict` object to `Namespace` object, use `dict_to_namespace` function in `sherlock/utils/conf_utils.py`.

2. You can override the config with CLI arguments using `override_config_with_parsed_args` function in `sherlock/utils/conf_utils.py`. This will result in a `Namespace` object.

3. Will add support for environment variables soon. They are useful for setting sensitive information like API keys.