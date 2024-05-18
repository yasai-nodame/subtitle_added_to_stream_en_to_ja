# Twitch Live Stream Subtitle Embedder

## 概要

Twitchのライブ配信のm3u8形式のURLを取得し、m3u8_download.pyのURLに記述します。このスクリプトは、取得したライブ配信をリアルタイムでダウンロードし、字幕(日本語→英語)を埋め込んで視聴することができます。

## 実行手順

1. コマンドプロンプトを開きます。
2. 空のディレクトリを4つ(tsファイル用, wavファイル用, srtファイル用, mkvファイル用)準備して、os.environに合わせて、コードを書き直します。
3. `start python m3u8_download.py & start python vlc_regeneration.py` を実行します。
4. m3u8_download.pyがライブ配信をダウンロードし続け、vlc_regeneration.pyが字幕を埋め込んだ動画をVLCでリアルタイムに再生します。
5. vlc_regeneration.pyの待ち時間が短ければ短いほど、止まりやすくなるため、できるだけ、待ち時間が長いようにtime.sleep()しましょう。

## 注意事項

- 日本語から英語に翻訳するため、deeplのAPIが必要です。
- 大容量の動画ファイルをダウンロードする場合は、十分なディスク容量を確保してください。
- このスクリプトはTwitchのライブ配信に対応しています。他の動画ストリーミングプラットフォームには対応していません。
- ディレクトリのPATHはご自身のPATHに置き換えてください。
- URLはTwichのネットワークタブからm3u8を取得してください。
