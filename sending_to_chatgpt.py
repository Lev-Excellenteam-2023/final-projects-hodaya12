import os
import time
import openai
import asyncio
import slide
os.environ["OPENAI_API_KEY"] = ''
openai.api_key = os.getenv("OPENAI_API_KEY")


def formulate_query(name_of_presentation: str):
    """
    Formulates a prompt to send to ChatGPT for slide explanations.

    :param name_of_presentation: The name of the presentation.
    :returns: The formulated query as a string.
    """
    return f"I have a presentation that I'm having trouble understanding. I will send you the slides one by one, and I would appreciate your explanations. Each slide will be provided in the following format:\n\nTitle: title\nContent: content\n\nThe presentation is about {name_of_presentation}. Thank you in advance for your assistance."


async def send_slide_to_gpt(slide:slide,messages:list):
    """
        Sends a slide to ChatGPT for explanation.

        :param slide: The slide to be sent for explanation.
        :param messages: The list of previous messages in the conversation.
        :returns: The response from ChatGPT as a string, or None if an error occurs.
        :rtype: str or None
        :raises: RateLimitError: If the rate limit for the API is reached.
             InvalidRequestError: If the maximum context length for the model is exceeded.
        """
    content_message = 'The title: ' + slide.title + '\n' + 'The content: ' + slide.paragraphs
    messages.append({"role": "user", "content": content_message})
    try:
        chat_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            timeout=30
        )
        chat_response = chat_response.choices[0].message.content
        messages.append({"role": "assistant", "content": chat_response})
    except openai.error.RateLimitError:
        print("Rate limit reached. Waiting before retrying...")
        time.sleep(20)  # Wait for 20 seconds before retrying
        return await send_slide_to_gpt(slide,messages) # Retry the API call
    except openai.error.InvalidRequestError:
        print(f"Model's maximum context length exceeded for slide {slide.number_of_slide}. Reducing message length...")
        messages.pop()  # Remove the last user message
        return await send_slide_to_gpt(slide,messages) # Retry the API call without the last message
    except Exception as e:
        print(f"Error occurred for slide {slide.number_of_slide}: {str(e)}")
        return None
    return chat_response



async def send_presentation_to_gpt(slides:list, name_of_presentation:str):
    """
    Sends each slide of a presentation to ChatGPT for explanation.

    :param slides: A list of slides to be sent for explanation.
    :param name_of_presentation: The name of the presentation.
    :returns: A list of responses from ChatGPT for each slide.
    """
    messages = [{"role": "system", "content": formulate_query(name_of_presentation)}]
    return await asyncio.gather(*(send_slide_to_gpt(slide, messages) for slide in slides), return_exceptions=True)











