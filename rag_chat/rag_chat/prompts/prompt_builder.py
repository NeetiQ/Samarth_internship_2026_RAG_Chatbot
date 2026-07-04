from rag_chat.prompts.system_prompt import SYSTEM_PROMPT
from rag_chat.prompts.history_formatter import format_history

def build_prompt(question, context, history=None):

    prompt = SYSTEM_PROMPT

    if history:
        formatted_history = format_history(history)

        prompt += "\n\nChat History:\n"
        prompt += formatted_history

    prompt += "\n\nContext:\n"
    prompt += context

    prompt += "\n\nQuestion:\n"
    prompt += question

    return prompt