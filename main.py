import sending_to_chatgpt
import asyncio
import reading_from_presentation
import writing_to_json
import argparse


def process_presentation(presentation_path):
    name_of_presentation = presentation_path.split('\\')[::-1][0].split('.')[0]
    slides = reading_from_presentation.read_from_presentation(presentation_path)
    list_of_responses = sending_to_chatgpt.send_presentation_to_gpt(slides, name_of_presentation)
    writing_to_json.writing_to_json_file(name_of_presentation, list_of_responses)


