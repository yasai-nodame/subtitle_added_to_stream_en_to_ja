import time 
import vlc
import os 
import re
from itertools import zip_longest
import asyncio

import video_path

#############################################################################
# mkvファイルが存在するまで回す
# srtファイルも存在してる場合、mkvファイルの連番と等しい時に動画に埋め込む
# mkvファイルが存在して、srtファイルが存在しない場合、mkvファイルだけ回し続ける
# srtファイルが存在しない時は、音声を認識してないか、喋ってないかのどちらか
#############################################################################
async def play_mkv_files(mkv_directory, srt_directory):
    # VLC インスタンス化
    instance = vlc.Instance('--sub-source marq')
    player = instance.media_player_new()
    
    playing_mkv_files = set()
    playing_srt_files = set()
    while True:
        # ディレクトリ内の mkv ファイル,srtファイルを順番に再生
        mkv_files = set(f for f in os.listdir(mkv_directory) if f.endswith('.mkv'))
        srt_files = set(f for f in os.listdir(srt_directory) if f.endswith('.srt'))
        
        # 新しいmkvファイル,srtファイルが追加された場合に、再生リストに追加
        new_mkv_files = mkv_files - playing_mkv_files
        new_srt_files = srt_files - playing_srt_files
        
        # set()によって要素がバラバラになってるのでsorted()で整形する。 それだけだと1,10,2の順番になるので key=lambdaを使って最初の数字の部分を抽出しint()にいれ、group()で部分文字列を取得。
        sort_mkv_files = sorted(new_mkv_files, key=lambda x: int(re.search(r'\d+', x).group()))
        sort_srt_files = sorted(new_srt_files, key=lambda x: int(re.search(r'\d+', x).group()))
        

        
        for mkv_file,srt_file in zip_longest(sort_mkv_files, sort_srt_files):
            if srt_file is None:
                mkv_file_number = int(re.search(r'\d+', mkv_file).group())
                
                mkv_file_path = os.path.join(mkv_directory, mkv_file)
                
                if len(os.listdir(mkv_directory)[:-10]) < mkv_file_number:
                    print('ファイルに追いつくので、60秒遅延を発生させます。')
                    time.sleep(60)
                
                    media = instance.media_new(mkv_file_path)
                    player.set_media(media)
                    player.play()
                    playing_mkv_files.add(mkv_file)
            
                while player.get_state() != vlc.State.Playing:
                    time.sleep(0.1)
                
                duration = player.get_length() / 1000
                time.sleep(duration)
            else:
                mkv_file_number = int(re.search(r'\d+', mkv_file).group())
                srt_file_number = int(re.search(r'\d+', srt_file).group())
            
                if mkv_file_number == srt_file_number:
                    mkv_file_path = os.path.join(mkv_directory, mkv_file)
                    srt_file_path = os.path.join(srt_directory, srt_file)
                    
                    mkv_file_number = int(re.search(r'\d+', mkv_file).group())
                    
                    if len(os.listdir(mkv_directory)[:-10]) < mkv_file_number:
                        print('ファイルに追いつくので、60秒遅延を発生させます。')
                        time.sleep(60)
                    
                    # mkv ファイルを再生
                    media = instance.media_new(mkv_file_path)
                    media.add_option(f':sub-file={srt_file_path}')
                    
                    player.set_media(media)
                    player.play()
                    playing_mkv_files.add(mkv_file)
                    playing_srt_files.add(srt_file)
                    
                    # ファイルが再生されるまで待機
                    while player.get_state() != vlc.State.Playing:
                        time.sleep(0.1)
                    
                    # 再生が終了するまで待機
                    duration = player.get_length() / 1000
                    time.sleep(duration)
                    
                elif mkv_file_number != srt_file_number:
                        mkv_file_path = os.path.join(mkv_directory, mkv_file)
                        
                        mkv_file_number = int(re.search(r'\d+', mkv_file).group())
                        
                        if len(os.listdir(mkv_directory)[:-10]) < mkv_file_number:
                            print('ファイルに追いつくので、60秒遅延を発生させます。')
                            time.sleep(60)
                        media = instance.media_new(mkv_file_path)
                        player.set_media(media)
                        player.play()
                        playing_mkv_files.add(mkv_file)
                        
                        while player.get_state() != vlc.State.Playing:
                            time.sleep(0.1)
                        
                        duration = player.get_length() / 1000
                        time.sleep(duration)
            
            # 再生が終了したファイルを再生リストから削除
            for mkv_file, srt_file in zip(playing_mkv_files.copy(), playing_srt_files.copy()):
                if not os.path.exists(os.path.join(mkv_directory, mkv_file)):
                    playing_mkv_files.remove(mkv_file)
                if not os.path.exists(os.path.join(srt_directory, srt_file)):
                    playing_srt_files.remove(srt_file)
            
                    
            break
        

async def main():
    mkv_file = video_path.os.environ.get('MKV_DIRECTORY')
    srt_file = video_path.os.environ.get('SRT_DIRECTORY')
    print('約60秒後に、ライブを再生します。')
    while True:
        if len(os.listdir(mkv_file)) > 60:
            await play_mkv_files(mkv_file, srt_file)
        else:
            continue
        

if __name__ == '__main__':
    asyncio.run(main())
