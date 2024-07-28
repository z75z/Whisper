from whisperbot.keyboards_func import *
from whisperbot.lateral_func import *
from whisperbot.main_func import *
from config_bot import *
from core_file import *


async def inline_query_process(msg: types.InlineQuery):
    msg_id = msg.id
    user_id = msg.from_user.id
    if msg.from_user.username:
        username = f"@{msg.from_user.username}"
    else:
        username = user_id
    user_name = msg.from_user.first_name
    chat_type = msg.chat_type
    input = msg.query
    saveUsername(msg, mode="inline")
    setupUserSteps(msg, user_id)
    langU = lang[lang_user(user_id)]
    buttuns = langU["buttuns"]
    ln_in = langU["inline"]
    print(colored("Inline >", "cyan"))
    print(colored("userID", "yellow"), colored(user_id, "white"))
    print(colored("Query", "yellow"), colored(input, "white"))
    print(colored("inlineID", "yellow"), colored(msg_id, "white"))
    print()
    if input == "":
        input_content = InputTextMessageContent(
            message_text=ln_in["text"]["help_send"].format(GlobalValues().botUser),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["help_comp"],
                url="t.me/{}?start=help".format(GlobalValues().botUser),
            )
        )
        item1 = InlineQueryResultArticle(
            id=f"help:{user_id}",
            title=ln_in["title"]["help_send"],
            description=ln_in["desc"]["help_send"],
            thumb_url=pic_question,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        input_content = InputTextMessageContent(
            message_text=ln_in["text"]["my_id"].format(user_id),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["whisper_to"].format(user_name),
                switch_inline_query_current_chat="{} {}".format(
                    username, buttuns["example"]
                ),
            )
        )
        item2 = InlineQueryResultArticle(
            id=f"myid:{user_id}",
            title=ln_in["title"]["my_id"],
            description=ln_in["desc"]["my_id"].format(user_id),
            thumb_url=pic_atsign,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        await answerInlineQuery(msg_id, results=[item1, item2], cache_time=1)
    if not re.findall(r"@all", input.lower()) and (
        re.search(r"(?:(?<!\d)\d{6,10}(?!\d)) (.*)$", input)
        or re.search(r"(@[a-zA-Z0-9_]*) (.*)$", input)
    ):
        ap = re.findall(r"(@[a-zA-Z0-9_]*)", input)
        ap2 = re.findall(r"(?:(?<!\d)\d{6,10}(?!\d))", input)
        text = input
        users = set()
        for i in ap:
            text = text.replace(f"{i} ", "").replace(f"{i}", "")
            users.add(i)
        for i in ap2:
            text = text.replace(f"{i} ", "").replace(f"{i}", "")
            users.add(i)
        users = list(users)
        ti_me = time()
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["show_whisper"],
                callback_data="showN:{}:{}".format(user_id, ti_me),
            )
        )
        ads = DataBase.get("have_ads")
        if ads:
            inlineKeys.add(
                iButtun(
                    DataBase.hget("info_ads", "buttuns"),
                    url=DataBase.hget("info_ads", "url"),
                )
            )
        if text == "":
            input_content = InputTextMessageContent(
                message_text=ln_in["text"]["whisper_havn_text"],
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            item1 = InlineQueryResultArticle(
                id="null",
                title=ln_in["title"]["whisper_havn_text"],
                description=ln_in["desc"]["whisper_havn_text"],
                thumb_url=pic_cross,
                thumb_width=512,
                thumb_height=512,
                input_message_content=input_content,
            )
            return await answerInlineQuery(
                msg_id,
                results=[
                    item1,
                ],
                cache_time=1,
            )
        if len(users) > 1:
            name_users = ""
            count = 0
            for i in users:
                if "@" in i:
                    k = await userIds(i)
                    if k:
                        users[count] = k
                count += 1
            for i in users:
                name_user = await userInfos(i, info="name")
                if str(i).isdigit():
                    name_users = '<a href="tg://user?id={}">{}</a>\n{}'.format(
                        i, name_user, name_users
                    )
                else:
                    name_users = "{}\n{}".format(name_user, name_users)
            input_content = InputTextMessageContent(
                message_text=ln_in["text"]["whisper_group"].format(
                    len(users), name_users
                ),
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            item1 = InlineQueryResultArticle(
                id=f"whisperP:{user_id}",
                title=ln_in["title"]["whisper_group"].format(
                    len(users)
                ),
                description=ln_in["desc"]["whisper_group"].format(
                    len(text)
                ),
                thumb_url=pic_group,
                thumb_width=512,
                thumb_height=512,
                input_message_content=input_content,
                reply_markup=inlineKeys,
            )
        else:
            if "@" in users[0]:
                k = await userIds(users[0])
                if k:
                    users[0] = k
            name_user2 = None
            if DataBase.hget(f"setting_whisper:{user_id}", "noname"):
                name_user2 = langU["no_name"]
            name_user = await userInfos(users[0], info="name")
            input_content = InputTextMessageContent(
                message_text=ln_in["text"]["whisper_person"].format(
                    name_user2 or name_user
                ),
                parse_mode="HTML",
                disable_web_page_preview=False,
            )
            item1 = InlineQueryResultArticle(
                id=f"whisperP:{user_id}",
                title=ln_in["title"]["whisper_person"].format(
                    name_user
                ),
                description=ln_in["desc"]["whisper_person"].format(
                    len(text)
                ),
                thumb_url=pic_message,
                thumb_width=512,
                thumb_height=512,
                input_message_content=input_content,
                reply_markup=inlineKeys,
            )
        user_steps[user_id].update(
            {
                "whisper": {
                    "time": ti_me,
                    "text": text,
                    "users": users,
                }
            }
        )
        await answerInlineQuery(
            msg_id,
            results=[
                item1,
            ],
            cache_time=1,
        )
    if re.search(r"@[Aa][Ll][Ll] (.*)$", input) or re.search(
        r"@[Aa][Ll][Ll] (.*)$", input
    ):
        ap = re.findall(r"@[Aa][Ll][Ll] (.*)$", input)
        text = ap[0]
        ti_me = time()
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["stats"],
                callback_data="showS:{}:{}".format(user_id, ti_me),
            ),
            iButtun(
                buttuns["show_whisper"],
                callback_data="showN:{}:{}".format(user_id, ti_me),
            ),
        )
        ads = DataBase.get("have_ads")
        if ads:
            inlineKeys.add(
                iButtun(
                    DataBase.hget("info_ads", "buttuns"),
                    url=DataBase.hget("info_ads", "url"),
                )
            )
        input_content = InputTextMessageContent(
            message_text=ln_in["text"]["whisper_all"],
            parse_mode="HTML",
            disable_web_page_preview=False,
        )
        item1 = InlineQueryResultArticle(
            id=f"whisperA:{user_id}",
            title=ln_in["title"]["whisper_all"],
            description=ln_in["desc"]["whisper_all"].format(len(text)),
            thumb_url=pic_all,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        input_content = InputTextMessageContent(
            message_text=ln_in["text"]["whisper_all2"],
            parse_mode="HTML",
            disable_web_page_preview=False,
        )
        item2 = InlineQueryResultArticle(
            id=f"whisperA2:{user_id}",
            title=ln_in["title"]["whisper_all"],
            description=ln_in["desc"]["whisper_all2"].format(
                len(text)
            ),
            thumb_url=pic_all,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        user_steps[user_id].update(
            {
                "whisper": {
                    "time": ti_me,
                    "text": text,
                    "users": "all",
                }
            }
        )
        await answerInlineQuery(msg_id, results=[item1, item2], cache_time=1)
    if re.search(r"set$", input.lower()):
        set_desc = ln_in["desc"]
        set_title = {}
        set_photo = {}
        items = []
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["quick_set"], switch_inline_query_current_chat="set"
            )
        )
        input_content = InputTextMessageContent(
            message_text=ln_in["text"]["setting_changed"],
            parse_mode="HTML",
            disable_web_page_preview=False,
        )
        for i in ("seen", "recv", "encrypt", "noname", "dispo", "antisave"):
            if DataBase.hget(f"setting_whisper:{user_id}", i):
                status = langU["is_power_on"]
                set_title[i] = ln_in["title"]["power_off"]
                set_photo[i] = pic_tick
            else:
                status = langU["is_power_off"]
                set_title[i] = ln_in["title"]["power_on"]
                set_photo[i] = pic_cross
            item = InlineQueryResultArticle(
                id=f"set:{i}:{user_id}",
                title=set_title[i],
                description=set_desc[f"whisper_{i}"].format(status),
                thumb_url=set_photo[i],
                thumb_width=512,
                thumb_height=512,
                input_message_content=input_content,
                reply_markup=inlineKeys,
            )
            items.append(item)
        await answerInlineQuery(
            msg_id,
            items,
            1,
            ln_in["title"]["all_set"],
            "set",
        )
    if (
        not re.findall(r"@all", input.lower())
        and not re.findall(r"(?:(?<!\d)\d{6,10}(?!\d))", input)
        and not re.findall(r"(@[a-zA-Z0-9_]*)", input)
        and chat_type == "supergroup"
    ):
        ap = re_matches(r"(.*)", input)
        text = ap[1]
        ti_me = time()
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["show_whisper"],
                callback_data="showN2:{}:{}".format(user_id, ti_me),
            )
        )
        ads = DataBase.get("have_ads")
        if ads:
            inlineKeys.add(
                iButtun(
                    DataBase.hget("info_ads", "buttuns"),
                    url=DataBase.hget("info_ads", "url"),
                )
            )
        input_content = InputTextMessageContent(
            message_text=ln_in["text"]["whisper_reply"],
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        item1 = InlineQueryResultArticle(
            id=f"whisperR:{user_id}",
            title=ln_in["title"]["whisper_reply"],
            description=ln_in["desc"]["whisper_reply"],
            thumb_url=pic_message,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        user_steps[user_id].update(
            {
                "whisper": {
                    "time": ti_me,
                    "text": text,
                    "users": "reply",
                }
            }
        )
        await answerInlineQuery(
            msg_id,
            results=[
                item1,
            ],
            cache_time=1,
        )
    if not re.findall(r"@all", input.lower()) and (
        re.search(r"^(?:(?<!\d)\d{6,10}(?!\d))$", input)
        or re.search(r"^(@[a-zA-Z0-9_]*)$", input)
    ):
        ap1 = re.findall(r"(@[a-zA-Z0-9_]*)", input)
        ap2 = re.findall(r"(?:(?<!\d)\d{6,10}(?!\d))", input)
        ap = ap1 or ap2
        user = ap[0]
        ti_me = time()
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                "{} - {}".format(GlobalValues().botName, GlobalValues().botUser),
                url="t.me/{}".format(GlobalValues().botUser),
            )
        )
        ads = DataBase.get("have_ads")
        if ads:
            inlineKeys.add(
                iButtun(
                    DataBase.hget("info_ads", "buttuns"),
                    url=DataBase.hget("info_ads", "url"),
                )
            )
        input_content = InputTextMessageContent(
            message_text=ln_in["text"]["whisper_havn_text"],
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        item2 = InlineQueryResultArticle(
            id="null",
            title=ln_in["title"]["whisper_havn_text"],
            description=ln_in["desc"]["whisper_havn_text"],
            thumb_url=pic_cross,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
        )
        if "@" in user:
            name_user = await userIds(user)
            user = name_user
        else:
            name_user = user
        name_user2 = None
        if DataBase.hget(f"setting_whisper:{user_id}", "noname"):
            name_user2 = langU["no_name"]
        name_user = await userInfos(name_user, info="name")
        input_content = InputTextMessageContent(
            message_text=ln_in["text"]["whisper_special"].format(
                name_user2 or name_user
            ),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        item1 = InlineQueryResultArticle(
            id=f"whisperS:{user_id}",
            title=ln_in["title"]["whisper_special"].format(name_user),
            description=ln_in["desc"]["whisper_special"],
            thumb_url=pic_special,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        user_steps[user_id].update(
            {
                "whisper": {
                    "time": ti_me,
                    "text": None,
                    "users": user,
                }
            }
        )
        await answerInlineQuery(msg_id, results=[item1, item2], cache_time=1)
    if re.match(r"sp(\d+)\.(\d+)\.(\d+)", input):
        ap = re_matches(r"sp(\d+)\.(\d+)\.(\d+)", input)
        from_user = ap[1]
        time_data = float(f"{ap[2]}.{ap[3]}")
        special_msgID = DataBase.hget(
            "whisper_special:{}".format(from_user), "id"
        )
        users_data = DataBase.hget(
            "whisper:{}:{}".format(from_user, time_data), "users"
        )
        if not str(user_id) in users_data and not str(username) in users_data:
            if special_msgID:
                return DataBase.sadd(
                    "whisper_nosy:{}:{}".format(from_user, time_data), user_id
                )
            else:
                return False
        if not special_msgID:
            input_content = InputTextMessageContent(
                message_text=ln_in["text"]["special_404"],
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            item1 = InlineQueryResultArticle(
                id="null",
                title=ln_in["title"]["special_404"],
                description=ln_in["desc"]["special_404"],
                thumb_url=pic_cross,
                thumb_width=512,
                thumb_height=512,
                input_message_content=input_content,
            )
            await answerInlineQuery(
                msg_id,
                results=[
                    item1,
                ],
                cache_time=3600,
            )
        file_id = DataBase.hget(
            "whisper:{}:{}".format(from_user, time_data), "file_id"
        )
        file_type = DataBase.hget(
            "whisper:{}:{}".format(from_user, time_data), "file_type"
        )
        source_id = DataBase.hget(
            "whisper:{}:{}".format(from_user, time_data), "source_id"
        )
        msg_ID = DataBase.hget(
            "whisper:{}:{}".format(from_user, time_data), "msg_id"
        )
        input_content = InputTextMessageContent(
            message_text=langU["cant_send_hide"],
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        item1 = None
        if file_type == "photo":
            item1 = InlineQueryResultCachedPhoto(
                id="null",
                photo_file_id=file_id,
                input_message_content=input_content,
            )
        elif file_type == "video":
            item1 = InlineQueryResultCachedVideo(
                id="null",
                title=" ",
                video_file_id=file_id,
                input_message_content=input_content,
            )
        elif file_type == "voice":
            item1 = InlineQueryResultCachedVoice(
                id="null",
                title=" ",
                voice_file_id=file_id,
                input_message_content=input_content,
            )
        elif file_type == "sticker":
            item1 = InlineQueryResultCachedSticker(
                id="null",
                sticker_file_id=file_id,
                input_message_content=input_content,
            )
        elif file_type == "animation":
            item1 = InlineQueryResultCachedGif(
                id="null",
                gif_file_id=file_id,
                input_message_content=input_content,
            )
        if item1:
            if DataBase.hget(
                f"setting_whisper:{from_user}", "seen"
            ) and not DataBase.get(
                "notif_before:{}:{}".format(from_user, time_data)
            ):
                DataBase.set(
                    "notif_before:{}:{}".format(from_user, time_data), 1
                )
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
                if DataBase.hget(f"setting_whisper:{from_user}", "dispo"):
                    special_msgID = DataBase.hget(
                        "whisper_special:{}".format(from_user), "id"
                    )
                    DataBase.srem(
                        "whisper_autodel",
                        f"{from_user}:{time_data}:{special_msgID}",
                    )
                    DataBase.delete("whisper:{}:{}".format(from_user, time_data))
                    DataBase.delete("whisper_special:{}".format(from_user))
            await answerInlineQuery(
                msg_id,
                results=[
                    item1,
                ],
                is_personal=True,
                cache_time=3600,
            )
    if re.match(r"^\*$", input):
        users = DataBase.smembers(f"whisper_recent2:{user_id}")
        if len(users) == 0:
            return False
        users = list(users)
        ti_me = time()
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                "{} - {}".format(GlobalValues().botName, GlobalValues().botUser),
                url="t.me/{}".format(GlobalValues().botUser),
            )
        )
        ads = DataBase.get("have_ads")
        if ads:
            inlineKeys.add(
                iButtun(
                    DataBase.hget("info_ads", "buttuns"),
                    url=DataBase.hget("info_ads", "url"),
                )
            )
        items = []
        count = 0
        for user in users:
            count += 1
            if count > 5:
                break
            name_user = user
            name_user2 = None
            if DataBase.hget(f"setting_whisper:{user_id}", "noname"):
                name_user2 = langU["no_name"]
            name_user = await userInfos(name_user, info="name")
            input_content = InputTextMessageContent(
                message_text=ln_in["text"]["whisper_special"].format(
                    name_user2 or name_user
                ),
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            # have_prof = DataBase.hget('userProfs', user)
            # if have_prof:
                # file_path = f"docs/profiles/{user}.jpg"
            # else:
                # file_path = pic_user
            file_path = pic_user
            item1 = InlineQueryResultArticle(
                id=f"whisperS:{user_id}:{user}",
                title=ln_in["title"]["whisper_special"].format(
                    name_user
                ),
                description=ln_in["desc"]["whisper_special"],
                thumb_url=file_path,
                thumb_width=512,
                thumb_height=512,
                input_message_content=input_content,
                reply_markup=inlineKeys,
            )
            items.append(item1)
        user_steps[user_id].update(
            {
                "whisper": {
                    "time": ti_me,
                    "text": None,
                    "users": "x",
                }
            }
        )
        await answerInlineQuery(msg_id, results=items, cache_time=1)
    if re.match(r"^me$", input):
        input_content = InputTextMessageContent(
            message_text=ln_in["text"]["my_id"].format(user_id),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        inlineKeys = iMarkup()
        inlineKeys.add(
            iButtun(
                buttuns["whisper_to"].format(user_name),
                switch_inline_query_current_chat="{} {}".format(
                    username, buttuns["example"]
                ),
            )
        )
        item1 = InlineQueryResultArticle(
            id=f"myid:{user_id}",
            title=ln_in["title"]["my_id"],
            description=ln_in["desc"]["my_id"].format(user_id),
            thumb_url=pic_atsign,
            thumb_width=512,
            thumb_height=512,
            input_message_content=input_content,
            reply_markup=inlineKeys,
        )
        await answerInlineQuery(msg_id, results=[item1, ], cache_time=1)