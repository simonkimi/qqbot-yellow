from bean import RuleBuilder

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