import asyncio
import functools

class MainLoop():
    loop=asyncio.get_event_loop()
    def __init__(self):
        self.loop.run_forever()

    def __str__(self):
        return "Main loop obj"

    def stop_loop(self):
        self.loop.stop()
        exit(0)


# async def doSmthg():
#     print("csumi")

# def main():
#     loop=asyncio.get_event_loop()
#     try:
#         loop.run_until_complete(doSmthg())
#     finally:
#         loop.close()

if __name__=='__main__':
    z=MainLoop()