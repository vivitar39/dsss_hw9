import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from transformers import pipeline

# --- Configuration ---
API_TOKEN = "7376680509:AAErXVIz3vIHwchMOUc_Pc9I6kvfQz2WpbY"
MODEL_NAME = "TinyLlama/TinyLlama-1.1B"  # Using TinyLlama

# --- Setup Logging ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Load the Language Model ---
try:
    generator = pipeline("text-generation", model="./TinyLlama-1.1B")
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    generator = None

# --- Command: Start ---
async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command."""
    await update.message.reply_text("Hi! I am your AI assistant Marvin. Ask me about any animal, and I’ll give you 5 fun facts!")


# --- Function: Generate Animal Facts ---
def generate_fact(animal_name):
    """Generates a structured list of fun facts about the given animal using TinyLlama."""
    if generator is None:
        return "Error: Language model is not loaded."

    prompt = (
        f"List exactly 5 fun and interesting facts about {animal_name}. "
        f"Format your response as a numbered list with 5 items and no extra text.\n\n"
        "1."
    )

    try:
        response = generator(prompt, max_length=250, truncation=True)
        text = response[0]['generated_text'].strip()

        # Ensure the response starts with "1."
        if "1." in text:
            text = text[text.index("1.") :].strip()

        # Extract exactly 5 facts by stopping at "6." if the model over-generates
        lines = text.split("\n")
        clean_facts = []
        for line in lines:
            if line.strip().startswith(("1.", "2.", "3.", "4.", "5.")):
                clean_facts.append(line.strip())

            # Stop once we have exactly 5 facts
            if len(clean_facts) == 5:
                break

        # Format the cleaned response
        formatted_response = "\n".join(clean_facts)

        return formatted_response if len(formatted_response) > 10 else "I couldn't find good facts about that animal."
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "Sorry, I couldn't generate a fact list right now."

# --- Message Handler ---
async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handles user messages."""
    user_message = update.message.text
    logger.info(f"Received message: {user_message}")

    # Extract animal name from user input
    if "about" in user_message.lower():
        animal_name = user_message.split("about")[-1].strip().strip("?")
    else:
        animal_name = user_message.strip()

    response = generate_fact(animal_name)

    # Send response to user
    await update.message.reply_text(response)


# --- Main Function ---
def main():
    """Start the bot."""
    app = Application.builder().token(API_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    logger.info("Bot is running...")
    app.run_polling()


# --- Run Bot ---
if __name__ == "__main__":
    main()
