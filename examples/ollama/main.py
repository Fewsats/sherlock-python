import os
import openai
from cosette import Chat, Client as CosetteClient, contents
from sherlock.core import Sherlock
from dotenv import load_dotenv
import os

load_dotenv()

MODEL = os.getenv('MODEL', 'llama3.2')
INFERENCE_HOST = os.getenv('INFERENCE_HOST', 'http://localhost:11434/v1')
API_KEY = os.getenv('API_KEY', 'PLACEHOLDER_API_KEY')
SHERLOCK_AGENT_PRIVATE_KEY_HEX = os.getenv('SHERLOCK_AGENT_PRIVATE_KEY_HEX')
DEBUG = os.getenv('DEBUG', False)


def main():
    # Cossete expects a client that implements the OpenAI API
    cli = openai.OpenAI(base_url=INFERENCE_HOST, api_key='not-required')

    # Private key for authenticating with sherlock
    # If you don't provide one, authenticated calls will not be available
    sherlock = Sherlock(SHERLOCK_AGENT_PRIVATE_KEY_HEX)

    cossete_client = CosetteClient(MODEL, cli)
    sp = '''
    You are a helpful assistant that has access to a domain registrar and DNS management API.

    Some things to keep in mind:
    - Always provide accurate information.
    - Always provide the id for domains and id for records when available.
    - When talking to the user, keep it concise and to the point.
    - Always double check before making any destructive actions.
    - If you are not sure about the answer, ask the user for clarification.
    - Prices are always in the minimum unit of the currency. For example for USD they are in cents. An offer of {price:1199 currency: USD} is $11.99.
    - For domains that you are own you are usually interested in domain_id, name, expiration date, and auto-renewal status.
    - All the DNS endpoints use the domain id to identify the domain.
    '''
    chat = Chat(cli=cossete_client, sp=sp, tools=sherlock.as_tools())

    trace_func = print if DEBUG else None

    print("Welcome to the Sherlock Agent chat! Type 'exit' to quit.")
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == 'exit':
                break
            if user_input:
                response = chat.toolloop(user_input, trace_func=trace_func)
                print("\nAssistant:", contents(response))
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == '__main__':
    main()
