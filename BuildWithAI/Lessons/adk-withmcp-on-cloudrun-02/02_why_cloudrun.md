# Why Deploy to Cloud Run?

Cloud Run is a great choice for hosting ADK agents because it's a **serverless platform**, which means you can focus on your code and not on managing the underlying infrastructure. Google handles the operational work for you.

Think of it like a **pop-up shop**: it only opens and uses resources when customers (requests) arrive. When there are no customers, it closes down completely, and you don't pay for an empty store.

---

## Key Features

### Runs Containers Anywhere

- You bring a container (Docker image) that has your app inside
- Cloud Run runs it on Google's infrastructure
- No OS patching, VM setup, or scaling headaches

### Automatic Scaling

- If **0 people** are using your app → **0 instances** run (scales down to zero, which is cost effective)
- If **1000 requests** hit it → it spins up as many copies as needed

### Stateless by Default

- Each request could go to a different instance
- If you need to store state, use an external service like Cloud SQL, Firestore, or Memorystore

### Supports Any Language or Framework

- As long as it runs in a Linux container, Cloud Run doesn't care if it's Python, Go, Node.js, Java, or .NET

### Pay for What You Use

| Billing Model | Description |
|---------------|-------------|
| **Request-based** | Billed per request + compute time (down to 100 ms) |
| **Instance-based** | Billed for full instance lifetime (no per-request fee) |

---

## Why Cloud Run for ADK Agents?

| Benefit | For ADK Agents |
|---------|----------------|
| **Zero to Hero Scaling** | Handle traffic spikes when many users query your agent |
| **Cost Efficiency** | Pay nothing when the agent isn't being used |
| **Simple Deployment** | Deploy with a single `gcloud run deploy` command |
| **Secure by Default** | Built-in IAM authentication for service-to-service calls |
| **Managed TLS** | HTTPS endpoints with automatic certificate management |