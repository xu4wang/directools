import configparser

config_file_path = "./config.ini"

def read_config_file(file_path):
    # 创建配置解析器对象
    config = configparser.ConfigParser()

    # 读取配置文件
    try:
        config.read(file_path)
    except configparser.Error:
        # 配置文件不存在或格式不正确时，返回默认配置
        return get_default_config()

    # 获取特定配置项的值
    directus_url = config.get("directus", "url", fallback="http://localhost:8055")
    directus_token = config.get("directus", "token", fallback="MISSING ADMIN TOKEN in config.ini!")
    folder = config.get("system", "folder", fallback="./")

    # 检查配置项是否为空，如果为空则返回默认配置
    if not directus_url or not directus_token:
        return get_default_config()

    # 创建一个字典来存储配置项的值
    config_data = {
        "directus": {
            "url": directus_url,
            "token": directus_token,
        },
        "system": {
            "folder": folder,
        }
    }

    return config_data

def get_default_config():
    # 默认配置
    return {
        "directus": {
            "url": "http://localhost:8055",
            "token": "GNuG2xodzTMY19AaYh0r7yYNWSqWF-AE",
        },
        "system": {
            "folder": "./",
        }
    }

def get_config():
    return read_config_file(config_file_path)
