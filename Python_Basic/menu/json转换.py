'''
@FileName   :json.py
@Description:不同编程语言间数据交换格式--JSON(本质是字符串)
@Date       :2024/04/13 17:14:01
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
import json

data_dict = {"k1": 123, "k2": "daito", "k3": ["add", "substract"]}
data_str = json.dumps(data_dict)  # dict to json
# "{}"--nojson   '{}'--是json
# "{"k1":True}"--nojson   "{"k1":true}"--JSON
# "{"k1":(1,2,3)}"--nojson   "{"k1":[1,2,3]}"--JSON
print(type(data_str))
print(data_str)
