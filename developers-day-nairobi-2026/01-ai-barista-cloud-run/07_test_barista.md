## 7. Verify the base RAG behavior

| Prompt | Pass condition |
|---|---|
| Recommend something strong and warm. | Espresso Solo, a single shot. The menu is authoritative for the shot count. |
| Do you have a matcha frappuccino? | Explains the drink is unavailable on this menu. Any alternatives are real menu items. |
| I'm lactose intolerant. What can I get? | Selects items explicitly listed as dairy-free. Uses menu wording and avoids claims such as “completely safe.” |
| What's hot, sweet, and dairy-free? | Oat Milk Honey Latte. |
| How much is that? | In the same chat after the latte recommendation, gives $5.00. |
| Hi | A greeting or one clarifying question is acceptable. |

Rehearsal evidence showed the original Cloud Run service responding, selecting Espresso Solo, declining the matcha frappuccino, and carrying the dairy-free preference forward. Its item selection passed the dietary check, and its wording overstated safety. The instructions above address that behavior. Follow-up pricing and the revised wording require a fresh chat check on the updated build.

---

[Lab overview](README.md) · [Previous](06_deploy_cloud_run.md) · [Next](08_firestore_vector_search.md)
