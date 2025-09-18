import time
from fastapi import Request

async def logging_middleware(request: Request, call_next):
    """
    Middleware global :
    - logge méthode + chemin + statut
    - mesure le temps d'exécution et l'insère dans X-Process-Time-ms
    """
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time-ms"] = f"{duration_ms:.2f}"
    print(f"[{request.method}] {request.url.path} -> {response.status_code} in {duration_ms:.2f} ms")
    return response
