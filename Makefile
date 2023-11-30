
docker: 
	cd ../.. ; docker build -t eopti/text_service -f ./services/text_service/Dockerfile ./

webdock_push:
	docker image tag eopti/text_service $(DOCKERHUB)/eopti/text_service
	docker push $(DOCKERHUB)/eopti/text_service
