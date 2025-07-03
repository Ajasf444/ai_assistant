import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MAX_CONVERSATION_ITERATIONS
from functions.call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    user_prompt = " ".join(args)
    if not user_prompt:
        print("Error: No prompt supplied.")
        exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    iterations = 0
    while True:
        iterations += 1
        if iterations > MAX_CONVERSATION_ITERATIONS:
            print(f"Maximum iterations ({
                  MAX_CONVERSATION_ITERATIONS}) reached.")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")
    if not response.function_calls:
        return response.text
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("Empty function call result.")
        if verbose:
            print(
                f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("No function responses generated, exiting.")

    messages.append(types.Content(role="tool", parts=function_responses))


if __name__ == "__main__":
    main()
