documentation :

https://python.langchain.com/docs/integration/tools/




%pip install --upgrade --quiet langchain langchain-community langchain-openai langchain-databricks wikipedia duckduckgo-search youtube_search  




dbutils.library.restartPython()



from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun, YouTubeSearchTool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool


wikidata = WikipediaQueryRun(api_wrapper = WikipediaAPIWrapper())


wikidata.run("what is databricks")



# Note: Previous Wikipedia API wrapper may need user-agent configuration
# Recreating with proper headers
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun

wiki_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=500)
wikidata_fixed = WikipediaQueryRun(api_wrapper=wiki_wrapper)

wikidata_fixed.run("what is generative ai")



# Wikipedia API requires User-Agent header
# Using wikipedia library directly with proper configuration
import wikipedia

# Set user agent to avoid 403 errors
wikipedia.set_user_agent("LangChainBot/1.0 (https://example.com; bot@example.com)")

try:
    result = wikipedia.summary("ayush susheel", sentences=2)
    print(result)
except wikipedia.exceptions.PageError:
    print("No Wikipedia page found for 'ayush susheel'")
except wikipedia.exceptions.DisambiguationError as e:
    print(f"Multiple pages found: {e.options[:5]}")




pip install -U ddgs



from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
search.invoke("What is the capital of France")




search.invoke("Who is narendra modi")



search.invoke("ayush susheel pursuing masters , working as project trainee intern at Stmicroelectronics ")



search.run("ayush susheel pursuing masters , working as project trainee intern at Stmicroelectronics ")


from langchain_community.tools import YouTubeSearchTool

youtube_tool = YouTubeSearchTool()

youtube_tool.run("Ayush Susheel")



CREATING AGENT
from langchain_community.chat_models import ChatDatabricks
from langchain.agents import Tool, initialize_agent, AgentType

from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import YouTubeSearchTool




from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# List all serving endpoints
endpoints = w.serving_endpoints.list()

print("Available Serving Endpoints:")
print("-" * 50)
for endpoint in endpoints:
    print(f"Name: {endpoint.name}")
    if endpoint.config and endpoint.config.served_entities:
        for entity in endpoint.config.served_entities:
            if hasattr(entity, 'external_model') and entity.external_model:
                print(f"  Provider: {entity.external_model.provider}")
                print(f"  Model: {entity.external_model.name}")
            elif hasattr(entity, 'foundation_model'):
                print(f"  Foundation Model: {entity.foundation_model.name}")
    print()






 Meta Llama 3.3 70B Instruct

chat_model = ChatDatabricks(endpoint="databricks-meta-llama-3-3-70b-instruct")

# defining tools

# 1st) Wikipedia tool with proper User-Agent configuration
import wikipedia
wikipedia.set_user_agent("LangChainBot/1.0 (https://example.com; bot@example.com)")

def wikipedia_search(query):
    try:
        return wikipedia.summary(query, sentences=3)
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia page found for '{query}'"
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple pages found. Try being more specific. Options: {e.options[:5]}"
    except Exception as e:
        return f"Wikipedia search error: {str(e)}"

wiki_tool = Tool(
    name="Wikipedia",
    func=wikipedia_search,
    description="search wikipedia for movie information"
)

# 2nd)
youtube_tool = Tool(
    name="Youtube",
    func=YouTubeSearchTool().run,
    description="search youtube for movie information"
)

# # 3rd)
# search_tool = Tool(
#     name="DuckDuckGo",
#     func=DuckDuckGoSearchRun().run,
#     description="search duckduckgo for movie information"
# )

# tools = [wiki_tool, youtube_tool, search_tool]
tools = [wiki_tool, youtube_tool]

agent = initialize_agent(
    tools=tools,
    llm=chat_model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # does a reasoning before acting
    verbose=True
)

print("HI, I am Agent, I can answer your questions about movies")
theme = input("Enter your question: ")

try:
    movie = f"Give me a brief answer to the following question: {theme} from Wikipedia and find 2 youtube videos related to the {theme}"
    if movie:
        response = agent.run(movie)
        print(response)
except Exception as e:
    print(f"Error: {e}")

















