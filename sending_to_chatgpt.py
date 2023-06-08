import os
import time
import openai
import asyncio
import slide
os.environ["OPENAI_API_KEY"] = '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'
openai.api_key = os.getenv("OPENAI_API_KEY")


def formulate_query(name_of_presentation: str):
    """
    Formulates a prompt to send to ChatGPT for slide explanations.

    :param name_of_presentation: The name of the presentation.
    :returns: The formulated query as a string.
    """
    return f"I have a presentation that I'm having trouble understanding. I will send you the slides one by one, and I would appreciate your explanations. Each slide will be provided in the following format:\n\nTitle: title\nContent: content\n\nThe presentation is about {name_of_presentation}. Thank you in advance for your assistance."














