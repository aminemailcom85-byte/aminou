"""
ربات روبیکا - ارسال پیام خودکار به گروه‌ها و جذب ممبر
"""

import asyncio
import logging
from datetime import datetime
from rubka import Robot, Message
from config import (
    BOT_TOKEN,
    PROMO_MESSAGE,
    SEND_INTERVAL,
    GROUP_IDS,
    WELCOME_MESSAGE,
    DEBUG,
)

# ──────────────────────────────────────────────
# تنظیم لاگینگ
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("RubikaBot")

# ──────────────────────────────────────────────
# ساخت ربات
# ──────────────────────────────────────────────
bot = Robot(BOT_TOKEN)

# ──────────────────────────────────────────────
# ذخیره گروه‌ها (برای ارسال خودکار)
# ──────────────────────────────────────────────
active_groups = set(GROUP_IDS)


# ══════════════════════════════════════════════
#  📌 دستور /start - شروع ربات
# ══════════════════════════════════════════════
@bot.on_message(commands=["start"])
def start_handler(bot: Robot, message: Message):
    """پاسخ به دستور /start"""
    user_name = message.sender_id
    logger.info(f"User started bot: {user_name}")

    message.reply(
        "🤖 سلام! من ربات ارسال پیام خودکار هستم.\n\n"
        "📌 دستورات من:\n"
        "/start - شروع ربات\n"
        "/groups - نمایش گروه‌های فعال\n"
        "/add_group <آیدی> - اضافه کردن گروه\n"
        "/remove_group <آیدی> - حذف گروه\n"
        "/promo_message - نمایش پیام تبلیغاتی فعلی\n"
        "/set_message - تغییر پیام تبلیغاتی\n"
        "/send_now - ارسال فوری پیام به همه گروه‌ها\n"
        "/status - وضعیت ربات\n"
    )


# ══════════════════════════════════════════════
#  📌 دستور /groups - نمایش گروه‌های فعال
# ══════════════════════════════════════════════
@bot.on_message(commands=["groups"])
def groups_handler(bot: Robot, message: Message):
    """نمایش لیست گروه‌های فعال"""
    if not active_groups:
        message.reply("❌ هیچ گروهی ثبت نشده است.\n\nبرای اضافه کردن گروه از دستور /add_group استفاده کنید.")
        return

    groups_text = "📋 گروه‌های فعال:\n\n"
    for i, group_id in enumerate(active_groups, 1):
        groups_text += f"{i}. `{group_id}`\n"

    message.reply(groups_text)


# ══════════════════════════════════════════════
#  📌 دستور /add_group - اضافه کردن گروه
# ══════════════════════════════════════════════
@bot.on_message(commands=["add_group"])
def add_group_handler(bot: Robot, message: Message):
    """اضافه کردن گروه جدید"""
    text = message.text
    parts = text.split()

    if len(parts) < 2:
        message.reply("❌ لطفاً آیدی گروه را وارد کنید.\n\nمثال: /add_group g0ABCDEF1234567890")
        return

    group_id = parts[1]
    active_groups.add(group_id)
    logger.info(f"Group added: {group_id}")

    message.reply(f"✅ گروه `{group_id}` با موفقیت اضافه شد!")


# ══════════════════════════════════════════════
#  📌 دستور /remove_group - حذف گروه
# ══════════════════════════════════════════════
@bot.on_message(commands=["remove_group"])
def remove_group_handler(bot: Robot, message: Message):
    """حذف گروه از لیست"""
    text = message.text
    parts = text.split()

    if len(parts) < 2:
        message.reply("❌ لطفاً آیدی گروه را وارد کنید.\n\nمثال: /remove_group g0ABCDEF1234567890")
        return

    group_id = parts[1]
    if group_id in active_groups:
        active_groups.discard(group_id)
        logger.info(f"Group removed: {group_id}")
        message.reply(f"✅ گروه `{group_id}` حذف شد.")
    else:
        message.reply(f"❌ گروه `{group_id}` در لیست وجود ندارد.")


