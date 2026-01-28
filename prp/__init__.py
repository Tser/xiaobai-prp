"""Python Registry Provider (PRP) - A tool for managing Python package index sources."""

__version__ = '1.0.0'


default_config = {
    "registries": {
        "pypi": {
            "url": "https://pypi.org/simple/",
            "home": "https://pypi.org",
            "name": "pypi"
        },
        "tuna": {
            "url": "https://pypi.tuna.tsinghua.edu.cn/simple/",
            "home": "https://pypi.tuna.tsinghua.edu.cn",
            "name": "tuna"
        },
        "aliyun": {
            "url": "https://mirrors.aliyun.com/pypi/simple/",
            "home": "https://mirrors.aliyun.com",
            "name": "aliyun"
        },
        "douban": {
            "url": "https://pypi.douban.com/simple/",
            "home": "https://pypi.douban.com",
            "name": "douban"
        },
        "huawei": {
            "url": "https://mirrors.huaweicloud.com/repository/pypi/simple/",
            "home": "https://mirrors.huaweicloud.com/",
            "name": "huawei"
        },
        "ustc": {
            "url": "https://pypi.mirrors.ustc.edu.cn/simple/",
            "home": "https://mirrors.ustc.edu.cn/",
            "name": "ustc"
        }
    },
    "current_registry": "pypi"
}

s = 'https://pypi.mirrors.ustc.edu.cn/'
# 获取s在default_config中对应的name称
r = list(filter(lambda x: default_config['registries'][x]['url'] == s, default_config['registries'].keys()))
print(r)
