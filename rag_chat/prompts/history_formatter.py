def format_history(history):

    formatted_history = ""

    for message in history:

        role = message.get("role", "user")
        content = message.get("content", "")

        formatted_history += f"{role.capitalize()}: {content}\n"

    return formatted_history