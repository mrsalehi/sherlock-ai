## Testing Sherlock
Sherlock is tested using `pytest`. To run the tests, run the following command:
```bash
pytest -s tests/<TEST_FILE>::<TEST_FUNCTION>
```
replace <TEST_FILE> with the name of the Python file and <TEST_FUNCTION> with the name of the test function. For example:
```bash
pytest -s tests/test_config.py::test_override_config_with_parsed_args
```