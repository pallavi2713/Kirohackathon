"""
Prompt templates for the Government Scheme Chatbot.
Centralized location for all LLM prompts.
"""


def get_query_rewrite_prompt(history, question):
    """
    Get prompt for rewriting follow-up questions into standalone questions.
    
    Args:
        history: Conversation history text
        question: User's follow-up question
        
    Returns:
        str: Formatted prompt for query rewriting
    """
    return f"""
Convert the follow-up question into a standalone question.

Conversation History:
{history}

Follow-up Question:
{question}

Standalone Question:
"""


def get_answer_generation_prompt(lang_instruction, history, context, question):
    """
    Get prompt for generating answers using RAG approach.
    
    Args:
        lang_instruction: Language instruction (English/Hindi)
        history: Conversation history text
        context: Retrieved context from OpenSearch
        question: User's current question
        
    Returns:
        str: Formatted prompt for answer generation
    """
    return f"""
You are an AI assistant that helps citizens understand Indian Government Schemes.

Language Instruction:
{lang_instruction}

Instructions:
- Use the Context to answer the question.
- Use the Conversation History to understand follow-up questions.
- If the user asks something like "eligibility", "benefits", "how much money", assume they are referring to the scheme mentioned earlier in the conversation.
- Combine Conversation History context + Context to give the best answer.
- If the answer is not found in the Context, say: "I could not find this information in the available government scheme data."

Formatting Rules:
- Use simple language.
- Answer in clear bullet points using "-" only.
- Do NOT use markdown formatting like ** or *.
- Do NOT repeat information.
- Keep answers short and easy to understand.

Conversation History context--  use it to answer follow up questions:
{history}

Context:
{context}

Current User Question:
{question}

Provide the final answer for the user.
"""
