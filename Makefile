.PHONE: generate-hashes
generate-hashes:
	pip install pip-tools
	pip-compile --generate-hashes ./requirements.in --output-file ./requirements.txt --allow-unsafe