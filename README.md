## 一个很水的补天上传漏洞的脚本
### 写在前面
因为之前的互联网守护活动，提交数百上千个太累了，就搞了这个项目

其实这个稍微麻烦的地方就在于贴图以及识别验证码(当然大佬们可能觉得没什么麻烦的)，

贴图的话，我提前把图片上传到补天，然后插入图片链接（上传图片见script/utils）

验证码的话，直接调用联众打码平台，文字点选的2分钱打一次

### 使用说明
建议在py3环境下食用

由于使用的selenium，需要下载chromedriver，直接在这里下载对应你chrome的版本就好
https://npm.taobao.org/mirrors/chromedriver

建议使用virtualvenv

pip install -r requirements.txt

然后修改config.py中的配置