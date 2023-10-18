import openai


class Translator:
    en = "English"
    it = "Italian"

    def __init__(self, api_key):
        self.api_key = api_key
        # openai.api_key = api_key
        openai_api_key = "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"


    def translate(self, text_to_translate, source_language, target_language) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": f"""You will be provided with a sentence in {source_language}, and your task is to translate it into {target_language} and you will also provide 3 exmaples sentence of the word/s used in the {source_language}""",
                },
                {"role": "user", "content": text_to_translate},
            ],
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # Extract the translated text from the response
        translated_text = response["choices"][0]["message"]["content"]
        return translated_text
