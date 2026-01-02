from duckduckgo_search import DDGS

def test_ddg_chat(query):
    try:
        results = DDGS().chat(query, model="llama-3.1-70b")
        print(f"Chat Response: {results}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ddg_chat("What is the difference between specific risk and systemic risk?")
