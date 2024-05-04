from sanic import Sanic
from src.restful.detector import bp as detector_bp

app = Sanic("controller_root")
app.blueprint(detector_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, workers=1, auto_reload=False, debug=True)
