"""This scripts tests the availability of sanic server
"""
import sys
sys.path.append('./')
from mediapipe_apiserver.restful import controller_app

if __name__ == "__main__":
    controller_app.run(host="0.0.0.0", port=3000, single_process=True, auto_reload=False, debug=True)

    # 
    # ```shell
    # wscat -c http://127.0.0.1:3000/v1/detector/dummy
    # ```