import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("accelerator-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Data Platform Accelerator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/platforms")
def get_platforms():
    return [
        {"id": "plat-fin-gold", "name": "Finance Lakehouse", "target": "Azure Databricks", "status": "ACTIVE", "compliance": 0.98},
        {"id": "plat-mark-raw", "name": "Marketing Warehouse", "target": "Snowflake", "status": "ACTIVE", "compliance": 0.94},
        {"id": "plat-hr-global", "name": "HR Global Fabric", "target": "Microsoft Fabric", "status": "PROVISIONING", "compliance": 0.0}
    ]

@app.get("/governance/summary")
def get_governance_summary():
    return {
        "total_datasets": 1420,
        "certified_datasets": 850,
        "pii_coverage": "100%",
        "catalog_freshness": "5m ago"
    }

@app.get("/costs/summary")
def get_costs_summary():
    return {
        "monthly_burn": "$42.5K",
        "savings_identified": "$8.2K",
        "top_consumer": "Finance Lakehouse",
        "budget_status": "ON_TRACK"
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_environments": 12,
        "active_pipelines": 450,
        "reliability_index": "99.4%",
        "onboarding_velocity": "4.2 days"
    }

@app.post("/platforms/create")
def create_platform(blueprint_id: str, domain: str):
    logger.info(f"Triggering platform provisioning for blueprint: {blueprint_id} in domain: {domain}")
    return {"status": "Provisioning Job Enqueued", "job_id": "job_plat_123"}
