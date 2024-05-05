import deepl 
import os

##########################
# 英語から日本語に翻訳する
##########################
async def translation(text):
    def en_to_ja():
        # deeplのAPI_KEY
        API_KEY = os.environ.get('API_KEY')
        translator = deepl.Translator(API_KEY)

        result = translator.translate_text(text, target_lang='JA')
        return result.text
    result = en_to_ja()
    return result

