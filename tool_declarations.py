from utils import web_search_tool
from google.genai import types

web_search_tool_declaration = types.FunctionDeclaration(
    name="web_search_tool",
    description=(
        """This tool retrieves fresh, reliable, and up-to-date information from the web.
    Use it whenever a question requires current facts, dates, news, events,
    weather, market data, real-time updates, or any information that may have
    changed recently or is not known beforehand.
    Avoid its use when enough information is already known about the topic."""
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "query": types.Schema(
                type=types.Type.STRING,
                description="The query string to be used for the web search.",
            ),
        },
        required=["query"],
    ),
)

email_read_tool_declaration = types.FunctionDeclaration(
    name="email_read_tool",
    description=("""This tool reads unread emails from the connected Gmail inbox,
        marks them as read, and returns their sender, subject, and message body.
        Use it whenever you need to fetch the latest unread messages."""
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={},
        required=[],
    ),
)

email_send_tool_declaration = types.FunctionDeclaration(
    name="email_send_tool",
    description=(
        """Sends an email using the Gmail client.
        If no subject is provided, you have to generate subject based on data available."""
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "to": types.Schema(
                type=types.Type.STRING,
                description="Recipient email address.",
            ),
            "subject": types.Schema(
                type=types.Type.STRING,
                description="Email subject. If missing, a default subject will be created.",
            ),
            "body": types.Schema(
                type=types.Type.STRING,
                description="Plain text content of the email.",
            ),
        },
        required=["to", "subject", "body"],
    ),
)

get_news_tool_declaration = types.FunctionDeclaration(
    name="get_news_tool",
    description=(
        """Fetches the latest news articles for a given query. It searches Google News RSS,
        decodes article URLs, downloads the articles, and returns up to 5 results containing
        title, link, and extracted text. Use this tool when user needs anything related to news or some kind of event."""
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "query": types.Schema(
                type=types.Type.STRING,
                description="The news topic or search query."
            ),
        },
        required=["query"],
    ),
)