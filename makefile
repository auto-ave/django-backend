freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt
activate:
	sudo /etc/init.d/postgresql restart && source venv/bin/activate
