kill_guni:
	sudo ps aux | grep gunicorn | awk '{print $2}' | xargs sudo kill -9

reload:
	sudo ./bin/server.sh stop-dev
	sudo ./bin/database.sh setup-dev
	sudo ./bin/server.sh start-dev

reload_prod:
	sudo ./bin/server.sh stop-prod; sudo ./bin/server.sh start-prod
