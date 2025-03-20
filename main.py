from fastapi import FastAPI, Depends
from cgn_ec_api.dependencies import require_local_api_key

app = FastAPI(
    title="cgn-ec",
    description="Flexible solution for your CGNAT logging needs",
    dependencies=[Depends(require_local_api_key)],
)

from cgn_ec_api import views  # noqa: E402

app.include_router(views.api_router, prefix="/v1")
