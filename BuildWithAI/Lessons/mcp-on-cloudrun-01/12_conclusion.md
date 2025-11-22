# Conclusion

🎉 **Congratulations!** You have successfully deployed and connected to a secure remote MCP server.

## What You Accomplished

In this lab, you:

- Created a Python MCP server using FastMCP with two tools (`get_animals_by_species` and `get_animal_details`)
- Deployed the MCP server to Cloud Run as a secure, authenticated service
- Connected to the remote MCP server from Gemini CLI
- Verified tool calls in the server logs
- (Optional) Added custom MCP prompts for faster workflows
- (Optional) Used Gemini Flash Lite for faster responses

---

## Continue to the Next Lab

This lab is the first in a three-part series. In the second lab, you will use the MCP server you created with an ADK Agent.

**Next:** [Use an MCP Server on Cloud Run with an ADK Agent](#)

---

## (Optional) Clean Up

If you are not continuing on to the next lab and would like to clean up what you have created, you can delete your Cloud project to avoid incurring additional charges.

> **Note:** While Cloud Run does not charge when the service is not in use, you might still be charged for storing the container image in Artifact Registry. Deleting your Cloud project stops billing for all the resources used within that project.

### Delete the Project

If you would like to delete the project:

```bash
gcloud projects delete $GOOGLE_CLOUD_PROJECT
```

### Delete Local Resources

You may also want to delete unnecessary resources from your Cloud Shell disk.

**Delete the codelab project directory:**

```bash
rm -rf ~/mcp-on-cloudrun
```

**Delete the Gemini CLI settings:**

```bash
rm -rf ~/.gemini
```

> ⚠️ **Warning!** The next action cannot be undone! If you would like to delete everything on your Cloud Shell to free up space, you can delete your whole home directory. **Be careful that everything you want to keep is saved somewhere else.**

```bash
sudo rm -rf $HOME
```