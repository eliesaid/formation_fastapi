import asyncio

async def dire_bonjour():
    await asyncio.sleep(1)
    return "Bonjour"

async def main():
    resultats = await asyncio.gather(dire_bonjour(), dire_bonjour())
    print(resultats)  # ["Bonjour", "Bonjour"]

asyncio.run(main())