from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from cgn_ec_api.config import settings
from cgn_ec_api.dependencies.auth import require_local_api_key

app = FastAPI(
    title="cgn-ec",
    description="Flexible solution for your CGNAT logging needs",
    dependencies=[Depends(require_local_api_key)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_headers=["X-Requested-With", "X-Request-ID"],
    expose_headers=["X-Request-ID"],
)


from cgn_ec_api import views  # noqa: E402

app.include_router(views.api_router, prefix="/v1")
