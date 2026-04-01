# (Optional) Use Gemini Flash Lite

Many requests in this lab are structured and tool-heavy rather than deeply reasoning-heavy. That makes them a good fit for a faster model.

## Switch to Flash Lite

In Gemini CLI, you can switch to a faster model using the `/model` command:

```text
/model gemini-2.0-flash-lite
```

## Try a Faster Flow

Try prompts like:

```text
List the products in the catalog.
```

or:

```text
Validate an MPESA Express payload for one conference pass.
```

You should still see Gemini calling your MCP tools, but the response should appear faster.

## When This Helps

Flash Lite is a good fit for:

- listing products
- checking prices
- validating payload fields
- explaining known error codes

Use a more capable model when you need more planning or richer synthesis.
