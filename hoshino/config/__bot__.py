"""
----------------请阅读注释!!!!
--------------请阅读注释!!!!!!
-----------请阅读注释!!!!!!!!!
"""
###################################
'''---hoshino监听的端口与ip-----'''
PORT = 9222  # 本条请保持默认
HOST = '0.0.0.0'      # 本条请保持默认,本地部署使用此条配置（QQ客户端和bot端运行在同一台计算机）
# HOST = '0.0.0.0'      # 开放公网访问使用此条配置（不安全）
###################################
DEBUG = False           # 调试模式,不建议开启
###################################
'''---拥有最高权限的用户们的QQ---'''
SUPERUSERS = [512631235]    # 填写超级用户的QQ号，可填多个用半角逗号","隔开
PYS = {512631235}  # 高级权限用户的QQ号
###################################
'''---------昵称及网址----------'''
NICKNAME = r'柏崎栞|栞栞|栞|at,qq=2593047474'           # 设置bot的昵称，at，qq=xxxxxxxx处为bot的QQ号,呼叫昵称等同@bot,推荐修改
IP = '106.55.239.63'  # 修改为你的服务器ip,推荐修改
public_address = '106.55.239.63:9222'  # 修改为你的服务器ip+端口,推荐修改
###################################
'''
-----上方内容请务必结合注释修改-----
-----下面的内容请按需求修改---------
'''
###################################

'''
-------------apikeys---------------
lolicon_api,相关插件shebot/shebot_old,申请地址https://api.lolicon.app/#/setu?id=apikey
acggov_api,相关插件acggov,setuacggov,申请地址https://www.acg-gov.com/
shitu_api,相关插件shitu,申请地址http://saucenao.com/
jjc_api,相关插件arena,申请地址https://www.pcrdfans.com/bot
tenxun_api,相关插件aichat,申请地址https://ai.qq.com/,已经为你默认准备了一个,但建议自行申请进行个性定制
'''
lolicon_api = ''
acggov_api = ''
shitu_api = ''
jjc_api = ""
tenxun_api_ID = '1257426674'
tenxun_api_KEY = 'A6kETv96oHTN0OXOyHn0yfiYCdorjLip'
baidu_api = ''
###################################
'''-----------pixiv账号----------'''
pixiv_id = 'zw531129@outlook.com'  # pixiv账号,无需会员
pixiv_password = 'W@lsh4Hw'  # pixiv账号对应的密码
###################################
'''-------本部分建议不要改动-------'''
IMAGE_PATH = "../miraiGO/data/images"  # MiraiGO用这条,保持默认即可
COMMAND_START = {''}    # 命令前缀（空字符串匹配任何消息）
COMMAND_SEP = set()     # 命令分隔符（hoshino不需要该特性，保持为set()即可）

# 发送图片的协议
# 可选 http, file, base64
# 当QQ客户端与bot端不在同一台计算机时，可用http协议
RES_PROTOCOL = 'file'
# 资源库文件夹，需可读可写，windows下注意反斜杠转义
RES_DIR = "../res/"
# 使用http协议时需填写，原则上该url应指向RES_DIR目录
RES_URL = 'http://127.0.0.1:5000/static/'
###################################
'''
插件开关
初次尝试部署时请先保持默认
如欲启用新模块，请认真阅读部署说明，逐个启用逐个配置
切忌一次性开启多个
'''
###################################
MODULES_ON = {
    # hoshino基础功能
    'botmanage',    # hoshino基础功能
    'groupmaster',  # 群聊基础功能
    'setu_mix', # 俩涩图插件合二为一
    # 'epixiv', # 需要pixiv站账号
    'dice',     # 骰子
    'priconne',     # 抽卡/竞技场之类的集合
    'hourcallyao',  # 猜语音
    'voiceguess',
    'hiumsentences',  # 网抑云语录
    'generator',  # 营销文生成等五个小功能
    'russian',  # 俄罗斯轮盘赌
    'pcravatarguess',  # 图片猜角色
    'pcrdescguess',  # 通过角色描述猜角色,需要设置go-cqhttp的心跳间隔,推荐3
    'calendar',  # 查看日程表,实用的全服务器可用的功能
    'pcrmiddaymusic',  # 公主连结午间音乐
    'image_generate',  # 取代原image
    'music',  # 点歌插件
    'pcrmemorygames',  # 公主连结记忆小游戏
    'eclanblack',  # 兰德索尔黑名单
    'memberguess',  # 猜群友头像
    'anticoncurrency',  # 反并发插件
    'portune',  # 运势插件
    'nowtime',  # 发送"报时"有惊喜
    'reload',  # 重启，暂时不知是否能生效
    #　'pokemanpcr',#戳一戳卡片小游戏
    # 'pages',#bot网页端
    # 'clanbattle_rank',#会战排名查询插件
    # 'clanbattle_info',#自动报刀插件,开启前请按说明配置,难度较高
    # 'nbnhhsh',#将抽象短语转化为好好说话
    # 'eqa',#问答功能2
    # 'hourcall',#报时功能
    # 'kancolle',#舰娘的远征
    # 'mikan',#蜜柑订阅番剧
    # 'pcrclanbattle',#hoshinobot自带尚待完善
    # 'setu',#原生色图功能
    # 'translate',#原生翻译功能
    # 'twitter',#推特订阅，需要配置本目录下的twitter.py
    # 'yobot',#yobot会战功能
    # 'reload',#重启，暂时不知是否能生效
    # 'tarot',#塔罗牌
    # 'flac',#搜无损音乐
    # 'shitu',#识图功能需要apikey
    # 'shifan',#识别番剧
    # 'battle_report',#会战报告生成，需要修改路径
    # 'bot_manager_web',#新版webmanage
    # 'eclanrank',
    # 'aichat',#需要apikey，用前修改概率
    # 'QA',#问答功能,下方有集成优化版
    # 'ontree_scheduler',#挂树优化提醒
    # 'explosion',#每天一发惠惠
    # 'boxcolle',#BOX查询
    # 'timeline',#轴上传
    # 'picapi',#自定义拉取图片
    # 'aircon',#群空调
    # 'bilisearchspider',#b站订阅
    # 'shebot',##集合了许多插件,请勿和shebot及QA同时开启
    # 'nmsl',#抽象抽象抽抽抽像像像
    # 'baidupan',#百度盘解析
    # 'pcrsealkiller',#海豹杀手
    # 'setu_mix',#俩涩图插件合二为一
    # 'hoshino_training',#慎重启用,前往https://github.com/zyujs/hoshino_training查看说明
    # 'rss',#适用于Hoshino v2的rss订阅插件,详情https://github.com/zyujs/rss
    # 'Genshin_Impact',#原神系列
    # 'emergeface',#换脸插件,需要apikey
}
