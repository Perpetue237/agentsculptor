from agent.planner import PlannerAgent
from agent.loop import AgentLoop
from tools.prepare_context import prepare_context

def cli_agent(project_path, user_request):
    context = prepare_context(project_path)
    planner = PlannerAgent()
    loop = AgentLoop(planner, context, user_request, project_path)  # ✅ Pass project_path here
    loop.run()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python main.py <project_path> '<user_request>'")
        sys.exit(1)
    project_path = sys.argv[1]
    user_request = sys.argv[2]
    cli_agent(project_path, user_request)
