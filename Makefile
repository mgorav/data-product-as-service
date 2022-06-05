include .env
export

docker-build:
	docker build -t databricks-streamlit-demo .

docker-run: docker-build
	docker run -it -p 8052:8052 --env-file=.env databricks-streamlit-demo

debug-in-docker:
	pip install -e .
	PYTHONPATH=/workspaces/databricks-streamlit-demo
	streamlit run databricks_streamlit_demo/app.py \
		--server.port=8052 \
		--logger.level=debug \
		--logger.messageFormat="[%(asctime)s][%(levelname)s][%(name)s][%(funcName)s][%(message)s]"
