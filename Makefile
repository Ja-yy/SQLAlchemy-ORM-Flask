up:
	docker-compose up -d --build --force-recreate

down:
	docker-compose down -v --rmi local
