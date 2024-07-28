db = 'Whisperbot'
# - - - - - - - - - - - - - #
telegram_datas = {
"botToken": "7135965418:AAHO8PkH4lYcEjFzn9K_Z6TG_12vQ0jfMOI",
"api_hash": "b51499523800add51e4530c6f552dbc8",
"api_id": 12962251,
"device_model": "Linux",
"system_version": "Ubuntu 22.04",
"app_version": "1.0",
}
# - - - - - - - - - - - - - #
sudo_users = (833360381, telegram_datas['botToken'].split(':')[0], ) # PUT_YOUR_ADMINS_HERE
# - - - - - - - - - - - - - #
IDs_datas = {
"sudo_id": 833360381,
"bot_id": int(telegram_datas['botToken'].split(':')[0]),
"chUsername": "MGIMT", # for force join
"chLink": "https://t.me/MGIMT", # for force join
}
# - - - - - - - - - - - - - #
server_datas = {
"ip": "142.93.127.111",
"port_server": 10128, #optional
"port_tg": 8443, #80, 88, 443, 8443 
}
# - - - - - - - - - - - - - #
sendApi = "https://api.telegram.org/bot{}/".format(telegram_datas['botToken'])
# - - - - - - - - - - - - - #
git_url = 'https://raw.githubusercontent.com/ferisystem/ferisystem/files/files'
pic_atsign = f'{git_url}/atsign.jpg'
pic_user = f'{git_url}/user.jpg'
pic_message = f'{git_url}/message.jpg'
pic_question = f'{git_url}/question.jpg'
pic_group = f'{git_url}/group.jpg'
pic_all = f'{git_url}/all.jpg'
pic_tick = f'{git_url}/tick.jpg'
pic_cross = f'{git_url}/cross.jpg'
pic_special = f'{git_url}/special.jpg'
