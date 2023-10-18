import json
from os import path
from gtts import gTTS
from gtts import gTTS
from playsound import playsound
import flet
from flet import Container, Page, Row, Text, Column, TextSpan, TextStyle
from flet_core.control_event import ControlEvent
from pynput.keyboard import Key, Listener

class App:
    def __init__(self, page: Page):
        self.source_language = "Italian"
        self.target_language = "English"
        self.page = page
        self.page.padding = 20
        self.title = "Word Glider | Better Than Flash Card"
        self.words = []
        self.content_file = "./from.txt"
        json_bundled_words = "./dictionaries/italian_to_english_cybersecurity.json"
        self.text_spans_list = self.json_bundled_words_to_text_span(json_bundled_words)
        self.translation = Text("", selectable=False)
        self.current_index = 0
        self.build_gui(page)
        self.page.on_keyboard_event = self.on_keyboard_event
        self.text_views: Column = None
        self.on_word_selected(0, 0)
        self.is_window_active = True

    def build_gui(self, page: Page):
        page.title = self.title
        text_views: Column = Column(
            [
                Text(spans=self.text_spans_list),
                Container(height=100),  # Add space to the bottom
            ],
            scroll="always",
            height=page.window_height,
        )
        self.text_views = text_views
        page.add(
            Column(
                [
                    self.translation,
                    Container(height=20),  # Spacer
                    self.text_views,
                ],
            )
        )

        self.page.on_window_event = self.on_window_event
    
    def on_window_event(self, event: ControlEvent):
        if event.data == "focus":
            self.is_window_active = True
        elif event.data == "blur":
            self.is_window_active = False
        

    def json_bundled_words_to_text_span(self, file_path: str) -> list:
        text_spans = []
        space = [TextSpan(" ")]
        with open(file_path, "r") as f:
            self.words = json.load(f)
            for word in self.words:
                span = TextSpan(word["word"], spans=space)
                span.style = TextStyle(bgcolor=flet.colors.TRANSPARENT, size=18)
                span.on_click = self.on_span_clicked
                span.data = len(text_spans)  # Store the word's index within its line
                text_spans.append(span)  # the length should be added before appending
        text_spans[0].style.bgcolor = flet.colors.BLUE_ACCENT
        return text_spans

    def on_word_selected(self, prev_index: int, current_index: int):
        last_span: TextSpan = self.text_spans_list[prev_index]
        current_span: TextSpan = self.text_spans_list[current_index]
        last_span.style.bgcolor = flet.colors.TRANSPARENT
        current_span.style.bgcolor = flet.colors.BLUE_ACCENT
        word = self.words[current_index]
        self.update_translation(word)

    
    def play_spoken_word(self, word):
        audio_file_path = path.join("./audio", f"{word}.mp3")
        try: 
            if not path.exists(audio_file_path):
                tts = gTTS(text=word, lang='it')
                tts.save(audio_file_path)
            playsound(audio_file_path)
        except Exception as e:
            # make a dialog to show the error
            print(e)
            print("Error playing the word")

    def get_text_spans_to_translate(self) -> list:
        text_spans = []
        with open(self.content_file, "r") as f:
            for line in f:
                for word in line.strip().split():
                    word = word.strip()
                    if not word:
                        continue
                    separator = "  "
                    span = TextSpan(f"{word}{separator}")
                    span.style = TextStyle(bgcolor=flet.colors.TRANSPARENT, size=18)
                    span.on_click = self.on_span_clicked
                    span.data = len(
                        text_spans
                    )  # Store the word's index within its line
                    text_spans.append(
                        span
                    )  # the length should be added before appending
        text_spans[0].style.bgcolor = flet.colors.BLUE_ACCENT
        return text_spans

    def update_translation(self, word: json):
        exmaples_spans = TextSpan("\n\n", style=TextStyle(size=14))

        for exmaple, mean in zip(word["examples"], word["translation_of_examples"]):
            exmaples_spans.spans.append(TextSpan(f"{exmaple} \n\t {mean}\n\n"))

        translation_span = TextSpan(word["translation"], style=TextStyle(color=flet.colors.GREEN ,size=18))
        word_span = TextSpan(word["word"], style=TextStyle(size=18))
        self.translation.spans = [word_span, TextSpan(" : "), translation_span, exmaples_spans]
        self.page.update()

    def on_keyboard_event(self, e: flet.KeyboardEvent):
        if e.key == "Arrow Left":
            self.move_selection_left_or_right("left")
        if e.key == "Arrow Right":
            self.move_selection_left_or_right("right")
        if e.key == "Arrow Up":
            word = self.words[self.current_index]
            self.play_spoken_word(word["word"])

    def on_span_clicked(self, e: ControlEvent):
        prev_index = self.current_index
        new_index = e.control.data
        self.on_word_selected(prev_index, new_index)
        self.current_index = new_index

    def move_selection_left_or_right(self, key):
        prev_index = self.current_index
        if key == "left":
            if self.current_index == 0:
                print("This is the first word")
                return
            self.current_index -= 1
        elif key == "right":
            if self.current_index == len(self.text_spans_list) - 1:
                print("This is the last word")
                return
            self.current_index += 1
        self.on_word_selected(prev_index, self.current_index)

if __name__ == "__main__":
    flet.app(target=App)