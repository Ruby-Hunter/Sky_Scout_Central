from fastapi import APIRouter

router = APIRouter()


@router.get("")
def health_check():
    return {"status": "ok", "message": "Sky Scout Central API is up and soaring!"}


@router.get("/pingspeed")
def ping_speed(start_time: float):
    import time

    end_time = time.time()
    latency = end_time - start_time
    return {"status": "ok", "ping_ms": latency * 1000}
