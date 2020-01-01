qq群聊天图片自动鉴黄
---
![lJoEGD.jpg](https://s2.ax1x.com/2020/01/02/lJoEGD.jpg)
### 部署
1. 在[腾讯ai开放平台](https://ai.qq.com/product/yellow.shtml)注册账号
2. 安装[酷q机器人](https://cqp.cc/) 推荐使用pro版, pro版可以撤回消息
3. 安装[cqhttp插件](https://cqp.cc/t/30748) 可能需要安装[VC++ 2017运行库](https://aka.ms/vs/15/release/VC_redist.x86.exe)
4. 配置cqhttp, 记录其host和port
5. git clone此项目, 根据config文件修改配置
6. 使用
```shell
python main.py
```
运行项目

### 配置说明
```python
bot_host = "127.0.0.1"  # 机器人host
bot_port = "8080"  # 机器人port
qq_group = [123456, 987654]  # 生效群
compress_kb = 500  # 压缩图片大小, 单位为kb
bot_img_file_dir = r"C:\酷Q Pro\data\image"  # 酷q机器人接收图片位置, 如图位置

APP_ID = 123456  # 从tx云获取的api
APP_KEY = 'jlKkjKOWtEogd'

# 规则
rules = RuleBuilder()\
    .add(RuleBuilder.TAG_NORMAL_HOT_PORN, 90, 100, True, RuleBuilder.Punishment.kick(True))\
    .add(RuleBuilder.TAG_NORMAL_HOT_PORN, 80, 89, True, RuleBuilder.Punishment.ban(7*24*60*60))\
    .build()
```
规则说明:
类型 检测最小值 检测最大值 是否撤回 处理方式

RuleBuilder.TAG_NORMAL_HOT_PORN, 90, 100, True, RuleBuilder.Punishment.kick(True)

色情的综合值 满足 90 <= x <= 100 则 撤回消息 踢出本群且不能再申请

RuleBuilder.TAG_NORMAL_HOT_PORN, 80, 89, True, RuleBuilder.Punishment.ban(7*24*60*60)

色情的综合值 满足 80 <= x <= 89 则 撤回消息 进行禁言7天(单位为秒)

### 注
安装pillow模块可能会报错, 请去 [lfd.uci.edu](https://www.lfd.uci.edu/~gohlke/pythonlibs/) 下载第三方whl直接安装

善用 **ctrl+f**


