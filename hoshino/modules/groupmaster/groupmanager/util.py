import hoshino
from hoshino import priv

from . import *

#获取指定群成员信息
async def group_member_info(bot, ev, gid, uid):
    try:
        gm_info = await bot.get_group_member_info(
            group_id = gid,
            user_id = uid,
            no_cache = True
        )
        return gm_info
    except Exception as e:
        hoshino.logger.exception(e)

#获取Bot的群信息
async def self_member_info(bot, ev, gid):
    for sid in hoshino.get_self_ids():
        self_id = sid
        try:
            gm_info = await bot.get_group_member_info(
                group_id = gid,
                user_id = self_id,
                no_cache = True
            )
            return gm_info
        except Exception as e:
            hoshino.logger.exception(e)

#群荣誉信息
async def honor_info(bot, ev, gid, honor_type):
    try:
        gh_info = await bot.get_group_honor_info(
            group_id = gid,
            type = honor_type
        )
        return gh_info
    except Exception as e:
        hoshino.logger.exception(e)

#全员禁言
async def gruop_silence(bot, ev, gid, status):
    self_info = await self_member_info(bot, ev, gid)
    if self_info['role'] != 'owner' and self_info['role'] != 'admin':
        await bot.send(ev, '\n不给我管理员还想让我帮忙塞口球？做梦去吧！', at_sender=True)
        return    
    if not priv.check_priv(ev,priv.ADMIN):
        await bot.send(ev, '只有狗管理才能给大家塞口球哦w', at_sender=True) 
    else:   
        try:
            await bot.set_group_whole_ban(
                    group_id = gid,
                    enable = status
                )
            if not status:
                await bot.send(ev, '全员禁言取消啦w')
            else:
                await bot.send(ev, '嘻嘻大家都被塞口球啦~')
        except Exception as e:
            await bot.send(ev, f'操作失败惹...\n错误代码：{e}', at_sender=True)

#单人禁言
async def member_silence(bot, ev, uid, sid, gid, time):
    self_info = await self_member_info(bot, ev, gid)
    if self_info['role'] != 'owner' and self_info['role'] != 'admin':
        await bot.send(ev, '\n不给我管理员还想让我帮忙塞口球？做梦去吧！', at_sender=True)
        return
    if not time.isdigit() and '*' not in time:
        await bot.send(ev, '憨批，时长都能输错？')
    else:
        if uid == sid or priv.check_priv(ev,priv.ADMIN):
            try:
                await bot.set_group_ban(
                    group_id = gid,
                    user_id = sid,
                    duration = eval(time)
                    )
                if time == '0':
                    await bot.send(ev, f'[CQ:at,qq={sid}]的口球已经摘下来啦w')
                else:
                    await bot.send(ev, f'成功禁言[CQ:at,qq={sid}]{eval(time)}秒~')

            except Exception as e:
                await bot.send(ev, '口球失败惹呜呜呜...\n错误代码：{e}', at_sender=True)
        elif uid != sid and not priv.check_priv(ev,priv.ADMIN):
            await bot.send(ev, '只有管理员才可以给别人塞口球哦~', at_sender=True)

#头衔申请
async def title_get(bot, ev, uid, sid, gid, title):
    self_info = await self_member_info(bot, ev, gid)
    if self_info['role'] != 'owner':
        await bot.send(ev, '\n嘻嘻嘻，把群转移给我才能用这个功能哦！\n我才不告诉你可以去qun.qq.com里找回群主权限呢！', at_sender=True)
        return
    if uid == sid or priv.check_priv(ev,priv.ADMIN):
        try:
            await bot.set_group_special_title(
                group_id = gid,
                user_id = sid,
                special_title = title,
                duration = -1
                )
            if not title:
                await bot.send(ev, f'祝贺[CQ:at,qq={sid}]喜提没有头衔的头衔~')
            else:
                await bot.send(ev, f'已为[CQ:at,qq={sid}]发放专属头衔“{title}”~')
        except Exception as e:
            await bot.send(ev, f'诶...头衔呢？\n错误代码：{e}', at_sender=True)
    elif uid != sid and not priv.check_priv(ev,priv.ADMIN):
        await bot.send(ev, '只有管理员才可以对别人的头衔进行操作哦~', at_sender=True)

#群组踢人
async def member_kick(bot, ev, uid, sid, gid, is_reject):
    self_info = await self_member_info(bot, ev, gid)
    if self_info['role'] != 'owner' and self_info['role'] != 'admin':
        await bot.send(ev, '\n傻批，不给我管理员我搁那踢空气呢？？？', at_sender=True)
        return
    if uid == sid or priv.check_priv(ev,priv.ADMIN):
        try:
            await bot.set_group_kick(
                group_id = gid,
                user_id = sid,
                reject_add_request = is_reject
            )
            await bot.send(ev, f'恭喜幸运用户[CQ:at,qq={sid}]喜提芜湖飞机票一张~')
        except Exception as e:
            await bot.send(ev, f'诶！！！为什么没踢成功！\n错误代码：{e}', at_sender=True)
    elif uid != sid and not priv.check_priv(ev,priv.ADMIN):
        await bot.send(ev, '只有狗管理才能送飞机票的说', at_sender=True)

#群名片修改
async def card_edit(bot, ev, uid, sid, gid, card_text):
    self_info = await self_member_info(bot, ev, gid)
    if self_info['role'] != 'owner' and self_info['role'] != 'admin':
        await bot.send(ev, '\n我日，不给我管理改锤子名片', at_sender=True)
    if uid == sid or priv.check_priv(ev,priv.ADMIN):
        try:
            await bot.set_group_card(
                group_id = gid,
                user_id = sid,
                card = card_text
            )
            await bot.send(ev, f'已经把[CQ:at,qq={sid}]的群名片修改为“{card_text}”啦~')
        except Exception as e:
            await bot.send(ev, f'修改群名片失败勒...\n错误代码：{e}', at_sender=True)
    elif uid != sid and not priv.check_priv(ev,priv.ADMIN):
        await bot.send(ev, '只有狗管理才能给别人设置名片了啦！', at_sender=True)

		

async def group_name(bot, ev, gid, name_text):
    self_info = await self_member_info(bot, ev, gid)
    if self_info['role'] != 'owner' and self_info['role'] != 'admin':
        await bot.send(ev, '\n我还没获得管理权限呢...', at_sender=True)
        return    
    if not priv.check_priv(ev,priv.ADMIN):
        await bot.send(ev, '只有狗管理才能修改群名哦！', at_sender=True) 
    else:   
        try:
            await bot.set_group_name(
			    group_id = gid,
			    name = name_text
			)
            await bot.send(ev, f'群名已修改为“{name_text}”啦')
        except Exception as e:
            await bot.send(ev, '群名修改失败惹...\n错误代码：{e}', at_sender=True)