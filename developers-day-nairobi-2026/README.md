# Google for Developers Day: Nairobi

> Hands-on engineering with Google's cloud and agentic stack.

| Event detail | Information |
|---|---|
| Date | November 13, 2026 |
| Time | 8:00 AM–5:00 PM EAT (GMT+3) |
| Venue | Sarit Expo Center, Sarit Center, Westlands, Nairobi, 00100, Kenya |
| Audience | Software engineers, cloud architects, and applied AI developers |
| Featured lab in this folder | Deploy a RAG AI Barista with Google ADK, Streamlit, and Cloud Run |

## About the event

Google for Developers Day: Nairobi brings developers together for hands-on workshops, live deployments, and deep dives into Google's cloud and agentic stack. The event announcement describes more than four workshop tracks and opportunities to connect with Googlers, founders, Google Developer Experts, and developers from across East Africa.

The event themes include:

- **Autonomous AI and RAG:** Build automations, connect customer intelligence with Firebase, and deploy retrieval-augmented agents on serverless infrastructure.
- **Production cloud scale:** Explore container orchestration and dynamic autoscaling on Google Kubernetes Engine (GKE).
- **Hands-on engineering:** Work through code, deployment terminals, and practical application architecture.
- **Nairobi developer community:** Learn and build alongside the local ecosystem.

Event logistics and themes above come from the supplied event announcement. This folder documents the Barista workshop; the wider event's Firebase and GKE sessions are separate tracks.

## Start the workshop

**[Lab 1: Deploy a RAG AI Barista with Google ADK, Streamlit, and Cloud Run](01-ai-barista-cloud-run/README.md)**

Build a coffee shop assistant that recommends real menu items, answers price questions, and uses menu tags and listed allergens when responding to preferences. Deploy the Streamlit application to Cloud Run, then optionally replace local JSON retrieval with Firestore vector search.

| Path | What it contains |
|---|---|
| [Lab overview](01-ai-barista-cloud-run/README.md) | Learning objectives, prerequisites, and lesson navigation |
| [HTML architecture guide](01-ai-barista-cloud-run/BARISTA_CLOUD_RUN_ARCHITECTURE.html) | Browser document with four diagrams, source map, validation checks, and print support |
| [Architecture and flows](01-ai-barista-cloud-run/architecture.md) | Cloud Run architecture, chat sequence, Firestore retrieval, and deployment diagrams |
| [Core lab](01-ai-barista-cloud-run/01_overview.md) | Numbered instructions for building, deploying, and testing the Barista |
| [Optional extension](01-ai-barista-cloud-run/08_firestore_vector_search.md) | Semantic menu retrieval and a live menu update without redeployment |
| [Cleanup](01-ai-barista-cloud-run/09_cleanup.md) | Remove the resources created for the selected workshop track |
| [Troubleshooting](01-ai-barista-cloud-run/10_troubleshooting.md) | Errors, diagnostic commands, and completion checklist |

## Folder structure

```text
developers-day-nairobi-2026/
├── README.md
└── 01-ai-barista-cloud-run/
    ├── README.md
    ├── BARISTA_CLOUD_RUN_ARCHITECTURE.html
    ├── architecture.md
    ├── 01_overview.md
    ├── 02_project_setup.md
    ├── 03_choose_track.md
    ├── 04_create_menu.md
    ├── 05_build_agent_and_ui.md
    ├── 06_deploy_cloud_run.md
    ├── 07_test_barista.md
    ├── 08_firestore_vector_search.md
    ├── 09_cleanup.md
    └── 10_troubleshooting.md
```

## Workshop material

The numbered lessons are adapted from the supplied `barista-cloud-run-lab.md`, preserving its code, dependency pins, project configuration, and rehearsal notes. Rehearsal observations refer to the supplied guide; this documentation import does not establish a fresh deployment or runtime test.

[Original Google Cloud codelab](https://codelabs.developers.google.com/codelabs/cloud-run/build-streamlit-rag-agent-google-adk-cloud-run) · [All LabsDotGDE workshops](../README.md)
