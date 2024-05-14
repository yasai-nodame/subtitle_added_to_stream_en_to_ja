import os 
import asyncio

import video_path

# ディレクトリ内の mkv ファイル,srtファイルを順番に再生
async def file_remove(file_number):
    loop = asyncio.get_event_loop()
    if os.path.exists(os.path.join(video_path.os.environ.get('AUDIO_FILE_PATH'), f'output_audio{file_number}.wav')):
        await loop.run_in_executor(None, os.remove, os.path.join(video_path.os.environ.get('AUDIO_FILE_PATH'), f'output_audio{file_number}.wav'))
        
    if os.path.exists(os.path.join(video_path.os.environ.get('MKV_DIRECTORY'), f'output{file_number}.mkv')):
        await loop.run_in_executor(None, os.remove, os.path.join(video_path.os.environ.get('MKV_DIRECTORY'), f'output{file_number}.mkv'))

async def ts_remove(file_number):
    loop = asyncio.get_event_loop()
    if os.path.exists(os.path.join(video_path.os.environ.get('VIDEO_FILE_PATH'), f'file{file_number}.ts')):
        await loop.run_in_executor(None, os.remove, os.path.join(video_path.os.environ.get('VIDEO_FILE_PATH'), f'file{file_number}.ts'))
