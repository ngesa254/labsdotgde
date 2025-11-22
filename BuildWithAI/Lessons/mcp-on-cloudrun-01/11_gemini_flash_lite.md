# (Optional) Use Gemini Flash Lite for Faster Responses

Gemini CLI lets you choose the model you are using.

| Model | Description |
|-------|-------------|
| **Gemini 2.5 Pro** | Google's state-of-the-art thinking model, capable of reasoning over complex problems in code, math, and STEM, as well as analyzing large datasets, codebases, and documents using long context. |
| **Gemini 2.5 Flash** | Google's best model in terms of price-performance, offering well-rounded capabilities. Best for large scale processing, low-latency, high volume tasks that require thinking, and agentic use cases. |
| **Gemini 2.5 Flash Lite** | Google's fastest flash model optimized for cost-efficiency and high throughput. |

Since the requests related to finding the zoo animals don't require complex thinking or reasoning, try speeding things up by using a faster model.

## Start Gemini CLI with Flash Lite

Start Gemini CLI with the Flash Lite model:

```bash
gemini --model=gemini-2.5-flash-lite
```

## Test with the Custom Command

Use the custom command you created in the previous step:

```
/find lions
```

You should still see that Gemini CLI calls the `get_animals_by_species` tool and formats the response as instructed by the MCP prompt, but the answer should appear much faster!

```
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✔  get_animals_by_species (zoo-remote MCP Server) {"species":"lion"}                              │
│                                                                                                   │
│    [{"species":"lion","name":"Leo","age":7,"enclosure":"The Big Cat                               │
│    Plains","trail":"Savannah Heights"},...]                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯

✦ Lions can be found in The Big Cat Plains on the Savannah Heights.
```

---

## Troubleshooting

### Unknown Command Error

If you see an error like this:

```
✕ Unknown command: /find --animal="lions"
```

Run `/mcp` to check the server status. If it shows `zoo-remote - Disconnected`, you may need to refresh your credentials.

**To fix this:**

1. Exit Gemini CLI with `/quit`

2. Re-run the IAM binding and refresh your tokens:

   ```bash
   gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
     --member="user:$(gcloud config get-value account)" \
     --role="roles/run.invoker"

   export PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")
   export ID_TOKEN=$(gcloud auth print-identity-token)
   ```

3. Regenerate the settings file:

   ```bash
   cat > ~/.gemini/settings.json << EOF
   {
     "ide": {
       "hasSeenNudge": true
     },
     "mcpServers": {
       "zoo-remote": {
         "httpUrl": "https://zoo-mcp-server-${PROJECT_NUMBER}.europe-west1.run.app/mcp",
         "headers": {
           "Authorization": "Bearer ${ID_TOKEN}"
         }
       }
     },
     "security": {
       "auth": {
         "selectedType": "cloud-shell"
       }
     }
   }
   EOF
   ```

4. Restart Gemini CLI:

   ```bash
   gemini --model=gemini-2.5-flash-lite
   ```