# Lightweight Class Attendance Tracker for Telegram

I wrote this Telegram bot to assist my Judo dojo with class attendance tracking/RSVP. 

Our school isn't large enough to justify paying for a service like MindBody or ZenPlanner, and we already have an existing Telegram group chat.

This bot utilizes the existing polling feature in Telegram to act as a front end for similar features. Additionally, it will automatically generate CSV files to track who is attending your classes.

Setup:
1. install requirements.txt
2. Create Telegram bot (follow this guide: https://core.telegram.org/bots/tutorial)
3. create .env file with TOKEN as your API Token from Telegram's BotFather.
4. Add the bot to your group chat and give it admin rights.

Commands

/pollclass - sends a simple Yes/No poll to the group to see who will attend class that day.
/stoppoll - closes the poll and creates a CSV file with confirmed attendees.


 