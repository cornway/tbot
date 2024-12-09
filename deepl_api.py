import deepl

auth_key: str = ''

def deepl_set_auth(auth: str):
    global auth_key
    auth_key = auth

def remap_language(language: str):
    lang_map = {
        'Polish': 'PL',
        'English': 'EN-US'
    }

    assert language in lang_map
    return lang_map[language]

def deepl_translate(text, language):
    language = remap_language(language)
    translator = deepl.Translator(auth_key)

    print(f'translator = {language}')
    result = translator.translate_text(text, target_lang=language)
    return result.text