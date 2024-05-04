from sanic import Sanic
import sys
sys.path.append('./')
from src.restful.dummy import bp as dummpy_bp

app = Sanic("controller_root")
app.blueprint(dummpy_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, workers=1, auto_reload=False, debug=True)
