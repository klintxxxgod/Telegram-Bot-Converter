import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

BOT_TOKEN = ""
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

VIDEO_FOLDER = "downloads\\videos"
AUDIO_FOLDER = "downloads\\audios"

os.makedirs(VIDEO_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "Hola by KLINTXXXGOD"
    )

@dp.message(lambda message: message.video)
async def handle_video(message: types.Message):
    video = message.video
    file_id = video.file_id
    file = await bot.get_file(file_id)
    video_path = os.path.join(VIDEO_FOLDER, f"{file_id}.mp4")
    video_pathnew = os.path.join(VIDEO_FOLDER, f"{file_id}new.mp4")
    await bot.download_file(file.file_path, video_path)
    try:
        input_video = VideoFileClip(video_path)
        w, h = input_video.size
        circle_size = 360
        aspect_ratio = float(w) / float(h)
        if w > h:
            new_w = int(circle_size * aspect_ratio)
            new_h = circle_size
        else:
            new_w = circle_size
            new_h = int(circle_size / aspect_ratio)
        resized_video = input_video.resize((new_w, new_h))
        output_video = resized_video.crop(x_center=resized_video.w/2, y_center=resized_video.h/2, width=circle_size, height=circle_size)
        output_video.write_videofile(video_pathnew, codec="libx264", audio_codec="aac", bitrate="5M")
        await message.answer_video_note(
            video_note=FSInputFile(video_pathnew)
        )
    except Exception as e:
        print(f"Error {e}")

@dp.message(lambda message: message.audio)
async def handle_audio(message: types.Message):
    audio = message.audio
    file_id = audio.file_id
    file = await bot.get_file(file_id)
    audio_path = os.path.join(AUDIO_FOLDER, f"{file_id}.mp3")
    await bot.download_file(file.file_path, audio_path)
    if not os.path.exists(audio_path):
        return
    await message.answer_voice(voice=FSInputFile("audio_path"))
    
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
