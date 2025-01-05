# Sherlock Domains Python SDK


<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

### Installation

Install latest from the GitHub
[repository](https://github.com/Fewsats/sherlock-python):

``` sh
$ pip install git+https://github.com/Fewsats/sherlock-python.git
```

``` sh
$ pip install sherlock-domains
```

## How to use

Create a Sherlock instance with a private key for the agent to use. If
no key is provided, a new one will be generated and saved to the default
config file.

``` python
s = Sherlock()
s
```

    Sherlock(pubkey=90ba884688884277e49080712f386eebc88806efa8345ca937f75fe80950156d)

You can search for a domain and request to purchase it. Purchasing a
domain requires contact information as mandated by ICANN.

``` python
sr = s.search("trakwiska.com")
sr
```

    {'id': '0125c86b-f067-41a9-936d-1dcc9542b190',
     'created_at': '2025-01-05T04:18:27.042Z',
     'available': [{'name': 'trakwiska.com',
       'tld': 'com',
       'tags': [],
       'price': 1105,
       'currency': 'USD',
       'available': True}],
     'unavailable': []}

Contact information is needed for registering a new domain with the
ICANN.

``` python
c = Contact(**{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "address": "123 Test St",
    "city": "Test City",
    "state": "CA",
    "country": "US",
    "postal_code": "12345",
})

s = Sherlock(c=c)
```

Finalizing a pruchase involves a payment. Sherlock Domains currently
supports two payment methods: Credit Card (`credit_card`) and the
Lightning Netowrk (`lightning`). By default the credit card method is
used. The method will then return a checkout URL that can be used to
complete the payment. In the case of lightning the response will contain
a lightning invoice.

``` python
s.purchase_domain(sr['id'], "trakwiska.com")
```

    {'payment_method': {'checkout_url': 'https://checkout.stripe.com/c/pay/cs_live_a1Dy5JtF7phqQg28y8Y6AerkkQuYuhTC7Y5WuxuDoeIZf4l5KrZxsfnOnO#fidkdWxOYHwnPyd1blppbHNgWjA0S3VzXDdBbTFNVlJzfDVRQVQ2dVdBTnJTSH1QMGs2dHRsanJMbkY0PTxKbUtRaWowT2NwMGM8RlVBbGRqSWo3UFYwcVdqR3F9N2BtM2ZTPXc1Z3dQXGc2NTVPYVVSQkM8bycpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl',
      'lightning_invoice': None},
     'expires_at': '2025-01-05T04:48:28.120Z'}

You can now use the checkout URL to complete the purchase and the domain
will be registered to your agent.

You can view the domains you own with:

``` python
s.domains()
```

    [{'id': 'd9b2cc30-c15d-44b9-9d39-5d33da504484',
      'domain_name': 'h402.org',
      'created_at': '2024-12-28T18:58:49.899Z',
      'expires_at': '2024-12-31T18:58:42Z',
      'auto_renew': False,
      'locked': True,
      'private': True,
      'nameservers': [],
      'status': 'active'}]

Below is a list of all the tools that the client offers to manage the
domains and purchases.

``` python
s.as_tools().map(lambda t: t.__name__)
```

    (#10) ['_me','_set_contact','_get_contact','_search','purchase_domain','_domains','_dns_records','_create_dns_record','_update_dns_record','_delete_dns_record']

## AI agents

We will show how to enable your AI assistant to handle payments using
[Claudette](https://claudette.answer.ai), Answer.ai convenient wrapper
for Claude. You’ll need to export your `ANTHROPIC_API_KEY`.

``` python
from claudette import Chat, models
```

``` python
model = models[1]; model
```

    'claude-3-5-sonnet-20240620'

Create a Sherlock instance with a public & private key for the agent to
use.

Sherlock supports returning all the tools with `s.as_tools()`.

In order to request a purchase, we need to provide a contact
information. You can either do so during the class initialization or
manually. Then we just pass the extra tool.

``` python
sp = 'You are a helpful assistant that has access to a domain purchase API.'
chat = Chat(model, sp=sp, tools=s.as_tools())

pr = f"Search if domain 'the-favourite-game.com' is available? If it is request a purchase and process the payment using credit card method."
r = chat.toolloop(pr, trace_func=print)
r
```

    Message(id='msg_01Tvso582YUVNv9ihCKaYRn4', content=[TextBlock(text="Certainly! I'll search for the domain 'the-favourite-game.com' and if it's available, I'll proceed with the purchase request using the credit card payment method. Let's start with the search.", type='text'), ToolUseBlock(id='toolu_01Bqi6ks9GRqVEuBCpgcfSGS', input={'q': 'the-favourite-game.com'}, name='_search', type='tool_use')], model='claude-3-5-sonnet-20240620', role='assistant', stop_reason='tool_use', stop_sequence=None, type='message', usage=In: 2961; Out: 104; Cache create: 0; Cache read: 0; Total: 3065)
    Message(id='msg_018d9XfZYzTgNXxJxYkWhmuZ', content=[TextBlock(text="Great news! The domain 'the-favourite-game.com' is available for purchase. The search results show that it's priced at $11.05 USD.\n\nNow, before we proceed with the purchase, we need to make sure that the contact information is set up correctly. Let's check the current contact information:", type='text'), ToolUseBlock(id='toolu_01S2CjBV3my9YR9AaoMkC87A', input={}, name='_get_contact', type='tool_use')], model='claude-3-5-sonnet-20240620', role='assistant', stop_reason='tool_use', stop_sequence=None, type='message', usage=In: 3192; Out: 107; Cache create: 0; Cache read: 0; Total: 3299)
    Message(id='msg_01P1ofAoXRH3d63PZ88Khebb', content=[TextBlock(text="It looks like there's already contact information set up. If you want to use different contact information for this purchase, please let me know, and we can update it. Otherwise, we'll proceed with the purchase using the existing contact information.\n\nNow, let's request the purchase of the domain using the credit card payment method:", type='text'), ToolUseBlock(id='toolu_01GsycUDxqPSjykG1Nzah924', input={'sid': 'e5bf5d1b-9c68-4837-8a8f-0265c67bb957', 'domain': 'the-favourite-game.com', 'payment_method': 'credit_card'}, name='purchase_domain', type='tool_use')], model='claude-3-5-sonnet-20240620', role='assistant', stop_reason='tool_use', stop_sequence=None, type='message', usage=In: 3364; Out: 190; Cache create: 0; Cache read: 0; Total: 3554)
    Message(id='msg_01TcZh8WaxN4RXwVoC9vnp9t', content=[TextBlock(text="Excellent! The purchase request for 'the-favourite-game.com' has been processed successfully. Here's what you need to know:\n\n1. Payment Method: Credit Card (as requested)\n2. Checkout URL: https://checkout.stripe.com/c/pay/cs_live_a1KyXxSVx9E67tS1qa4swSyBtIBIXVTPXTCQZYMnAPdBzFgIIiuhwgXqqS#fidkdWxOYHwnPyd1blppbHNgWjA0S3VzXDdBbTFNVlJzfDVRQVQ2dVdBTnJTSH1QMGs2dHRsanJMbkY0PTxKbUtRaWowT2NwMGM8RlVBbGRqSWo3UFYwcVdqR3F9N2BtM2ZTPXc1Z3dQXGc2NTVPYVVSQkM8bycpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl\n3. Expiration: The payment link expires at 2025-01-05T04:49:29.781Z\n\nTo complete the purchase, please follow these steps:\n\n1. Click on the checkout URL provided above.\n2. You will be redirected to a secure Stripe payment page.\n3. Enter your credit card details and complete the payment process.\n4. Once the payment is successful, the domain 'the-favourite-game.com' will be registered to your account.\n\nMake sure to complete the payment before the expiration time to secure your domain. If you have any issues with the payment process or need any further assistance, please don't hesitate to ask. Good luck with your new domain!", type='text')], model='claude-3-5-sonnet-20240620', role='assistant', stop_reason='end_turn', stop_sequence=None, type='message', usage=In: 3909; Out: 508; Cache create: 0; Cache read: 0; Total: 4417)

Excellent! The purchase request for ‘the-favourite-game.com’ has been
processed successfully. Here’s what you need to know:

1.  Payment Method: Credit Card (as requested)
2.  Checkout URL:
    https://checkout.stripe.com/c/pay/cs_live_a1KyXxSVx9E67tS1qa4swSyBtIBIXVTPXTCQZYMnAPdBzFgIIiuhwgXqqS#fidkdWxOYHwnPyd1blppbHNgWjA0S3VzXDdBbTFNVlJzfDVRQVQ2dVdBTnJTSH1QMGs2dHRsanJMbkY0PTxKbUtRaWowT2NwMGM8RlVBbGRqSWo3UFYwcVdqR3F9N2BtM2ZTPXc1Z3dQXGc2NTVPYVVSQkM8bycpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl
3.  Expiration: The payment link expires at 2025-01-05T04:49:29.781Z

To complete the purchase, please follow these steps:

1.  Click on the checkout URL provided above.
2.  You will be redirected to a secure Stripe payment page.
3.  Enter your credit card details and complete the payment process.
4.  Once the payment is successful, the domain ‘the-favourite-game.com’
    will be registered to your account.

Make sure to complete the payment before the expiration time to secure
your domain. If you have any issues with the payment process or need any
further assistance, please don’t hesitate to ask. Good luck with your
new domain!

<details>

- id: `msg_01TcZh8WaxN4RXwVoC9vnp9t`
- content:
  `[{'text': "Excellent! The purchase request for 'the-favourite-game.com' has been processed successfully. Here's what you need to know:\n\n1. Payment Method: Credit Card (as requested)\n2. Checkout URL: https://checkout.stripe.com/c/pay/cs_live_a1KyXxSVx9E67tS1qa4swSyBtIBIXVTPXTCQZYMnAPdBzFgIIiuhwgXqqS#fidkdWxOYHwnPyd1blppbHNgWjA0S3VzXDdBbTFNVlJzfDVRQVQ2dVdBTnJTSH1QMGs2dHRsanJMbkY0PTxKbUtRaWowT2NwMGM8RlVBbGRqSWo3UFYwcVdqR3F9N2BtM2ZTPXc1Z3dQXGc2NTVPYVVSQkM8bycpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl\n3. Expiration: The payment link expires at 2025-01-05T04:49:29.781Z\n\nTo complete the purchase, please follow these steps:\n\n1. Click on the checkout URL provided above.\n2. You will be redirected to a secure Stripe payment page.\n3. Enter your credit card details and complete the payment process.\n4. Once the payment is successful, the domain 'the-favourite-game.com' will be registered to your account.\n\nMake sure to complete the payment before the expiration time to secure your domain. If you have any issues with the payment process or need any further assistance, please don't hesitate to ask. Good luck with your new domain!", 'type': 'text'}]`
- model: `claude-3-5-sonnet-20240620`
- role: `assistant`
- stop_reason: `end_turn`
- stop_sequence: `None`
- type: `message`
- usage:
  `{'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0, 'input_tokens': 3909, 'output_tokens': 508}`

</details>
