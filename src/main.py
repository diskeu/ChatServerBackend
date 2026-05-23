from src.chat.chat_websockets import ChatCommunication
from src.chat.http_server import HTTPServer
import asyncio

async def run():
    # Making Server Object
    http_server = HTTPServer("localhost", 8000)
    chat_server = ChatCommunication()

    # getting chat page
    with open("chat_page.html", "r") as chat_page:
        chat_start_page = chat_page.read()

    # Defining my Routes
    server.add_Route(
        "/",
        chat_page,
        "GET"
    )
    server.mount_static("", "static/")

    # running services
    await asyncio.gather(
        server.boot_Server(),
        chat_server.main()
    )
    
if __name__ == "__main__":
    asyncio.run(run())