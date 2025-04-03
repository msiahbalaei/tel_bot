const TelegramBot = require('node-telegram-bot-api');
const schedule = require('node-schedule');

// ???? ???? ? ????? ?????
const TOKEN = process.env.TOKEN || '7243834241:AAHgRWMIQ6Y6DvWhFvkFMwEL4Kjehx7mr94';
const CHANNEL_ID = process.env.CHANNEL_ID || '@Mim_PosterBot';

const bot = new TelegramBot(TOKEN);
let messages = [];

// ???? ???? ????? ????
function sendNextMessage() {
  if (messages.length > 0) {
    const message = messages.shift();
    bot.sendMessage(CHANNEL_ID, message);
    console.log(`???? ????? ??: ${message}`);
  }
}

// ????????? ?? 10 ?????
schedule.scheduleJob('*/10 * * * * *', sendNextMessage);

// ???? ???? ??????????
exports.handler = async (event, context) => {
  if (event.httpMethod === 'POST') {
    const body = JSON.parse(event.body);
    if (body.message && body.message.text) {
      const msg = body.message.text.replace('/add ', '');
      if (msg) {
        messages.push(msg);
        await bot.sendMessage(body.message.chat.id, `??? '${msg}' ????? ??!`);
      }
    }
  }
  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'OK' }),
  };
};