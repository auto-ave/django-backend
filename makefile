all: start_db activate 

start_db:
	sudo /etc/init.d/postgresql restart
activate:
	source venv/bin/activate
freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt