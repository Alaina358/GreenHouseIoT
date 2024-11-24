import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler
import paho.mqtt.client as mqtt
import json
import os

# Load environment variables
TOKEN = os.getenv("TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

# Initialize the bot using the new API
app = Application.builder().token(TOKEN).build()

# Global variables to track the mute state
alerts_muted = False

async def send_alert(sensor, value, greenhouse, habitat):
    """Sends an alert to Telegram when a threshold is exceeded."""
    global alerts_muted
    if alerts_muted:
        print("Alerts are muted. Skipping notification.")
        return
    message = (
        f"⚠️ *Alert: {sensor.upper()}* ⚠️\n"
        f"Value: `{value}`\n"
        f"Greenhouse: `{greenhouse}`\n"
        f"Habitat: `{habitat}`\n"
    )
    await app.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

def check_threshold(sensor, value):
    """Checks if a value exceeds the defined thresholds."""
    try:
        with open("thresholds.json", "r") as file:
            thresholds = json.load(file)
        if sensor in thresholds:
            min_val = thresholds[sensor]["min"]
            max_val = thresholds[sensor]["max"]
            return value < min_val or value > max_val
    except FileNotFoundError:
        print("Thresholds file not found.")
    except json.JSONDecodeError:
        print("Error decoding thresholds.json.")
    return False

def on_message(client, userdata, message):
    """Callback to handle incoming MQTT messages."""
    try:
        payload = message.payload.decode("utf-8").strip()
        if not payload:
            raise ValueError("Empty payload received")
        payload = json.loads(payload)

        topic_parts = message.topic.split("/")
        sensor = topic_parts[0]
        greenhouse = topic_parts[1]
        habitat = topic_parts[2]
        value = float(payload[sensor])

        print(f"Received {sensor}: {value} from {greenhouse}/{habitat}")

        if check_threshold(sensor, value):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(send_alert(sensor, value, greenhouse, habitat))
            loop.close()
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

def start_mqtt():
    """Conecta al broker MQTT y comienza a escuchar mensajes."""
    mqtt_client.connect("mqtt-broker", 1883)
    mqtt_client.subscribe("#")
    mqtt_client.loop_start()

# Command Handlers
async def start(update: Update, context):
    """Handles the /start command."""
    await update.message.reply_text("Hello! I'm monitoring your sensors. Use /help to view available commands.")

async def getthresholds(update: Update, context):
    """Handles the /getthresholds command."""
    try:
        with open("thresholds.json", "r") as file:
            thresholds = json.load(file)
        message = "Current Thresholds:\n"
        for sensor, values in thresholds.items():
            message += f"{sensor}: Min = {values['min']}, Max = {values['max']}\n"
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"Error fetching thresholds: {e}")

async def setthreshold(update: Update, context):
    """Handles the /setthresholds command."""
    try:
        args = context.args
        if len(args) != 3:
            await update.message.reply_text("Usage: /setthreshold [sensor] [min] [max]")
            return
        sensor, min_val, max_val = args[0], float(args[1]), float(args[2])
        with open("thresholds.json", "r") as file:
            thresholds = json.load(file)
        thresholds[sensor] = {"min": min_val, "max": max_val}
        with open("thresholds.json", "w") as file:
            json.dump(thresholds, file, indent=4)
        await update.message.reply_text(f"Thresholds updated for {sensor}: Min = {min_val}, Max = {max_val}")
    except Exception as e:
        await update.message.reply_text(f"Error setting thresholds: {e}")

async def mute(update: Update, context):
    """Handles the /mute command to stop sending alerts."""
    global alerts_muted
    alerts_muted = True
    await update.message.reply_text("Alerts have been muted.")

async def unmute(update: Update, context):
    """Handles the /unmute command to resume sending alerts."""
    global alerts_muted
    alerts_muted = False
    await update.message.reply_text("Alerts have been unmuted.")

async def help(update: Update, context):
    """Handles the /help command to display available commands."""
    commands = """
Available Commands:
/start - Start the bot
/getthresholds - View current thresholds
/setthreshold [sensor] [min] [max] - Update thresholds for a sensor
/mute - Stop receiving alerts
/unmute - Resume receiving alerts
/help - Show this help message
"""
    await update.message.reply_text(commands)

# Register Command Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("getthresholds", getthresholds))
app.add_handler(CommandHandler("setthreshold", setthreshold))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("unmute", unmute))
app.add_handler(CommandHandler("help", help))

# Configurar handlers usando la nueva API
app.add_handler(CommandHandler("start", start))
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

# Start MQTT and the bot
start_mqtt()

# Run the bot
if __name__ == "__main__":
    app.run_polling()
