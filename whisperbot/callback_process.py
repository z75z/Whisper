from whisperbot.keyboards_func import *
from whisperbot.lateral_func import *
from whisperbot.main_func import *
from config_bot import *
from core_file import *


async def callback_query_process(msg: types.CallbackQuery):
    saveUsername(msg, mode="callback")
    user_id = msg.from_user.id
    if msg.from_user.username:
        username = msg.from_user.username
    else:
        username = ""
    input = msg.data.lower()
    setupUserSteps(msg, user_id)
    langU = lang[lang_user(user_id)]
    buttuns = langU["buttuns"]
    if "message" in msg:
        msg_id = msg.message.message_id
    else:
        msg_id = 0
    if "message" in msg and "reply_to_message" in msg.message:
        reply_msg = msg.message.reply_to_message
        reply_id = reply_msg.message_id
    else:
        reply_msg = None
        reply_id = 0
    print(colored("Callback >", "cyan"))
    print(colored("userID", "yellow"), colored(user_id, "white"))
    print(colored("Query", "yellow"), colored(input, "white"))
    print(colored("queryID", "yellow"), colored(msg.id, "white"))
    print()
    # if re.search(r"@(\d+)", input):
    # ap = re_matches("@(\d+)", input, 's')
    # if int(ap[1]) != user_id:
    # if not DataBase.get('user.alertinline:{}:{}'.format(user_id, msg_id)):
    # DataBase.setex('user.alertinline:{}:{}'.format(user_id, msg_id), 3600, "True")
    # return AnswerCallbackQuery(msg.id, langU['isNot4u'], True, None, 3600)
    # return False
    # if int(ap[1]) == user_id and not DataBase.get('user.alertNotMemberChannel:{}'.format(user_id)):
    # if not re.search(r'insgp(.*)', input) and not re.search(r'ib(.*)', input) and not await is_Channel_Member("@{}".format(IDs_datas['chUsername']), user_id):
    # DataBase.set('user.alertNotMemberChannel2:{}'.format(user_id), "True")
    # await answerCallbackQuery(msg, langU['uNotJoined'].format(IDs_datas['chUsername']), True)
    # inlineKeys = iMarkup()
    # inlineKeys.add = (
    # iButtun(langU['buttuns']['join'], url = 'https://t.me/{}'.format(IDs_datas['chUsername'])),
    # iButtun(langU['buttuns']['joined'], callback_data = input)
    # )
    # await editText(chat_id, msg_id, 1, langU['join_channel'].format(IDs_datas['chUsername']), 'md', inlineKeys)
    # return False
    # if DataBase.get('user.alertNotMemberChannel2:{}'.format(user_id)):
    # DataBase.delete('user.alertNotMemberChannel2:{}'.format(user_id))
    # await answerCallbackQuery(msg, langU['you_accepted'])
    # DataBase.setex('user.alertNotMemberChannel:{}'.format(user_id), 3600, "True")
    if "message" in msg:
        _ = msg.message
        msg_id = _.message_id
        chat_id = _.chat.id
        chat_name = _.chat.title
        if not rds.get(input):
            rds.psetex(input, 500, 1)
        else:
            return False
        if int(_.date.timestamp()) < (int(time()) - 86400):
            cPrint(
                "{} Old Callback Skipped".format(_.date), 2, textColor="cyan"
            )
            return False
        if re.match(r"^joined$", input):
            chId = GlobalValues().chId
            channel_member = await is_Channel_Member(chId, user_id)
            force_join = DataBase.get("force_join")
            if force_join and chId != 0 and not channel_member:
                DataBase.setex(f"join_alarm:{user_id}", 120, "True")
                inlineKeys = iMarkup()
                inlineKeys.add(
                    iButtun(
                        langU["buttuns"]["join"],
                        url=IDs_datas["chLink"],
                    ),
                    iButtun(
                        langU["buttuns"]["joined"],
                        callback_data="joined",
                    ),
                )
                return await answerCallbackQuery(
                    msg,
                    langU["uNotJoined"].format(IDs_datas['chUsername']),
                    show_alert=True,
                    cache_time=5,
                )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["start"].format(GlobalValues().botName),
                "html",
                start_keys(user_id),
            )
        if re.match(r"^forcejoin$", input):
            if DataBase.get("force_join"):
                DataBase.delete("force_join")
                text = langU["force_join_deactive"]
            else:
                DataBase.set("force_join", "True")
                text = langU["force_join_active"]
            await answerCallbackQuery(
                msg,
                text,
                show_alert=True,
                cache_time=2,
            )
            await editMessageReplyMarkup(
                chat_id,
                msg_id,
                reply_markup=start_keys(user_id),
            )
        if re.match(r"^backstart:@(\d+)$", input):
            DataBase.delete("sup:{}".format(user_id))
            DataBase.delete("ready_to_change_link:{}".format(user_id))
            DataBase.delete("ready_to_change_name:{}".format(user_id))
            DataBase.delete("ready_to_enter_id:{}".format(user_id))
            DataBase.delete("ready_to_recv_special:{}".format(user_id))
            DataBase.delete("who_conneted:{}".format(user_id))
            user_steps[user_id].update({"action": "nothing"})
            await editText(
                chat_id,
                msg_id,
                0,
                langU["start"].format(GlobalValues().botName),
                "html",
                start_keys(user_id),
            )
        if re.match(r"^supp:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                langU["support2"],
                "html",
                support_keys(user_id),
            )
        if re.match(r"^support:@(\d+)$", input):
            user_steps[user_id].update({"action": "support"})
            await sendText(
                GlobalValues().supchat,
                0,
                1,
                lang[lang_user(GlobalValues().sudoID)]["connected_support"].format(menMD(msg)),
                "md",
            )
            inlineKeys = iMarkup()
            inlineKeys.add(
                iButtun(
                    buttuns["disconnect"],
                    callback_data="backstart:@{}".format(user_id),
                )
            )
            await editText(
                chat_id, msg_id, 0, langU["support"], "html", inlineKeys
            )
        if re.match(r"^from_who:(\d+):(\d+)$", input):
            ap = re_matches(r"^from_who:(\d+):(\d+)$", input)
            name_user = await userInfos(ap[1], "name")
            await answerCallbackQuery(
                msg,
                langU["message_from"].format(name_user),
                show_alert=True,
                cache_time=86400,
            )
        if re.match(r"^language:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                langU["language"],
                None,
                settings_keys(user_id),
            )
        if re.match(r"^adsfree:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                langU["adsfree"].format(GlobalValues().linkyCH),
                "html",
                back_keys(user_id),
            )
        if re.match(r"^set_(.*)_(.*):@(\d+)$", input):
            ap = re_matches("^set_(.*)_(.*):@(\d+)$", input)
            if ap[1] == "lang":
                if ap[2] == "de":
                    return AnswerCallbackQuery(
                        msg.id, lang["set_{}".format(ap[2])], True, None, 0
                    )
                DataBase.set("user.lang:{}".format(user_id), ap[2])
                if user_id in user_steps:
                    user_steps[user_id].update(
                        {
                            "lang": ap[2],
                        }
                    )
                else:
                    setupUserSteps(msg, user_id)
                try:
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        lang[ap[2]]["language"],
                        None,
                        settings_keys(user_id, ap[2]),
                    )
                except:
                    await _.edit_reply_markup(settings_keys(user_id, ap[2]))
                return AnswerCallbackQuery(
                    msg.id, lang["set_{}".format(ap[2])], True, None, 0
                )
        if re.match(r"^notice_1:@(\d+)$", input):
            return AnswerCallbackQuery(
                msg.id, langU["notice_change_file"], True, None, 86400
            )
        if re.match(r"^start_again:@(\d+)$", input):
            DataBase.delete("sup:{}".format(user_id))
            user_steps[user_id].update({"action": "nothing"})
            try:
                await _.edit_reply_markup()
            except:
                pass
            await sendText(
                chat_id, 0, 1, langU["start"], None, start_keys(user_id)
            )
        if re.match(r"^blockuser:(\d+)$", input):
            ap = re_matches("^blockuser:(\d+)$", input)
            if DataBase.get("isBan:{}".format(ap[1])):
                alerttext = langU["usblocked"]
            else:
                DataBase.set("isBan:{}".format(ap[1]), "True")
                alerttext = langU["usblock"]
                keyboard = blockKeys(ap[1])
                try:
                    getC = await userInfos(ap[1], info="name")
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        "#NewUser\n<a href=\"tg://user?id={1}\">{0}</a> > <code>{1}</code>\nStatus: Deactive🚫".format(
                            getC, ap[1]
                        ),
                        "html",
                        keyboard,
                    )
                except:
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        "#NewUser\n<a href=\"tg://user?id={0}\">{0}</a> > <code>{0}</code>\nStatus: Deactive🚫".format(
                            ap[1]
                        ),
                        "html",
                        keyboard,
                    )
            await answerCallbackQuery(msg, alerttext)
        if re.match(r"^unblockuser:(\d+)$", input):
            ap = re_matches("^unblockuser:(\d+)$", input)
            if DataBase.get("isBan:{}".format(ap[1])):
                DataBase.delete("isBan:{}".format(ap[1]))
                alerttext = langU["usunblocked"]
                keyboard = blockKeys(ap[1])
                try:
                    getC = await userInfos(ap[1], info="name")
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        "#NewUser\n<a href=\"tg://user?id={1}\">{0}</a> > <code>{1}</code>\nStatus: Active✅".format(
                            getC, ap[1]
                        ),
                        "html",
                        keyboard,
                    )
                except:
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        "#NewUser\n<a href=\"tg://user?id={0}\">{0}</a> > <code>{0}</code>\nStatus: Active✅".format(
                            ap[1]
                        ),
                        "html",
                        keyboard,
                    )
            else:
                alerttext = langU["usunblock"]
            await answerCallbackQuery(msg, alerttext)
        if re.match(r"^list:(.*):(\d+):@(\d+)$", input):
            ap = re_matches("^list:(.*):(\d+):@(\d+)$", input)
            inlineKeys = iMarkup()
            if ap[1] == "block":
                await editText(chat_id, msg_id, 0, langU["wait"])
                text = langU["list_block"]
                keys = DataBase.smembers("isBanned")
                n = int(ap[2])
                for i in keys:
                    n += 1
                    userID = i
                    text = "{}{}- {} | {}\n".format(
                        text,
                        n,
                        await userInfos(userID),
                        userID,
                    )
                keys = DataBase.keys("isBan:*")
                for i in keys:
                    n += 1
                    userID = i.replace(f'{db}.isBan:', '')
                    text = "{}{}- {} | {}\n".format(
                        text,
                        n,
                        await userInfos(userID),
                        userID,
                    )
                with open(
                    "docs/list_block.txt", mode="a", encoding="utf-8"
                ) as file:
                    file.write(text)
                await sendDocument(
                    chat_id, open("docs/list_block.txt", encoding="utf-8")
                )
                inlineKeys.add(
                    iButtun(
                        buttuns["back"],
                        callback_data="backstart:@{}".format(user_id),
                    ),
                )
                await editText(
                    chat_id,
                    msg_id,
                    0,
                    langU["blocklist_sent"],
                    None,
                    inlineKeys,
                )
                os.system("rm docs/list_block.txt")
            elif ap[1] == "stats":
                stat_users = DataBase.scard("allUsers")
                stat_block = DataBase.scard("isBanned")
                stat_whisper = DataBase.get("stat_whisper")
                stat_anon = DataBase.get("stat_anon")
                await editText(
                    chat_id,
                    msg_id,
                    0,
                    langU["stats"]
                    .format(
                        stat_users,
                        stat_block,
                        stat_whisper,
                        stat_anon,
                    )
                    .replace("None", "0"),
                    "html",
                    back_keys(user_id),
                )
        if re.match(r"^anon:@(\d+)$", input):
            DataBase.delete("ready_to_change_link:{}".format(user_id))
            DataBase.delete("ready_to_change_name:{}".format(user_id))
            DataBase.delete("ready_to_enter_id:{}".format(user_id))
            DataBase.delete("ready_to_recv_special:{}".format(user_id))
            DataBase.delete("who_conneted:{}".format(user_id))
            await editText(
                chat_id,
                msg_id,
                0,
                langU["anon"].format(GlobalValues().botName),
                "html",
                anonymous_keys(user_id),
            )
        if re.match(r"^anon:link:@(\d+)$", input):
            DataBase.delete("ready_to_change_link:{}".format(user_id))
            await editText(
                chat_id,
                msg_id,
                0,
                langU["my_link_anon"].format(
                    GlobalValues().botName,
                    GlobalValues().botUser,
                    DataBase.get("link_anon:{}".format(user_id)),
                ),
                "html",
                anonymous_my_link_keys(user_id),
            )
        if re.match(r"^anon:cus:@(\d+)$", input):
            DataBase.setex(
                "ready_to_change_link:{}".format(user_id), 3600, "True"
            )
            DataBase.set(
                "pre_msgbot:{}".format(user_id), msg.message.message_id
            )
            await editText(
                chat_id,
                msg_id,
                0,
                "{}t.me/{}?start={}".format(
                    langU["customize_link_anon"],
                    GlobalValues().botUser,
                    DataBase.get("link_anon:{}".format(user_id)),
                ),
                None,
                anonymous_cus_link_keys(user_id),
            )
        if re.match(r"^anon:change:@(\d+)$", input):
            link_previous = DataBase.get("link_anon:{}".format(user_id))
            DataBase.delete("link_anon:{}".format(link_previous))
            DataBase.srem("links_anon", link_previous)
            text = generate_link()
            while True:
                if not DataBase.sismember("links_anon", text):
                    DataBase.set("link_anon:{}".format(user_id), text)
                    DataBase.set("link_anon:{}".format(text), user_id)
                    DataBase.sadd("links_anon", text)
                    break
                text = generate_link()
            await editText(
                chat_id,
                msg_id,
                0,
                "{}t.me/{}?start={}".format(
                    langU["customize_link_anon"],
                    GlobalValues().botUser,
                    DataBase.get("link_anon:{}".format(user_id)),
                ),
                None,
                anonymous_cus_link_keys(user_id),
            )
        if re.match(r"^anon:telg:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                "{}\n<code>https://t.me/{}?start={}</code>".format(
                    langU["telg_link_anon"],
                    GlobalValues().botUser,
                    DataBase.get("link_anon:{}".format(user_id)),
                ),
                "html",
                anonymous_insta_link_keys(user_id),
            )
        if re.match(r"^anon:insta:@(\d+)$", input):
            link_picture = '<a href="https://s6.uupload.ir/files/photo_2022-09-01_18-03-08_s3qf.jpg">مشاهده عکس آموزشی</a>'
            await editText(
                chat_id,
                msg_id,
                0,
                langU["insta_link_anon"].format(
                    GlobalValues().botUser, DataBase.get("link_anon:{}".format(user_id))
                ),
                parse_mode="html",
                reply_markup=anonymous_insta_link_keys(user_id),
            )
        if re.match(r"^anon:help:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                langU["help_anon"],
                None,
                anonymous_help_keys(user_id),
            )
        if re.match(r"^anon:help(\d+):@(\d+)$", input):
            ap = re_matches(r"^anon:help(\d+):@(\d+)$", input)
            hash = ":@{}".format(user_id)
            inlineKeys = iMarkup()
            inlineKeys.add(
                iButtun(
                    buttuns["back_help_anon"],
                    callback_data="anon:help{}".format(hash),
                )
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["help{}_anon".format(ap[1])].format(GlobalValues().botName),
                None,
                inlineKeys,
            )
        if re.match(r"^anon:stats:@(\d+)$", input):
            await answerCallbackQuery(
                msg,
                langU["stats_anon"].format(
                    int(
                        DataBase.get("user.stats_anon:{}".format(user_id)) or 0
                    )
                ),
                show_alert=True,
                cache_time=90,
            )
        if re.match(r"^anon:name:@(\d+)$", input):
            DataBase.delete("ready_to_change_name:{}".format(user_id))
            await editText(
                chat_id,
                msg_id,
                0,
                langU["name_anon"].format(
                    DataBase.get("name_anon2:{}".format(user_id))
                    or msg.from_user.first_name
                ),
                None,
                anonymous_name_keys(user_id),
            )
        if re.match(r"^anon:cus_name:@(\d+)$", input):
            DataBase.setex(
                "ready_to_change_name:{}".format(user_id), 3600, "True"
            )
            DataBase.set(
                "pre_msgbot:{}".format(user_id), msg.message.message_id
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["help_cus_name_anon"],
                None,
                anonymous_cus_name_keys(user_id),
            )
        if re.match(r"^anon:default_name:@(\d+)$", input):
            DataBase.delete("name_anon2:{}".format(user_id))
            await answerCallbackQuery(
                msg, langU["changed_name_anon"], show_alert=True, cache_time=90
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["name_anon"].format(
                    DataBase.get("name_anon2:{}".format(user_id))
                    or msg.from_user.first_name
                ),
                None,
                anonymous_name_keys(user_id),
            )
        if re.match(r"^anon:send:@(\d+)$", input):
            DataBase.setex(
                "ready_to_enter_id:{}".format(user_id), 3600, "True"
            )
            DataBase.set(
                "pre_msgbot:{}".format(user_id), msg.message.message_id
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["enter_id_for_send"],
                None,
                anonymous_back_keys(user_id),
            )
        if re.match(r"^anon:b:(\w+):(\d+):(\d+):@(\d+)$", input):
            ap = re_matches(r"^anon:b:(\w+):(\d+):(\d+):@(\d+)$", input)
            token_user = ap[1]
            token_to_id = local_id_user(uniq_id=token_user)
            if DataBase.sismember("blocks:{}".format(user_id), token_to_id):
                DataBase.srem("blocks:{}".format(user_id), token_to_id)
                text = langU["user_unblocked"]
            else:
                DataBase.sadd("blocks:{}".format(user_id), token_to_id)
                text = langU["user_blocked"]
            input_ = _.reply_markup.inline_keyboard[1][0].callback_data
            SHOW_SENDER = False
            if input_ == "none:yes":
                SHOW_SENDER = token_to_id
            await answerCallbackQuery(msg, text, show_alert=True, cache_time=2)
            await editMessageReplyMarkup(
                chat_id,
                msg_id,
                reply_markup=anonymous_new_message_keys(
                    user_id, token_user, ap[2], SHOW_SENDER, ap[3]
                ),
            )
        if re.match(r"^anon:r:(\w+):(\d+):(\d+):@(\d+)$", input):
            ap = re_matches(r"^anon:r:(\w+):(\d+):(\d+):@(\d+)$", input)
            await answerCallbackQuery(
                msg, langU["help_reply_anon"], show_alert=True, cache_time=3600
            )
        if re.match(r"^anon:t:(\d+):@(\d+)$", input):
            ap = re_matches(r"^anon:t:(\d+):@(\d+)$", input)
            ti_me = datetime.fromtimestamp(int(ap[1]))
            ti_me = ti_me.strftime("%Y-%m-%d %H:%M:%S")
            ti_me = re_matches(r"(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)", ti_me)
            if user_steps[user_id]["lang"] == "fa":
                ti_me2 = gregorian_to_jalali(
                    int(ti_me[1]), int(ti_me[2]), int(ti_me[3])
                )
                sent_time = "{:04d}/{}/{:02d} - {:02d}:{:02d}:{:02d}".format(
                    ti_me2[0],
                    echoMonth(ti_me2[1], True),
                    ti_me2[2],
                    int(ti_me[4]),
                    int(ti_me[5]),
                    int(ti_me[6]),
                )
            else:
                sent_time = "{:04d}/{}/{:02d} - {:02d}:{:02d}:{:02d}".format(
                    int(ti_me[1]),
                    echoMonth(ti_me[2], False),
                    int(ti_me[3]),
                    int(ti_me[4]),
                    int(ti_me[5]),
                    int(ti_me[6]),
                )
            await answerCallbackQuery(
                msg, sent_time, show_alert=True, cache_time=180
            )
        if re.match(r"^anon:receive:@(\d+)$", input):
            ap = re_matches(r"^anon:receive:@(\d+)$", input)
            if DataBase.get("dont_receive_anon:{}".format(user_id)):
                DataBase.delete("dont_receive_anon:{}".format(user_id))
                text = langU["receive_anon_active"]
            else:
                DataBase.set("dont_receive_anon:{}".format(user_id), "True")
                text = langU["receive_anon_deactive"]
            await answerCallbackQuery(msg, text, show_alert=True, cache_time=2)
            await editMessageReplyMarkup(
                chat_id, msg_id, reply_markup=anonymous_keys(user_id)
            )
        if re.match(r"^anon:lock:@(\d+)$", input):
            ap = re_matches(r"^anon:lock:@(\d+)$", input)
            if DataBase.get("anti_save.anon:{}".format(user_id)):
                DataBase.delete("anti_save.anon:{}".format(user_id))
                text = langU["lock_anon_deactive"]
            else:
                DataBase.set("anti_save.anon:{}".format(user_id), "True")
                text = langU["lock_anon_active"]
            await answerCallbackQuery(msg, text, show_alert=True, cache_time=2)
            await editMessageReplyMarkup(
                chat_id, msg_id, reply_markup=anonymous_keys(user_id)
            )
        if re.match(r"^anon:myblock:@(\d+)$", input):
            if DataBase.scard("blocks:{}".format(user_id)) > 0:
                await editText(
                    chat_id,
                    msg_id,
                    0,
                    langU["besure_del_all_blocks"],
                    None,
                    anonymous_delete_blocks_keys(user_id),
                )
            else:
                await answerCallbackQuery(
                    msg,
                    langU["blocks_empty_anon"],
                    show_alert=True,
                    cache_time=10,
                )
        if re.match(r"^anon:delblocks:@(\d+)$", input):
            DataBase.delete("blocks:{}".format(user_id))
            await answerCallbackQuery(
                msg, langU["blocks_clear_anon"], show_alert=True, cache_time=2
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["anon"].format(GlobalValues().botName),
                "html",
                anonymous_keys(user_id),
            )
        if re.match(r"^anon:sendmore:(\w+):@(\d+)$", input):
            ap = re_matches(r"^anon:sendmore:(\w+):@(\d+)$", input)
            hash = ":@{}".format(user_id)
            token_user = ap[1]
            token_to_id = local_id_user(uniq_id=token_user)
            inlineKeys = iMarkup()
            inlineKeys.add(
                iButtun(
                    buttuns["cancel"], callback_data="backstart{}".format(hash)
                )
            )
            DataBase.set("who_conneted:{}".format(user_id), token_to_id)
            await _.edit_reply_markup()
            await sendText(
                chat_id,
                0,
                1,
                langU["user_connect_4send"].format(
                    DataBase.get("name_anon2:{}".format(token_to_id))
                ),
                "md",
                inlineKeys,
            )
        if re.match(r"^whisper:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                langU["whisper"].format(GlobalValues().botUser, GlobalValues().botName),
                "html",
                whisper_keys(user_id),
            )
        if re.match(r"^whisper:settings:@(\d+)$", input):
            await editText(
                chat_id,
                msg_id,
                0,
                langU["whisper_settings"].format(GlobalValues().botName),
                "html",
                whisper_settings_keys(user_id),
            )
        if re.match(r"^whisper:settings:(.*):@(\d+)$", input):
            ap = re_matches(r"^whisper:settings:(.*):@(\d+)$", input)
            if ap[1] == "recents":
                recent = DataBase.smembers("whisper_recent:{}".format(user_id))
                recent2 = DataBase.smembers("whisper_recent2:{}".format(user_id))
                if len(recent) > 0 or len(recent2) > 0:
                    text = langU["recent_list"].format(
                        len(recent) + len(recent2)
                    )
                    inlineKeys = iMarkup()
                    members = set()
                    count = 0
                    for i in recent:
                        name_user = await userInfos(i, "name")
                        if "Deleted" in name_user:
                            DataBase.srem(f"whisper_recent:{user_id}", i)
                            DataBase.srem(f"whisper_recent2:{user_id}", i)
                        elif not i in members:
                            members.add(i)
                            count += 1
                            inlineKeys.add(
                                iButtun(
                                    f"{count}- {name_user}",
                                    callback_data=f"recent:{i}:@{user_id}",
                                ),
                            )
                            if len(members) > 22:
                                break                            
                    for i in recent2:
                        name_user = await userInfos(i, "name")
                        if "Deleted" in name_user:
                            DataBase.srem(f"whisper_recent:{user_id}", i)
                            DataBase.srem(f"whisper_recent2:{user_id}", i)
                        elif not i in members:
                            members.add(i)
                            count += 1
                            inlineKeys.add(
                                iButtun(
                                    f"{count}- {name_user}",
                                    callback_data=f"recent:{i}:@{user_id}",
                                ),
                            )
                            if len(members) > 22:
                                break
                        elif i in members:
                            DataBase.srem(f"whisper_recent2:{user_id}", i)
                    inlineKeys.add(
                        iButtun(
                            buttuns["back_nset"],
                            callback_data=f"whisper:settings:@{user_id}",
                        ),
                        iButtun(
                            buttuns["delall"],
                            callback_data=f"recent:all:@{user_id}",
                        ),
                    )
                    await editText(chat_id, msg_id, 0, text, None, inlineKeys)
                else:
                    await answerCallbackQuery(
                        msg,
                        langU["recent_empty"],
                        show_alert=True,
                        cache_time=10,
                    )
            elif ap[1] == "blocks":
                blocks2 = DataBase.smembers("blocks2:{}".format(user_id))
                if len(blocks2) > 0:
                    text = langU["blocks2_list"].format(len(blocks2))
                    inlineKeys = iMarkup()
                    count = 0
                    for i in blocks2:
                        name_user = await userInfos(i, "name")
                        if "Deleted" in name_user:
                            DataBase.srem(f"blocks2:{user_id}", i)
                        else:
                            count += 1
                            inlineKeys.add(
                                iButtun(
                                    f"{count}- {name_user}",
                                    callback_data=f"blocks2:{i}:@{user_id}",
                                ),
                            )
                            if count > 22:
                                break
                    inlineKeys.add(
                        iButtun(
                            buttuns["back_nset"],
                            callback_data=f"whisper:settings:@{user_id}",
                        ),
                        iButtun(
                            buttuns["delall"],
                            callback_data=f"blocks2:all:@{user_id}",
                        ),
                    )
                    await editText(chat_id, msg_id, 0, text, None, inlineKeys)
                else:
                    await answerCallbackQuery(
                        msg,
                        langU["blocks2_empty"],
                        show_alert=True,
                        cache_time=10,
                    )
            elif ap[1] == "delall":
                count = len(DataBase.keys(f"whisper:{user_id}:*"))
                if count == 0:
                    return await answerCallbackQuery(
                        msg,
                        langU["whispers_sent_is_zero"],
                        show_alert=True,
                        cache_time=10,
                    )
                inlineKeys = whisper_delall_keys(user_id)
                await editText(
                    chat_id,
                    msg_id,
                    0,
                    langU["delall"].format(count),
                    "html",
                    inlineKeys
                )
        if re.match(r"^whisper:delall:y:@(\d+)$", input):
            whispers_keys = DataBase.keys(f"whisper:{user_id}:*")
            if len(whispers_keys) == 0:
                await answerCallbackQuery(
                    msg,
                    langU["whispers_sent_is_zero"],
                    show_alert=True
                )
                return await editText(
                    chat_id,
                    msg_id,
                    0,
                    langU["whisper_settings"].format(GlobalValues().botName),
                    "html",
                    whisper_settings_keys(user_id),
                )
            if DataBase.get(f"limit_delall:{user_id}"):
                next_time = DataBase.ttl(f"limit_delall:{user_id}")
                next_time = int(time()) + next_time
                next_time = datetime.fromtimestamp(next_time)
                next_time = next_time.strftime("%H:%M:%S")
                await answerCallbackQuery(
                    msg,
                    langU["you_are_on_limit"].format(next_time),
                    show_alert=True
                )
                return await editText(
                    chat_id,
                    msg_id,
                    0,
                    langU["whisper_settings"].format(GlobalValues().botName),
                    "html",
                    whisper_settings_keys(user_id),
                )
            count = len(whispers_keys) * 1
            if count > 60:
                count = float(count / 60)
                text = "{:.2f}".format(count)
                text = buttuns["minute"].format(text)
            else:
                text = "{:,}".format(count)
                text = buttuns["seconds"].format(text)
            await editText(
                chat_id,
                msg_id,
                0,
                langU["wait_delall"].format(len(whispers_keys), text)
            )
            count = 0
            for i in whispers_keys:
                null, from_user, time_data = i.split(':')
                hash_db = i
                seen_id = rds.hget(
                    hash_db, "seen_id"
                )
                if seen_id:
                    seen_id = seen_id.split(":")
                    await delete_messages(seen_id[0], seen_id[1])
                special_msgID = DataBase.hget(
                    "whisper_special:{}".format(from_user), "id"
                )
                DataBase.srem(
                    "whisper_autodel",
                    f"{from_user}:{time_data}:{special_msgID}"
                )
                rds.delete(hash_db)
                DataBase.delete("whisper_special:{}".format(from_user))
                msgID = DataBase.get(
                    f"whispers_sent:{from_user}:{time_data}"
                )
                if msgID:
                    await editMessageReplyMarkup(
                        inline_message_id=msgID,
                        reply_markup=whisper_seen2_keys(
                            user_id,
                            from_user,
                            time_data
                        ),
                    )
                    DataBase.delete(
                        f"whispers_sent:{from_user}:{time_data}"
                    )
                await asyncio.sleep(1)
                count += 1
                if count > 20:
                    break
            await editText(
                chat_id,
                msg_id,
                0,
                langU["delall_whisper_result"].format(count)
            )
            DataBase.setex(f"limit_delall:{user_id}", 3600, "True")
        if re.match(r"^blocks2:all:@(\d+)$", input):
            inlineKeys = iMarkup()
            inlineKeys.add(
                iButtun(
                    buttuns["no"],
                    callback_data=f"whisper:settings:blocks:@{user_id}",
                ),
                iButtun(
                    buttuns["yes"],
                    callback_data=f"blocks2:all:y:@{user_id}",
                ),
            )
            await editText(
                chat_id, msg_id, 0, langU["sure_del_blocks2"], None, inlineKeys
            )
        if re.match(r"^blocks2:all:y:@(\d+)$", input):
            DataBase.delete(f"blocks2:{user_id}")
            await answerCallbackQuery(msg, langU["delall_y"], show_alert=True)
            await editText(
                chat_id,
                msg_id,
                0,
                langU["whisper_settings"].format(GlobalValues().botName),
                "html",
                whisper_settings_keys(user_id),
            )
        if re.match(r"^blocks2:(\d+):@(\d+)$", input):
            ap = re_matches(r"^blocks2:(\d+):@(\d+)$", input)
            inlineKeys = iMarkup()
            uname_user = await userInfos(int(ap[1]), info="username")
            name_user = await userInfos(int(ap[1]), info="name")
            if uname_user:
                call_url = "https://t.me/{}".format(uname_user)
            else:
                call_url = "https://t.me?openmessage?user_id={}".format(ap[1])
            inlineKeys.add(
                iButtun(name_user, call_url),
            )
            inlineKeys.add(
                iButtun(
                    buttuns["no"],
                    callback_data=f"whisper:settings:blocks:@{user_id}",
                ),
                iButtun(
                    buttuns["yes"],
                    callback_data=f"blocks2:{ap[1]}:y:@{user_id}",
                ),
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["blocks2_info"].format(ap[1]),
                "html",
                inlineKeys,
            )
        if re.match(r"^blocks2:(\d+):y:@(\d+)$", input):
            ap = re_matches(r"^blocks2:(\d+):y:@(\d+)$", input)
            DataBase.srem(f"blocks2:{user_id}", ap[1])
            await answerCallbackQuery(
                msg, langU["blocks2_user_del"], show_alert=True
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["whisper_settings"].format(GlobalValues().botName),
                "html",
                whisper_settings_keys(user_id),
            )
        if re.match(r"^recent:all:@(\d+)$", input):
            inlineKeys = iMarkup()
            inlineKeys.add(
                iButtun(
                    buttuns["no"],
                    callback_data=f"whisper:settings:recents:@{user_id}",
                ),
                iButtun(
                    buttuns["yes"],
                    callback_data=f"recent:all:y:@{user_id}",
                ),
            )
            await editText(
                chat_id, msg_id, 0, langU["sure_del_recent"], None, inlineKeys
            )
        if re.match(r"^recent:all:y:@(\d+)$", input):
            DataBase.delete(f"whisper_recent:{user_id}")
            DataBase.delete(f"whisper_recent2:{user_id}")
            await answerCallbackQuery(
                msg, langU["delall_recent"], show_alert=True
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["whisper_settings"].format(GlobalValues().botName),
                "html",
                whisper_settings_keys(user_id),
            )
        if re.match(r"^recent:(\d+):@(\d+)$", input):
            ap = re_matches(r"^recent:(\d+):@(\d+)$", input)
            uname_user = await userInfos(int(ap[1]), info="username")
            name_user = await userInfos(int(ap[1]), info="name")
            inlineKeys = whisper_recent_user_keys(
                uname_user,
                name_user,
                int(ap[1]),
                user_id
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["recent_info"].format(ap[1]),
                "html",
                inlineKeys,
            )
        if re.match(r"^recent:(\d+):y:@(\d+)$", input):
            ap = re_matches(r"^recent:(\d+):y:@(\d+)$", input)
            DataBase.srem(f"whisper_recent:{user_id}", ap[1])
            DataBase.srem(f"whisper_recent2:{user_id}", ap[1])
            await answerCallbackQuery(
                msg, langU["recent_user_del"], show_alert=True
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["whisper_settings"].format(GlobalValues().botName),
                "html",
                whisper_settings_keys(user_id),
            )
        if re.match(r"^recent:(\d+):b:@(\d+)$", input):
            ap = re_matches(r"^recent:(\d+):b:@(\d+)$", input)
            hash_db = f"blocks2:{user_id}"
            who_user = int(ap[1])
            uname_user = await userInfos(who_user, info="username")
            name_user = await userInfos(who_user, info="name")
            if DataBase.sismember(hash_db, who_user):
                DataBase.srem(f"blocks2:{user_id}", who_user)
                text = langU["user_unblocked_whisper"]
            else:
                DataBase.sadd(f"blocks2:{user_id}", who_user)
                text = langU["user_blocked_whisper"]
            await answerCallbackQuery(
                msg, text, show_alert=True, cache_time=5
            )
            inlineKeys = whisper_recent_user_keys(
                uname_user,
                name_user,
                who_user,
                user_id
            )
            await editText(
                chat_id,
                msg_id,
                0,
                langU["recent_info"].format(ap[1]),
                "html",
                inlineKeys,
            )
        if re.match(r"^whisper:help:@(\d+)$", input):
            try:
                await _.delete()
            except:
                pass
            await sendText(
                chat_id,
                _.reply_to_message,
                1,
                langU["whisper_help"],
                "html",
                whisper_help_keys(user_id),
            )
        if re.match(r"^whisper:settings1:(.*):@(\d+)$", input):
            ap = re_matches(r"^whisper:settings1:(.*):@(\d+)$", input)
            if ap[1] == "autodel":
                if DataBase.hget(
                    "setting_whisper:{}".format(user_id), "autodel"
                ):
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        langU["autodel"],
                        None,
                        whisper_autodel2_keys(user_id),
                    )
                else:
                    await editText(
                        chat_id,
                        msg_id,
                        0,
                        langU["autodel"],
                        None,
                        whisper_autodel_keys(user_id),
                    )
            else:
                if DataBase.hget("setting_whisper:{}".format(user_id), ap[1]):
                    DataBase.hdel("setting_whisper:{}".format(user_id), ap[1])
                    text = langU["whisper_setoff_{}".format(ap[1])]
                else:
                    DataBase.hset("setting_whisper:{}".format(user_id), ap[1], 1)
                    text = langU["whisper_seton_{}".format(ap[1])]
                await answerCallbackQuery(
                    msg, text, show_alert=True, cache_time=2
                )
                await editMessageReplyMarkup(
                    chat_id, msg_id, reply_markup=whisper_settings_keys(user_id)
                )
        if re.match(r"^whisper:autodel:@(\d+)$", input):
            ap = re_matches(r"^whisper:autodel:@(\d+)$", input)
            if DataBase.hget("setting_whisper:{}".format(user_id), "autodel"):
                DataBase.hdel("setting_whisper:{}".format(user_id), "autodel")
                text = langU["whisper_setoff_autodel"]
                await answerCallbackQuery(msg, text, cache_time=2)
                await editMessageReplyMarkup(
                    chat_id, msg_id, reply_markup=whisper_autodel_keys(user_id)
                )
            else:
                if not DataBase.get("autodel_time:{}".format(user_id)):
                    DataBase.set("autodel_time:{}".format(user_id), 10)
                text = langU["whisper_seton_autodel"]
                DataBase.hset("setting_whisper:{}".format(user_id), "autodel", 1)
                await answerCallbackQuery(msg, text, cache_time=2)
                await editMessageReplyMarkup(
                    chat_id, msg_id, reply_markup=whisper_autodel2_keys(user_id)
                )
        if re.match(r"^whisper:help:(.*):@(\d+)$", input):
            ap = re_matches(r"^whisper:help:(.*):@(\d+)$", input)
            try:
                await _.delete()
            except:
                pass
            if ap[1] == "send":
                file = "docs/helps/help_send.jpg"
                with open(file, "rb") as file:
                    await sendPhoto(
                        chat_id,
                        file,
                        langU["whisper_help_send"].format(GlobalValues().botUser),
                        "html",
                        _.reply_to_message,
                        reply_markup=whisper_help1_keys(user_id),
                    )
            elif ap[1] == "media":
                file = "docs/helps/help_media.jpg"
                with open(file, "rb") as file:
                    await sendPhoto(
                        chat_id,
                        file,
                        langU["whisper_help_media"].format(GlobalValues().botUser),
                        "html",
                        _.reply_to_message,
                        reply_markup=whisper_help2_keys(user_id),
                    )
            elif ap[1] == "group":
                file = "docs/helps/help_group.jpg"
                with open(file, "rb") as file:
                    await sendPhoto(
                        chat_id,
                        file,
                        langU["whisper_help_group"].format(GlobalValues().botUser),
                        "html",
                        _.reply_to_message,
                        reply_markup=whisper_help3_keys(user_id),
                    )
            elif ap[1] == "bd":
                file = "docs/helps/help_bd.jpg"
                with open(file, "rb") as file:
                    await sendPhoto(
                        chat_id,
                        file,
                        langU["whisper_help_bd"].format(GlobalValues().botUser),
                        "html",
                        _.reply_to_message,
                        reply_markup=whisper_help4_keys(user_id),
                    )
            elif ap[1] == "noid":
                file = "docs/helps/help_noid.mp4"
                with open(file, "rb") as file:
                    await sendVideo(
                        chat_id,
                        _.reply_to_message,
                        file,
                        langU["whisper_help_noid"].format(GlobalValues().botUser),
                        "html",
                        supports_streaming=True,
                        reply_markup=whisper_help5_keys(user_id),
                    )
            elif ap[1] == "shset":
                file = "docs/helps/help_shset.jpg"
                with open(file, "rb") as file:
                    await sendPhoto(
                        chat_id,
                        file,
                        langU["whisper_help_shset"].format(GlobalValues().botUser),
                        "html",
                        _.reply_to_message,
                        reply_markup=whisper_help6_keys(user_id),
                    )
            elif ap[1] == "prob":
                file = "docs/helps/help_prob.jpg"
                with open(file, "rb") as file:
                    await sendPhoto(
                        chat_id,
                        file,
                        langU["whisper_help_prob"].format(GlobalValues().botUser),
                        "html",
                        _.reply_to_message,
                        reply_markup=whisper_help7_keys(user_id),
                    )
            elif ap[1] == "examp":
                await sendText(
                    chat_id,
                    _.reply_to_message,
                    1,
                    langU["whisper_help_examp"],
                    "html",
                    whisper_help8_keys(user_id),
                )
        if re.match(r"^whisper:vid:(\d+):@(\d+)$", input):
            ap = re_matches(r"^whisper:vid:(\d+):@(\d+)$", input)
            try:
                await _.delete()
            except:
                pass
            keyboard = whisper_help7_keys(user_id)
            if ap[1] == "5":
                keyboard = whisper_help9_keys(user_id)
            elif ap[1] == "6":
                keyboard = whisper_help5_keys(user_id)
            file = f"docs/helps/vid-{ap[1]}.mp4"
            with open(file, "rb") as file:
                await sendVideo(
                    chat_id,
                    _.reply_to_message,
                    file,
                    langU[f"whisper_vid-{ap[1]}"].format(GlobalValues().botUser),
                    "html",
                    supports_streaming=True,
                    reply_markup=keyboard,
                )
        if re.match(r"^autodel:(.*):@(\d+)$", input):
            ap = re_matches(r"^autodel:(.*):@(\d+)$", input)
            old_autodel_time = DataBase.get("autodel_time:{}".format(user_id))
            if int(old_autodel_time) + int(ap[1]) > 0:
                DataBase.set(
                    "autodel_time:{}".format(user_id),
                    int(old_autodel_time) + int(ap[1]),
                )
                await editMessageReplyMarkup(
                    chat_id, msg_id, reply_markup=whisper_autodel2_keys(user_id)
                )
            else:
                await answerCallbackQuery(
                    msg, langU["autodel_must_1"], cache_time=2
                )
        if re.match(r"^special:cancel:@(\d+)", input):
            time_data = DataBase.hget(
                "whisper_special:{}".format(user_id), "time"
            )
            special_msgID = DataBase.hget(
                "whisper_special:{}".format(user_id), "id"
            )
            DataBase.delete("whisper:{}:{}".format(user_id, time_data))
            DataBase.delete("whisper_special:{}".format(user_id))
            DataBase.delete("ready_to_recv_special:{}".format(user_id))
            DataBase.srem(
                "whisper_autodel", f"{user_id}:{time_data}:{special_msgID}"
            )
            await editText(
                inline_msg_id=special_msgID, text=langU["special_whisper_cancel"]
            )
            try:
                await _.delete()
            except:
                pass
            await answerCallbackQuery(msg, langU["canceled"], cache_time=3600)
        if re.match(r"^special:antisave:@(\d+)", input):
            ap = re_matches(r"^special:antisave:@(\d+)", input)
            if DataBase.hget("setting_whisper:{}".format(user_id), "antisave"):
                DataBase.hdel("setting_whisper:{}".format(user_id), 'antisave')
                text = langU["whisper_setoff_antisave"]
            else:
                DataBase.hset("setting_whisper:{}".format(user_id), "antisave", "True")
                text = langU["whisper_seton_antisave"]
            await answerCallbackQuery(msg, text, show_alert=True, cache_time=2)
            await editMessageReplyMarkup(
                chat_id, msg_id, reply_markup=register_special_keys(user_id)
            )
        if re.match(r"^special:reg1:@(\d+)", input):
            try:
                msg_ = await reply_msg.forward(GlobalValues().logchat)
                find_ID, find_type, can_hide = find_media_id(msg_)
                time_data = DataBase.hget(
                    "whisper_special:{}".format(user_id), "time"
                )
                hash_db = "whisper:{}:{}".format(user_id, time_data)
                special_msgID = DataBase.hget(
                    "whisper_special:{}".format(user_id), "id"
                )
                DataBase.delete("ready_to_recv_special:{}".format(user_id))
                DataBase.hset(
                    hash_db,
                    "file_id",
                    find_ID,
                )
                DataBase.hset(
                    hash_db,
                    "file_type",
                    find_type,
                )
                DataBase.hset(
                    hash_db,
                    "source_id",
                    reply_id,
                )
                DataBase.hset(
                    hash_db,
                    "msg_id",
                    msg_.message_id,
                )
                if DataBase.hget(f"setting_whisper:{user_id}", "autodel"):
                    DataBase.sadd(
                        "whisper_autodel",
                        f"{user_id}:{time_data}:{special_msgID}",
                    )
                inlineKeys = iMarkup()
                inlineKeys.add(
                    iButtun(
                        buttuns["show_whisper"],
                        callback_data="shown:{}:{}".format(user_id, time_data),
                    )
                )
                users_data = DataBase.hget(
                    hash_db, "users"
                )
                if "@" in users_data:
                    name_user = await userIds(users_data)
                else:
                    name_user = users_data
                name_user2 = None
                if DataBase.hget(f"setting_whisper:{name_user}", "noname"):
                    name_user2 = langU["no_name"]
                name_user = await userInfos(name_user, info="name")
                await editText(
                    inline_msg_id=special_msgID,
                    text=langU["special_whisper_registered"].format(
                        name_user2 or name_user
                    ),
                    parse_mode="html",
                    reply_markup=inlineKeys,
                )
                await editText(chat_id, msg_id, 0, langU["reg_whisper"])
            except Exception as e:
                await editText(chat_id, msg_id, 0, langU["error_reg_whisper"])
        if re.match(r"^special:reg2:@(\d+)", input):
            try:
                find_ID, find_type, can_hide = find_media_id(reply_msg)
                if not can_hide:
                    return await answerCallbackQuery(
                        msg,
                        langU["cant_hide"],
                        show_alert=True,
                        cache_time=3600,
                    )
                msg_ = await reply_msg.forward(GlobalValues().logchat)
                find_ID, find_type, can_hide = find_media_id(msg_)
                time_data = DataBase.hget(
                    "whisper_special:{}".format(user_id), "time"
                )
                hash_db = "whisper:{}:{}".format(user_id, time_data)
                special_msgID = DataBase.hget(
                    "whisper_special:{}".format(user_id), "id"
                )
                DataBase.delete("ready_to_recv_special:{}".format(user_id))
                DataBase.hset(
                    hash_db,
                    "file_id",
                    find_ID,
                )
                DataBase.hset(
                    hash_db,
                    "file_type",
                    find_type,
                )
                DataBase.hset(
                    hash_db,
                    "source_id",
                    reply_id,
                )
                DataBase.hset(
                    hash_db,
                    "msg_id",
                    msg_.message_id,
                )
                if DataBase.hget(f"setting_whisper:{user_id}", "autodel"):
                    DataBase.sadd(
                        "whisper_autodel",
                        f"{user_id}:{time_data}:{special_msgID}",
                    )
                inlineKeys = iMarkup()
                inlineKeys.add(
                    iButtun(
                        buttuns["show_whisper"],
                        switch_inline_query_current_chat="sp{}.{}".format(
                            user_id, time_data
                        ),
                    )
                )
                users_data = DataBase.hget(
                    hash_db, "users"
                )
                if "@" in users_data:
                    name_user = await userIds(users_data)
                else:
                    name_user = users_data
                name_user2 = None
                if DataBase.hget(f"setting_whisper:{name_user}", "noname"):
                    name_user2 = langU["no_name"]
                name_user = await userInfos(name_user, info="name")
                await editText(
                    inline_msg_id=special_msgID,
                    text=langU["special_whisper_registered"].format(
                        name_user2 or name_user
                    ),
                    parse_mode="html",
                    reply_markup=inlineKeys,
                )
                await editText(chat_id, msg_id, 0, langU["reg2_whisper"])
            except Exception as e:
                await editText(chat_id, msg_id, 0, langU["error_reg_whisper"])
        if re.match(r"^special:sendpv:@(\d+)", input):
            try:
                msg_ = await reply_msg.forward(GlobalValues().logchat)
                find_ID, find_type, can_hide = find_media_id(msg_)
                time_data = DataBase.hget(
                    "whisper_special:{}".format(user_id), "time"
                )
                hash_db = "whisper:{}:{}".format(user_id, time_data)
                special_msgID = DataBase.hget(
                    "whisper_special:{}".format(user_id), "id"
                )
                DataBase.hset(
                    hash_db,
                    "file_id",
                    find_ID,
                )
                DataBase.hset(
                    hash_db,
                    "file_type",
                    find_type,
                )
                DataBase.hset(
                    hash_db,
                    "source_id",
                    reply_id,
                )
                DataBase.hset(
                    hash_db,
                    "msg_id",
                    msg_.message_id,
                )
                if DataBase.hget(f"setting_whisper:{user_id}", "autodel"):
                    DataBase.sadd(
                        "whisper_autodel",
                        f"{user_id}:{time_data}:{special_msgID}",
                    )
                inlineKeys = iMarkup()
                inlineKeys.add(
                    iButtun(
                        buttuns["show_whisper"],
                        callback_data="showpv:{}:{}".format(
                            user_id, time_data
                        ),
                    )
                )
                users_data = DataBase.hget(
                    hash_db, "users"
                )
                if "@" in users_data:
                    id_user = await userIds(users_data)
                else:
                    id_user = users_data
                if not id_user:
                    return await answerCallbackQuery(
                        msg,
                        langU["cant_sent_whisper_pv"],
                        show_alert=True,
                        cache_time=3600,
                    )
                DataBase.delete("ready_to_recv_special:{}".format(user_id))
                name_user2 = None
                if DataBase.hget(f"setting_whisper:{id_user}", "noname"):
                    name_user2 = langU["no_name"]
                name_user = await userInfos(id_user, info="name")
                await editText(
                    inline_msg_id=special_msgID,
                    text=langU["special_whisper_registered"].format(
                        name_user2 or name_user
                    ),
                    parse_mode="html",
                )
                await sendText(
                    id_user,
                    0,
                    1,
                    lang[lang_user(id_user)]["receive_new_whisper_pv"].format(
                        msg.from_user.first_name
                    ),
                    "html",
                    inlineKeys,
                )
                await editText(
                    chat_id,
                    msg_id,
                    0,
                    langU["sent_whisper_pv"].format(
                        '<a href="tg://user?id={}">{}</a>'.format(
                            id_user, name_user
                        )
                    ),
                    "html",
                )
            except Exception as e:
                await editText(chat_id, msg_id, 0, langU["error_reg_whisper"])
        if re.match(r"^showpv:(\d+):([-+]?\d*\.\d+|\d+)$", input):
            ap = re_matches(r"^showpv:(\d+):([-+]?\d*\.\d+|\d+)$", input)
            from_user = ap[1]
            time_data = ap[2]
            hash_db = "whisper:{}:{}".format(from_user, time_data)
            if DataBase.hash_type(hash_db) != 'hash':
                return await editText(chat_id, msg_id, 0, langU["whisper_404"])
            try:
                await _.delete()
            except:
                pass
            anti_save = False
            if DataBase.hget(f"setting_whisper:{from_user}", "antisave"):
                anti_save = True
            DataBase.set(
                "whisper_seen_time:{}:{}".format(from_user, time_data),
                int(time()),
            )
            DataBase.incr(
                "whisper_seen_count:{}:{}".format(from_user, time_data)
            )
            DataBase.sadd(
                "whisper_seened:{}:{}".format(from_user, time_data), user_id
            )
            special_msgID = DataBase.hget(
                "whisper_special:{}".format(from_user), "id"
            )
            users_data = DataBase.hget(
                hash_db, "users"
            )
            file_id = DataBase.hget(
                hash_db, "file_id"
            )
            file_type = DataBase.hget(
                hash_db, "file_type"
            )
            source_id = DataBase.hget(
                hash_db, "source_id"
            )
            msgid = DataBase.hget(
                hash_db, "msg_id"
            )
            inlineKeys = await show_speical_whisper_keys(user_id, from_user)
            msg_ = await copyMessage(
                chat_id,
                GlobalValues().logchat,
                msgid,
                protect_content=anti_save,
                reply_markup=inlineKeys,
            )
            if DataBase.hget(f"setting_whisper:{from_user}", "seen"):
                await sendText(
                    from_user,
                    source_id,
                    1,
                    lang[lang_user(from_user)]["speical_whisper_seen"].format(
                        msg.from_user.first_name
                    ),
                )
            await editText(
                inline_msg_id=special_msgID,
                text=lang[lang_user(from_user)]["speical_whisper_seen2"].format(
                    msg.from_user.first_name
                ),
                parse_mode="html",
                reply_markup=whisper_seen3_keys(from_user, time_data),
            )
            if DataBase.hget(f"setting_whisper:{from_user}", "dispo"):
                special_msgID = DataBase.hget(
                    "whisper_special:{}".format(from_user), "id"
                )
                DataBase.srem(
                    "whisper_autodel", f"{from_user}:{time_data}:{special_msgID}"
                )
                DataBase.delete(hash_db)
                DataBase.delete("whisper_special:{}".format(from_user))
            DataBase.hset(
                hash_db,
                "seen_id",
                f"{chat_id}:{msg_[1].message_id}",
            )
        if re.match(r"^special:block:(\d+):@(\d+)$", input):
            ap = re_matches(r"^special:block:(\d+):@(\d+)$", input)
            if DataBase.sismember("blocks2:{}".format(user_id), ap[1]):
                DataBase.srem("blocks2:{}".format(user_id), ap[1])
                text = langU["user_unblocked"]
            else:
                DataBase.sadd("blocks2:{}".format(user_id), ap[1])
                text = langU["user_blocked"]
            await answerCallbackQuery(msg, text, show_alert=True, cache_time=2)
            inlineKeys = await show_speical_whisper_keys(user_id, ap[1])
            await editMessageReplyMarkup(
                chat_id, msg_id, reply_markup=inlineKeys
            )
        if re.match(r"^special:report:(\d+):@(\d+)$", input):
            ap = re_matches(r"^special:report:(\d+):@(\d+)$", input)
            await sendText(
                chat_id,
                _,
                1,
                langU["report_special_whisper"],
                "html",
                report_whisper_keys(user_id, ap[1], msg_id),
            )
        if re.match(r"^report:cancel:(\d+)@(\d+)$", input):
            ap = re_matches(r"^report:cancel:(\d+)@(\d+)$", input)
            try:
                await _.delete()
            except:
                pass
            await answerCallbackQuery(msg, langU["canceled"], cache_time=3600)
        if re.match(r"^special:report2:(\d+):(\d+):@(\d+)$", input):
            ap = re_matches(r"^special:report2:(\d+):(\d+):@(\d+)$", input)
            from_user = ap[1]
            msg_ID = ap[2]
            msg_ = await copyMessage(
                GlobalValues().sudoID, chat_id, msg_ID, protect_content=False
            )
            name_user = await userInfos(from_user, info="name")
            text = lang[lang_user(GlobalValues().sudoID)]["reported_this_user"].format(
                msg.from_user.first_name, name_user
            )
            await sendText(
                GlobalValues().sudoID,
                msg_[1].message_id,
                1,
                text,
                "html",
                ban_user_keys(from_user, GlobalValues().sudoID),
            )
            await editText(chat_id, msg_id, 0, langU["reported_special_whisper"])
            await _.reply_to_message.delete()
        if re.match(r"^banuser:(\d+)$", input):
            ap = re_matches(r"^banuser:(\d+)$", input)
            if DataBase.sismember("isBanned", ap[1]):
                DataBase.srem("isBanned", ap[1])
                text = langU["user_unbanned"]
            else:
                DataBase.sadd("isBanned", ap[1])
                text = langU["user_banned"]
            await answerCallbackQuery(msg, text, show_alert=True, cache_time=2)
            inlineKeys = ban_user_keys(ap[1], chat_id)
            await editMessageReplyMarkup(
                chat_id, msg_id, reply_markup=inlineKeys
            )
        if 'none' in input:
            await answerCallbackQuery(
            msg,
            langU["is_for_show"], 
            show_alert=True,
            cache_time=3600)
    else:
        msgID = msg.id
        msg_id = msg.inline_message_id
        if re.match(r"^shown:(\d+):([-+]?\d*\.\d+|\d+)$", input):
            ap = re_matches(r"^shown:(\d+):([-+]?\d*\.\d+|\d+)$", input)
            from_user = ap[1]
            time_data = ap[2]
            hash_db = "whisper:{}:{}".format(from_user, time_data)
            dispo_is_on = DataBase.hget(f"setting_whisper:{from_user}", "dispo")
            if DataBase.hash_type(hash_db) != 'hash':
                return await editText(
                    inline_msg_id=msg_id,
                    text=langU["whisper_404"]
                )
            text_data = DataBase.hget(hash_db, "text")
            users_data = DataBase.hget(hash_db, "users")
            is_allow = (username != "" and username in users_data) or str(
                user_id
            ) in users_data
            if is_allow or str(user_id) in from_user or users_data == "all":
                file_id = DataBase.hget(hash_db, "file_id")
                if file_id:
                    return await answerCallbackQuery(
                        msg,
                        url_web="t.me/{}?start={}_{}".format(
                            GlobalValues().botUser,
                            from_user,
                            time_data.replace(".", "_"),
                        ),
                    )
                await answerCallbackQuery(
                    msg, text_data, show_alert=True, cache_time=3600
                )
                if (
                    DataBase.scard(
                        "whisper_seened:{}:{}".format(from_user, time_data)
                    )
                    == 0
                    and is_allow
                ):
                    if (
                        DataBase.hget(f"setting_whisper:{from_user}", "seen")
                        and users_data != "all"
                    ):
                        await sendText(
                            from_user,
                            0,
                            1,
                            lang[lang_user(from_user)]["whisper_seened"].format(
                                msg.from_user.first_name
                            ),
                        )
                    if users_data != "all":
                        if len(users_data) == 1:
                            await editMessageReplyMarkup(
                                inline_message_id=msg_id,
                                reply_markup=whisper_seen_keys(
                                    user_id, from_user, time_data
                                ),
                            )
                        else:
                            name_user2 = None
                            if DataBase.hget(f"setting_whisper:{from_user}", "noname"):
                                name_user2 = langU["no_name"]
                            name_user = '<a href="tg://user?id={}">{}</a>'.format(
                                        user_id, msg.from_user.first_name
                                    )
                            if dispo_is_on:
                                inlineKeys = whisper_seen2_keys(
                                    from_user,
                                    from_user,
                                    time_data
                                )
                            else:
                                inlineKeys = whisper_seen_keys(
                                    user_id, from_user, time_data
                                )
                            await editText(
                                inline_msg_id=msg_id,
                                text=lang[lang_user(from_user)]["whisper_seened"].format(
                                    name_user2 or name_user
                                ),
                                parse_mode="html",
                                reply_markup=inlineKeys,
                            )
                        DataBase.sadd(
                            "whisper_seened:{}:{}".format(from_user, time_data),
                            user_id,
                        )
                    if str(users_data).isdigit() and not DataBase.get(
                        "whisper_seen_time:{}:{}".format(from_user, time_data)
                    ):
                        DataBase.set(
                            "whisper_seen_time:{}:{}".format(
                                from_user, time_data
                            ),
                            int(time()),
                        )
                        if dispo_is_on:
                            DataBase.srem(
                                "whisper_autodel",
                                f"{from_user}:{time_data}:{msg_id}"
                            )
                            DataBase.delete(hash_db)
                            DataBase.delete("whisper_special:{}".format(from_user))
                        elif DataBase.hget(
                            f"setting_whisper:{from_user}",
                            "autodel"
                        ):
                            DataBase.sadd(
                                "whisper_autodel",
                                f"{from_user}:{time_data}:{msg_id}",
                            )
                DataBase.incr(
                    "whisper_seen_count:{}:{}".format(from_user, time_data)
                )
            else:
                DataBase.sadd(
                    "whisper_nosy:{}:{}".format(from_user, time_data), user_id
                )
                await answerCallbackQuery(
                    msg,
                    langU["whisper_not_for_you"],
                    show_alert=True,
                    cache_time=3600,
                )
        if re.match(r"^delwhisper:(\d+):([-+]?\d*\.\d+|\d+)$", input):
            ap = re_matches(r"^delwhisper:(\d+):([-+]?\d*\.\d+|\d+)$", input)
            hash_db = "whisper:{}:{}".format(ap[1], ap[2])
            if user_id == int(ap[1]):
                seen_id = DataBase.hget(
                    hash_db, "seen_id"
                )
                if seen_id:
                    seen_id = seen_id.split(":")
                    await delete_messages(seen_id[0], seen_id[1])
                special_msgID = DataBase.hget(
                    "whisper_special:{}".format(ap[1]), "id"
                )
                DataBase.srem(
                    "whisper_autodel", f"{ap[1]}:{ap[2]}:{special_msgID}"
                )
                DataBase.delete(hash_db)
                DataBase.delete("whisper_special:{}".format(ap[1]))
                await answerCallbackQuery(msg, langU["whisper_deleted"])
                await editMessageReplyMarkup(
                    inline_message_id=msg_id,
                    reply_markup=whisper_seen2_keys(user_id, ap[1], ap[2]),
                )
            else:
                await answerCallbackQuery(
                    msg, langU["must_be_owner_whisper"],
                    show_alert=True, cache_time=3600
                )
        if re.match(r"^shows:(\d+):([-+]?\d*\.\d+|\d+)$", input):
            ap = re_matches(r"^shows:(\d+):([-+]?\d*\.\d+|\d+)$", input)
            from_user, time_data = ap[1], ap[2]
            if user_id != int(from_user):
                await answerCallbackQuery(
                    msg,
                    langU["must_be_owner_whisper"],
                    show_alert=True,
                    cache_time=3600,
                )
                return False
            seen_time = DataBase.get(
                "whisper_seen_time:{}:{}".format(from_user, time_data)
            )
            seen_count = DataBase.get(
                "whisper_seen_count:{}:{}".format(from_user, time_data)
            )
            seened_users = DataBase.smembers(
                "whisper_seened:{}:{}".format(from_user, time_data)
            )
            nosy_users = DataBase.smembers(
                "whisper_nosy:{}:{}".format(from_user, time_data)
            )
            if len(nosy_users) > 0:
                nosy_users_text = ""
                for i in nosy_users:
                    name_user = await userInfos(i, info="name")
                    nosy_users_text = "{}\n{}".format(
                        name_user, nosy_users_text
                    )
            else:
                nosy_users_text = langU["nobody_nosy"]
            if not seen_count:
                await answerCallbackQuery(
                    msg, langU["no_one_seen"], show_alert=True, cache_time=3
                )
            else:
                if seen_time:
                    ti_me = datetime.fromtimestamp(int(seen_time))
                    ti_me = ti_me.strftime("%Y-%m-%d %H:%M:%S")
                    ti_me = re_matches(
                        r"(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)", ti_me
                    )
                    if user_steps[user_id]["lang"] == "fa":
                        ti_me2 = gregorian_to_jalali(
                            int(ti_me[1]), int(ti_me[2]), int(ti_me[3])
                        )
                        seen_time = (
                            "{:04d}/{}/{:02d} - {:02d}:{:02d}:{:02d}".format(
                                ti_me2[0],
                                echoMonth(ti_me2[1], True),
                                ti_me2[2],
                                int(ti_me[4]),
                                int(ti_me[5]),
                                int(ti_me[6]),
                            )
                        )
                    else:
                        seen_time = (
                            "{:04d}/{}/{:02d} - {:02d}:{:02d}:{:02d}".format(
                                int(ti_me[1]),
                                echoMonth(ti_me[2], False),
                                int(ti_me[3]),
                                int(ti_me[4]),
                                int(ti_me[5]),
                                int(ti_me[6]),
                            )
                        )
                    name_user = list(
                        DataBase.smembers(
                            "whisper_seened:{}:{}".format(from_user, time_data)
                        )
                    )[0]
                    name_user = await userInfos(name_user, info="name")
                    await answerCallbackQuery(
                        msg,
                        langU["seen_whisper_person"].format(
                            seen_time,
                            seen_count,
                            name_user,
                            langU["nosies"].format(nosy_users_text),
                        ),
                        show_alert=True,
                        cache_time=3,
                    )
                else:
                    if len(seened_users) > 0:
                        seened_users_text = ""
                        for i in seened_users:
                            name_user = await userInfos(i, info="name")
                            seened_users_text = "{}\n{}".format(
                                name_user, seened_users_text
                            )
                        await answerCallbackQuery(
                            msg,
                            langU["seen_whisper_group"].format(
                                seen_count,
                                len(seened_users),
                                seened_users_text,
                                langU["nosies"].format(nosy_users_text),
                            ),
                            show_alert=True,
                            cache_time=3,
                        )
                    else:
                        await answerCallbackQuery(
                            msg,
                            langU["seen_whisper_all"].format(seen_count),
                            show_alert=True,
                            cache_time=3,
                        )
