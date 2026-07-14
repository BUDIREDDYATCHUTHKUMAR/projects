import logging
from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.core.logging import setup_logging
from app.database.session import get_db
from app.api.v1.auth import router as auth_router
setup_logging()
logger=logging.getLogger("app.main")
app=FastAPI(title=settings.PROJECT_NAME)
app.include_router(auth_router,prefix="/api/v1")
@app.on_event("startup")
def startup_event():
    logger.info(f"starting execution lifecycle for project:{settings.PROJECT_NAME}")
    logger.info(f"target execution environment context:{settings.ENVIRONMENT}")
@app.get("/health",status_code=200)
def health_check(db:Session=Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status="healthy"
    except Exception as e:
        logger.error(f"database health check failed with exception:{str(e)}")
        db_status="unhealthy"
    return {"status":"active",
            "environment":settings.ENVIRONMENT,
            "database":db_status,
            "version":"1.0.0"
    }
