.PHONY: all
all:
	@echo "nothing to do"

.PHONY: playground.test_local_camera
playground.test_local_camera:
	python playground/test_local_camera.py

.PHONY: playground.test_websocket_server
playground.test_websocket_server:
	python playground/test_websocket_server.py

.PHONY: playground.test_ws_client
playground.test_ws_client:
	python playground/test_ws_client.py

.PHONE: serve
serve:
	python -m src --port 3000

.PHONE: debug_serve
debug_serve:
	python -m src --port 3000 --debug