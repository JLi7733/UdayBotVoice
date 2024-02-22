# UdayBotVoice

A bot designed by Jonathan Li.
This bot is designed to be use in a communal discord server to respond to messages, play voicelines,
and generate TTS voices. This is inspired by DougDoug's chatBot AIs where I saw him use Elevenlabs.

# Voice Generation
This is the most recent feature and uses the Elevenlabs Python API. The bot takes in an input and
uses the Elevenlabs API to generate a mp3 file using that text. It then utilizes discord to play this
mp3 in the user's voice channel before deleting the file to ensure it doesn't retain all of these files.

# Text messages
This bot will read certain messages and respond if certain keywords or phrases are contained within.
For these messages it purpousley has multiple flaws such as returning the same message multiple times.
This is because the original bot had these flaws and I wanted to retain them.

# Pre-exisitng voice lines
This bot will take pre-existing voicelines and play them in the user's voice channel. These can range from
sound effects to inside jokes. Part of the reason why I wished to implement this is to have a soundboard like
feature before discord implemented the soundboard. Nowadays it also helps bypass the limits a non-boosted server has.

# Future Plans
- Implementing OpenAI's ChatGPT in order to allow for Uday bot to respond dynamically to questions.
- Looking into possibly streaming the audio directly to discord in order to make the TTS quicker for long paragraphs of text
- Linking into other APIs, just for personal interest

