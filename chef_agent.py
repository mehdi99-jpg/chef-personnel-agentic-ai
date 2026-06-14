import os
from typing import Annotated, List, TypedDict
from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode

# 1. Configuration & Setup
load_dotenv()

MODEL_NAME = "llama3.2:3b"
tavily_key = os.getenv("TAVILY_API_KEY")

# 2. RAG Tool
@tool
def local_recipe_search(query: str) -> str:
    """Searches local 'recipes/' folder for keywords."""
    recipe_dir = "recipes"
    if not os.path.exists(recipe_dir): return "No local recipe folder found."
    
    keywords = [k.strip().lower() for k in query.split() if len(k) > 2]
    if not keywords: keywords = [query.lower()]

    results = []
    for filename in os.listdir(recipe_dir):
        if filename.endswith(".md") or filename.endswith(".txt"):
            try:
                with open(os.path.join(recipe_dir, filename), "r", encoding="utf-8") as f:
                    content = f.read().lower()
                    if any(k in content or k in filename.lower() for k in keywords):
                        results.append(f"--- {filename} ---\n{content}")
            except Exception: continue
    
    return "\n\n".join(results) if results else "No matching local recipes."

# 3. Define the Agent State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "The list of messages"]

# 4. Initialize Tools & LLM
tools = [local_recipe_search]
if tavily_key:
    tools.append(TavilySearchResults(max_results=2))

llm = ChatOllama(model=MODEL_NAME, temperature=0).bind_tools(tools)

# 5. Simplified & Stricter Persona
CHEF_SYSTEM_PROMPT = """
You are a Personal Chef. 

MANDATORY SAFETY RULES:
1. If the user mentions an allergy (e.g., LEMON), you MUST NEVER suggest any recipe containing that ingredient.
2. If a recipe in the 'local_recipe_search' has an allergen, DO NOT suggest it. Suggest a different one or a version without the allergen.
3. Be concise. Do not hallucinate other users' conversations.
4. State if the recipe is from 'Local Book' or 'Web'.
"""

# 6. Graph Logic
def call_model(state: AgentState):
    messages = [SystemMessage(content=CHEF_SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# 7. Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))
workflow.set_entry_point("agent")
workflow.add_edge("tools", "agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})

# 8. Compile
memory = InMemorySaver()
app = workflow.compile(checkpointer=memory)

# 9. Interactive Loop
def chat():
    print(f"\n--- Personal Chef Agent (Model: {MODEL_NAME}) ---")
    config = {"configurable": {"thread_id": "unique_session_123"}}

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["quit", "exit"]: break

            input_message = HumanMessage(content=user_input)
            
            # Use 'invoke' instead of 'stream' for cleaner output with smaller models
            output = app.invoke({"messages": [input_message]}, config)
            final_msg = output["messages"][-1].content
            
            if final_msg:
                print(f"\nChef: {final_msg}")
            else:
                print("\nChef: I'm sorry, I couldn't find a safe recipe for you.")

        except Exception as e:
            print(f"\n[Error]: {e}")

if __name__ == "__main__":
    chat()
