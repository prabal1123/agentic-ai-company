from appAgents.orchestrator import Orchestrator

# Fresh workspace so we don't inherit leftover files from earlier
# manual testing (ai_workspace already has crop-tracker files in it).
orchestrator = Orchestrator(workspace="ai_workspace_orchestrator")

idea = """
A mobile application that helps small farmers
track crop health using photos.
"""

report = orchestrator.run(idea)

print("\n\n========== FINAL REPORT ==========")
print("Tests passed:", report["tests_passed"])
print("Files:", report["files"])
if not report["tests_passed"]:
    print("Last error stage:", report["final_result"].get("stage"))
