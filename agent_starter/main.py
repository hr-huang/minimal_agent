from agent import ToolCallingAgent
from config import load_settings


def main() -> None:
    settings = load_settings()
    agent = ToolCallingAgent(settings)

    print(f"Agent started | model={settings.model}")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Bye.")
            break

        try:
            answer = agent.run(user_input)
            print(f"Agent > {answer}\n")
        except Exception as exc:
            print(f"Error > {type(exc).__name__}: {exc}\n")


if __name__ == "__main__":
    main()
