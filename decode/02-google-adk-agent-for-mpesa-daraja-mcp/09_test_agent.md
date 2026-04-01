# Test the Deployed Agent

With your agent live on Cloud Run, open the public service URL in your browser.

## Start a Conversation

Type:

```text
hello
```

The agent should explain that it can help with:

- product lookup
- order totals
- MPESA Express request preparation
- callback interpretation
- payment error explanations

## Test Prompts

Try prompts like:

```text
List the products in the catalog.
```

```text
What is the total for two Build With AI Conference Passes?
```

```text
Prepare an MPESA Express request for two conference passes paid by 254722111111.
```

```text
Explain error code 1032.
```

```text
Parse this callback payload and tell me whether payment succeeded.
```

The expected behavior is that the agent uses the MCP tools rather than inventing prices or payment metadata.
