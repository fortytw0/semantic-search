build_api_docker: 
	# Building Docker 
	docker build -f src/api_endpoint/Dockerfile  -t fortytw0/api_endpoint:latest src/api_endpoint/ 
	docker push fortytw0/api_endpoint:latest

deploy_api_endpoint:
	# Deploying api_endpoint on Kubernetes
	kubectl apply -f src/api_endpoint/deployments/storageclass.yaml
	kubectl apply -f src/api_endpoint/deployments/pv.yaml 
	kubectl apply -f src/api_endpoint/deployments/pvc.yaml 
	kubectl apply -f src/api_endpoint/deployments/deployment.yaml
	kubectl apply -f src/api_endpoint/deployments/service.yaml

retire_api_endpoint: 
	kubectl delete storageclass local-storage
	kubectl delete pvc api-endpoint-pvc
	kubectl delete pv api-endpoint-pv
	kubectl delete deployment.apps/api-endpoint 
	kubectl delete service/api-endpoint-service 


# kubectl get pvc api-endpoint-pvc 
