'''
@FileName   :md5加密.py
@Description:
@Date       :2024/04/13 16:44:16
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
import hashlib


def encrypt(param):
    print(param)
    # obj_encrypt = hashlib.md5()#没有加盐，不安全
    obj_encrypt = hashlib.md5("daito_md5".encode('utf-8'))  # 加盐
    obj_encrypt.update(data_str.encode('utf-8'))
    ret = obj_encrypt.hexdigest()
    return ret


data_str = input("输入明文：")
ret = encrypt(data_str)
obj_file = open("md5.txt", mode='a', encoding='utf-8')
obj_file.write(f"明文：{data_str}\n")
obj_file.write(f"密文：{ret}\n")
obj_file.close()
print(ret)
