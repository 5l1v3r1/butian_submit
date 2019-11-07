# 修复建议
REPAIR = {
    "SQL": "使用预编译的SQL语句",
    "DMZX": "过滤用户不安全的输入",
    "OTHER": "过滤用户不安全的输入",
}

# 漏洞类型
CLASS_MAPPING = {
    "XSS": 1,
    "配置错误": 2,
    "弱口令": 3,
    "入侵事件": 4,
    "疑似被黑": 5,
    "文件上传": 6,
    "信息泄漏": 7,
    "存在后门": 8,
    "逻辑漏洞": 9,
    "代码执行": 10,
    "命令执行": 11,
    "SQL注入": 12,
    "解析漏洞": 13,
}

# 描述前缀
PRE_FLAG = "【互联网安全守护计划】"


# 联众打码平台配置
LZ_USERNAME = '你的用户名'
LZ_PASSWORD = '你的密码'
LZ_API = "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload"
LZ_CAPTCHA_TYPE = "1303"
LZ_TOKEN = "你的token"

# 补天的cookie设置
phpsessid = "Cookie中 phpsession 的值"
btlc_name = "Cookie中 btlc对应的键值对的key"
btlc_value = "Cookie中 btlc对应的键值对的value"
butian_cookie = "补天的Cookie"
