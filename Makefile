include .env
export

docker-build:
	docker build -t data_product_service .

docker-run: docker-build
	docker run -it -p 8052:8052 --env-file=.env data_product_service

debug-in-docker:
	pip install -e .
	PYTHONPATH=/workspaces/data_product_service
	streamlit run data_product_service/app.py \
		--server.port=8052 \
		--logger.level=debug \
		--logger.messageFormat="[%(asctime)s][%(levelname)s][%(name)s][%(funcName)s][%(message)s]"
