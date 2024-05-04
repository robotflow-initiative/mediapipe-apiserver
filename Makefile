.PHONY: all
all:
	@echo "nothing to do"

.PHONY: playground.test_local_camera
playground.test_local_camera:
	python playground/test_local_camera.py

.PHONY: playground.test_websocket_server
playground.test_websocket_server:
	python playground/test_websocket_server.py