# ══════════════════════════════════════════════
#  📌 دستور /promo_message - نمایش پیام فعلی
# ══════════════════════════════════════════════
@bot.on_message(commands=["promo_message"])
def promo_message_handler(bot: Robot, message: Message):
    """نمایش پیام تبلیغاتی فعلی"""
    message.reply(f"📝 پیام تبلیغاتی فعلی:\n\n{PROMO_MESSAGE}")


# ══════════════════════════════════════════════
#  📌 دستور /send_now - ارسال فوری
# ══════════════════════════════════════════════
@bot.on_message(commands=["send_now"])
def send_now_handler(bot: Robot, message: Message):
    """ارسال فوری پیام به همه گروه‌ها"""
    if not active_groups:
        message.reply("❌ هیچ گروهی ثبت نشده است.")
        return

    message.reply(f"⏳ در حال ارسال پیام به {len(active_groups)} گروه...")
    sent_count = send_promo_to_all_groups()
    message.reply(f"✅ پیام با موفقیت به {sent_count} گروه ارسال شد!")


# ══════════════════════════════════════════════
#  📌 دستور /status - وضعیت ربات
# ══════════════════════════════════════════════
@bot.on_message(commands=["status"])
def status_handler(bot: Robot, message: Message):
    """نمایش وضعیت ربات"""
    status_text = (
        f"📊 وضعیت ربات:\n\n"
        f"🔄 وضعیت: فعال ✅\n"
        f"👥 تعداد گروه‌ها: {len(active_groups)}\n"
        f"⏰ فاصله ارسال: {SEND_INTERVAL} ثانیه\n"
        f"📅 زمان فعلی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    message.reply(status_text)


# ══════════════════════════════════════════════
#  📌 پیام خوش‌آمدگویی برای اعضای جدید
# ══════════════════════════════════════════════
@bot.on_message()
def welcome_handler(bot: Robot, message: Message):
    """ارسال پیام خوش‌آمدگویی برای اعضای جدید"""
    try:
        # بررسی آیا پیام از نوع عضو جدید است
        if message.sender_type == "User":
            user_name = bot.get_name(message.sender_id) or "کاربر عزیز"
            welcome_text = WELCOME_MESSAGE.format(user_name=user_name)

            # ارسال پیام خوش‌آمدگویی
            message.reply(welcome_text)
            logger.info(f"Welcome message sent to user: {user_name}")
    except Exception as e:
        logger.error(f"Error in welcome handler: {e}")


# ══════════════════════════════════════════════
#  📌 تابع ارسال پیام به همه گروه‌ها
# ══════════════════════════════════════════════
def send_promo_to_all_groups() -> int:
    """ارسال پیام تبلیغاتی به تمام گروه‌های فعال"""
    sent_count = 0
    for group_id in active_groups:
        try:
            bot.send_message(
                chat_id=group_id,
                text=PROMO_MESSAGE,
            )
            sent_count += 1
            logger.info(f"Message sent to group: {group_id}")
        except Exception as e:
            logger.error(f"Failed to send message to group {group_id}: {e}")

    return sent_count


# ══════════════════════════════════════════════
#  📌 تابع ارسال خودکار پیام‌ها
# ══════════════════════════════════════════════
async def auto_send_loop():
    """حلقه ارسال خودکار پیام‌ها"""
    while True:
        await asyncio.sleep(SEND_INTERVAL)
        if active_groups:
            logger.info("Starting auto-send...")
            sent = send_promo_to_all_groups()
            logger.info(f"Auto-send completed. Sent to {sent} groups.")


# ══════════════════════════════════════════════
#  📌 اجرای ربات
# ══════════════════════════════════════════════
if __name__ == "__main__":
    logger.info("Starting Rubika Promo Bot...")
    logger.info(f"Active groups: {len(active_groups)}")
    logger.info(f"Send interval: {SEND_INTERVAL} seconds")

    # اجرای ربات و حلقه ارسال خودکار
    loop = asyncio.get_event_loop()
    loop.create_task(auto_send_loop())
    bot.run()
