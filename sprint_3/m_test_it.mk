target:
	python -m tests.test_type_request
	@ echo "\n"
	python -m tests.test_get_coverage
	@ echo "\n"
	python -m tests.test_dbc
	@ echo "\n"
	python -m tests.test_datacube
	@ echo "<Finished>"
