import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, PollAnswerHandler, CallbackContext
from dotenv import load_dotenv
from datetime import datetime
import csv

load_dotenv()
TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

yes_list = []

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    chat_admins = await context.bot.get_chat_administrators(chat_id)
    for admin in chat_admins:
        if admin.user.id == user_id:
            return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Let's do some Judo. Type '/pollclass' to see who is training today")
  

async def poll_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = "Are you attending class tonight?/Partecipi alla lezione stasera?"
    options = ["Yes", "No"]
    if await is_admin(update, context):
        message = await context.bot.send_poll(
            chat_id=update.effective_chat.id,
            question=question,
            options=options,
            is_anonymous=False
        )
        payload = {
            message.poll.id: {
                "questions": question,
                "message_id": message.message_id,
                "chat_id": update.effective_chat.id,
            }
        }
        context.bot_data['poll_message_id'] = message.message_id
        context.bot_data.update(payload)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Admnistrators only")

#write method to collect poll results and send them to the admin (mostly copied from example pollbot.py)
async def receive_answers(update: Update, context: CallbackContext):
    answer = update.poll_answer
    answered_poll = context.bot_data[answer.poll_id]
    try:
        questions = answered_poll["questions"]
    except KeyError:
        return
    selected_options = answer.option_ids
    for question_id in selected_options:
        if question_id == selected_options[0]:
            student_name = {"first name":answer.user.first_name, "last name": answer.user.last_name}
            yes_list.append(student_name)


async def stop_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await is_admin(update, context):
        if 'poll_message_id' in context.bot_data:
            await context.bot.stop_poll(
                chat_id=update.effective_chat.id,
                message_id=context.bot_data['poll_message_id']
            )
            
            print(yes_list)
            write_attendance(yes_list)
            yes_list.clear()

        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="No poll to stop")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Admnistrators only")
 
def write_attendance(list):

    now = datetime.now()
    attendence_dir = 'attendance'
    year_dir = os.path.join(attendence_dir, str(now.year))
    month_dir = os.path.join(year_dir, f"{now.month:02d}")
    os.makedirs(month_dir, exist_ok=True)

    filename = f"{now.year}-{now.month:02d}-{now.day:02d}.csv"
    filepath = os.path.join(month_dir, filename)

    with open(filepath, mode='w', newline='') as file:
        fieldnames = ['first name', 'last name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(list)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    poll_handler = CommandHandler('pollclass', poll_class)
    stop_poll_handler = CommandHandler('stoppoll', stop_poll)

    application.add_handler(start_handler)
    application.add_handler(poll_handler)
    application.add_handler(stop_poll_handler)
    application.add_handler(PollAnswerHandler(receive_answers))

    application.run_polling()
