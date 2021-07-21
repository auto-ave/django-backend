freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt
activate:
	source venv/bin/activate
