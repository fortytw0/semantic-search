build_api_docker: 
	# Building Docker 
	docker build -f src/api_endpoint/Dockerfile  -t fortytw0/api_endpoint:latest src/api_endpoint/ 
	docker push fortytw0/api_endpoint:latest
