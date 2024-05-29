from sanic import Sanic
from mediapipe_apiserver.restful.detector import bp as detector_bp
from mediapipe_apiserver.restful.camera import bp as camera_bp
# sanic controller must created as global variable
app = Sanic("controller_root")

# register a blueprint to controller
app.blueprint(detector_bp)
app.blueprint(camera_bp)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, workers=1, auto_reload=False, debug=True)
