
import sys
sys.path.append('./')
from src.restful import controller_app

if __name__ == "__main__":
    controller_app.run(host="0.0.0.0", port=3000, workers=1, auto_reload=False, debug=True)

    # 
    # ```shell
    # wscat -c http://127.0.0.1:3000/v1/detector/dummy
    # ```