import asyncio
import time

async def dire_bonjour():
    await asyncio.sleep(2)
    return "Bonjour"

async def main():
    start = time.time()  # début du chronomètre
    resultats = await asyncio.gather(dire_bonjour(), dire_bonjour())
    end = time.time()    # fin du chronomètre
    print(resultats)     # ["Bonjour", "Bonjour"]
    print(f"Temps d'exécution : {end - start:.2f} secondes")

asyncio.run(main())
