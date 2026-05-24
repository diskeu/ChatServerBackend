from src.chat.chat_websockets import ChatCommunication
from src.chat.http_server import HTTPServer
import asyncio
from os import listdir

async def run():
    # Making Server Object
    http_server = HTTPServer("localhost", 8000)
    chat_server = ChatCommunication()

    # getting chat page
    with open("src/chat/static/chat_page.html", "r") as chat_page:
        chat_start_page = chat_page.read()

    # Defining my Routes
    http_server.add_Route(
        "/",
        lambda : chat_start_page,
        "GET"
    )
    http_server.mount_static("", "src/chat/static/")

    # running services
    await asyncio.gather(
        http_server.boot_Server(),
        chat_server.main()
    )
    
if __name__ == "__main__":
    asyncio.run(run())