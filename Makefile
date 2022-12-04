build_api_docker: 
	# Building Docker 
	cd src/api_endpoint/ 
	docker build -t fortytw0/api_endpoint:latest . 
	docker push fortytw0/api_endpoint:latest
