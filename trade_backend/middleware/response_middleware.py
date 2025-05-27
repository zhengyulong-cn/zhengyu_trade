from flask import jsonify
import json


def response_middleware(response):
    wrapper_response = {
        "code": response.status_code,
        "success": 200 <= response.status_code < 300,
        "data": None,
    }

    try:
        if response.is_json:
            wrapper_response["data"] = response.get_json()
        elif response.response:
            if (
                isinstance(response.response, (list, tuple))
                and len(response.response) > 0
            ):
                # 处理字节类型的响应数据
                try:
                    data = json.loads(response.response[0].decode())
                    wrapper_response["data"] = data
                except (json.JSONDecodeError, UnicodeDecodeError):
                    wrapper_response["data"] = response.response[0].decode()
            else:
                wrapper_response["data"] = response.response
    except Exception as e:
        wrapper_response["success"] = False
        wrapper_response["message"] = str(e)

    return jsonify(wrapper_response)
