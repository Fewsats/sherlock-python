import openai
from cosette import Chat, Client as CosetteClient
from sherlock.core import Sherlock

MODEL = 'gpt-4o-mini'
API_KEY = ''
SHERLOCK_AGENT_PRIVATE_KEY_HEX = ''
DEBUG=True

def main():
    # Cossete expects a client that implements the OpenAI API
    cli = openai.OpenAI(api_key=API_KEY)

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
    - All the DNS endpoints use the domain_id to identify the domain.
    '''
    chat = Chat(cli=cossete_client, sp=sp, tools=sherlock.as_tools())

    trace_func = print if DEBUG else None

    print("Welcome to the Sherlock Agent chat! Type 'exit' to quit.")
    print("For multiline input, start with \"\"\" and end with \"\"\" on a new line.")
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == 'exit':
                break
            if user_input.startswith('"""'):
                lines = [user_input[3:]]
                while True:
                    line = input()
                    if line.rstrip().endswith('"""'):
                        lines.append(line[:-3])
                        break
                    lines.append(line)
                user_input = '\n'.join(lines)
            if user_input:
                response = chat.toolloop(user_input, trace_func=trace_func)
                print("\nAssistant:", response.choices[0].message.content)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == '__main__':
    main()
