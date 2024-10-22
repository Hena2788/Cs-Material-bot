import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to start the bot and show subject buttons
async def start(update: Update, context) -> None:
    keyboard = [
        [InlineKeyboardButton("Data Structures", callback_data='subject_ds')],  # Changed to DS
        [InlineKeyboardButton("Algorithms", callback_data='subject_algorithms')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the St'mary's CS Material Bot! Choose a subject:", reply_markup=reply_markup)

# Function to handle subject selection and show chapter buttons
async def button(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()

    keyboard = []  # Initialize keyboard

    # Check if a subject was selected
    if query.data.startswith('subject_'):
        subject = query.data[len('subject_'):]  # Extract subject correctly

        # Initialize keyboard for chapters based on selected subject
        if subject == "ds":  # Changed to DS
            keyboard = [
                [InlineKeyboardButton("Chapter 1", callback_data='chapter_ds_ch1')],
                [InlineKeyboardButton("Chapter 2", callback_data='chapter_ds_ch2')],
            ]
        elif subject == "algorithms":
            keyboard = [
                [InlineKeyboardButton("Chapter 1", callback_data='chapter_algorithms_ch1')],
                [InlineKeyboardButton("Chapter 2", callback_data='chapter_algorithms_ch2')],
                [InlineKeyboardButton("Chapter 3", callback_data='chapter_algorithms_ch3')],
                [InlineKeyboardButton("Chapter 4", callback_data='chapter_algorithms_ch4')],
                [InlineKeyboardButton("Chapter 5", callback_data='chapter_algorithms_ch5')],
                [InlineKeyboardButton("Chapter 6", callback_data='chapter_algorithms_ch6')],
                [InlineKeyboardButton("Chapter 7", callback_data='chapter_algorithms_ch7')],
            ]

        print(f"Selected subject: {subject}")  # Debugging output

        # If the keyboard is defined, update the message
        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"Selected subject: {subject.replace('_', ' ').capitalize()}. Now choose a chapter:", reply_markup=reply_markup)
        else:
            await query.edit_message_text("Invalid subject selected.")

    # Handle chapter selection and send materials
    elif query.data.startswith('chapter_'):
        parts = query.data.split('_')  # Split the callback data
        subject = parts[1]  # Get the subject (ds or algorithms)
        chapter = parts[2]  # Get the chapter (e.g., ch1, ch2)

        materials = get_materials(subject, chapter)

        print(f"Materials requested for Subject: {subject}, Chapter: {chapter}")  # Debugging output

        if materials:
            await query.edit_message_text('\n'.join(materials))
        else:
            await query.edit_message_text(f"No materials found for {subject.replace('_', ' ').capitalize()} - {chapter.replace('ch', 'Chapter ')}.")

# Function to get materials based on subject and chapter
def get_materials(subject, chapter):
    # Replace this with actual logic to fetch materials for each chapter
    materials_dict = {
        "ds": {
            "ch1": ["Data Structures Chapter 1: https://docs.google.com/document/d/13tfvJNQ0hIgbvwOzTT1HUQL4PsLtytazzUWILc8KdvQ/edit?usp=drivesdk"],
            "ch2": ["Data Structures Chapter 2: https://drive.google.com/file/d/1CfYAfz3tDXo_3cl6ysavRq_-VUZ2ucrs/view?usp=drivesdk"],
        },
        "algorithms": {
            "ch1": ["Algorithms Chapter 1: https://docs.google.com/presentation/d/1iFELQgbvePIKvaDDZ2EKxiFit547DNBL/edit?usp=drive_link&ouid=106695099869951681358&rtpof=true&sd=true"],
            "ch2": ["Algorithms Chapter 2: https://docs.google.com/presentation/d/1Kh0xjNDmyDCFZO7gpwDOA3nh5elJBMBf/edit?usp=drive_link&ouid=106695099869951681358&rtpof=true&sd=true"],
            "ch3": ["Algorithms Chapter 3: https://docs.google.com/presentation/d/1q12WT3tO5qrTDO0lOk47VUBOBzyWFOXt/edit?usp=drive_link&ouid=106695099869951681358&rtpof=true&sd=true"],
            "ch4": ["Algorithms Chapter 4: https://docs.google.com/presentation/d/1zMHL3eNR7WN-_Kzjpx6C4qHqO6yxOJmT/edit?usp=drive_link&ouid=106695099869951681358&rtpof=true&sd=true"],
            "ch5": ["Algorithms Chapter 5: https://docs.google.com/presentation/d/14u4DHg0rfXyCUcS-uPJF-Ndlw3cTTW3y/edit?usp=drive_link&ouid=106695099869951681358&rtpof=true&sd=true"],
            "ch6": ["Algorithms Chapter 6: https://docs.google.com/presentation/d/1-eM43a98KK4jbI1M3_iTZ8NIAmk1369T/edit?usp=drive_link&ouid=106695099869951681358&rtpof=true&sd=true"],
            "ch7": ["Algorithms Chapter 7: https://docs.google.com/presentation/d/1d4krKzA_h0l_4I4L2ucSkmp56hM5bZU8/edit?usp=drive_link&ouid=106695099869951681358&rtpof=true&sd=true"],
        }
    }
    return materials_dict.get(subject, {}).get(chapter, [])

def main():
    # Load the token from .env file
    TOKEN = os.getenv("TOKEN")

    if not TOKEN:
        raise ValueError("No TOKEN found. Please set it in the .env file.")

    # Create the Application instance
    application = Application.builder().token(TOKEN).build()

    # Add command and callback query handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
