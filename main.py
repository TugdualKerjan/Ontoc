from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import database

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Disable template caching to fix the unhashable type error
templates.env.cache = {}

@app.on_event("startup")
async def startup_event():
    database.init_database()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, filter: str = None, value: str = None):
    systems = database.get_all_systems()

    # Apply filtering if parameters are provided
    if filter and value:
        filtered_systems = []
        for system in systems:
            if filter == "determinism" and system.get("determinism") == value:
                filtered_systems.append(system)
            elif filter == "exactness" and system.get("exactness") == value:
                filtered_systems.append(system)
            elif filter == "reversibility" and system.get("reversibility") == value:
                filtered_systems.append(system)
            elif filter == "realization_type" and system.get("realization_type") == value:
                filtered_systems.append(system)
            elif filter == "computation_model" and system.get("computation_model") and value in system["computation_model"]:
                filtered_systems.append(system)
        systems = filtered_systems

    substrates = database.get_all_substrates()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "systems": systems,
            "substrates": substrates,
            "filter": filter,
            "filter_value": value
        }
    )

@app.get("/ontoc/systems/{system_id}", response_class=HTMLResponse)
async def system_page(request: Request, system_id: str):
    system = database.get_system(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found")

    return templates.TemplateResponse(
        request=request,
        name="system.html",
        context={"system": system}
    )

@app.get("/ontoc/substrates/{substrate_id}", response_class=HTMLResponse)
async def substrate_page(request: Request, substrate_id: str):
    substrate = database.get_substrate(substrate_id)
    if not substrate:
        raise HTTPException(status_code=404, detail="Substrate not found")

    systems = database.get_systems_by_substrate(substrate_id)
    return templates.TemplateResponse(
        request=request,
        name="substrate.html",
        context={
            "substrate": substrate,
            "systems": systems
        }
    )

@app.get("/api/systems")
async def api_systems():
    return database.get_all_systems()

@app.get("/api/substrates")
async def api_substrates():
    return database.get_all_substrates()

@app.get("/api/systems/{system_id}")
async def api_system(system_id: str):
    system = database.get_system(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    return system

# Category pages for all property types
@app.get("/ontoc/determinism/{value}", response_class=HTMLResponse)
async def determinism_page(request: Request, value: str):
    systems = database.get_systems_by_property("determinism", value)
    return templates.TemplateResponse(
        request=request,
        name="category.html",
        context={
            "property_name": "determinism",
            "property_value": value,
            "category_display_name": f"Determinism: {value.title()}",
            "systems": systems
        }
    )

@app.get("/ontoc/exactness/{value}", response_class=HTMLResponse)
async def exactness_page(request: Request, value: str):
    systems = database.get_systems_by_property("exactness", value)
    return templates.TemplateResponse(
        request=request,
        name="category.html",
        context={
            "property_name": "exactness",
            "property_value": value,
            "category_display_name": f"Exactness: {value.title()}",
            "systems": systems
        }
    )

@app.get("/ontoc/reversibility/{value}", response_class=HTMLResponse)
async def reversibility_page(request: Request, value: str):
    systems = database.get_systems_by_property("reversibility", value)
    return templates.TemplateResponse(
        request=request,
        name="category.html",
        context={
            "property_name": "reversibility",
            "property_value": value,
            "category_display_name": f"Reversibility: {value.title()}",
            "systems": systems
        }
    )

@app.get("/ontoc/realization_type/{value}", response_class=HTMLResponse)
async def realization_type_page(request: Request, value: str):
    systems = database.get_systems_by_property("realization_type", value)
    return templates.TemplateResponse(
        request=request,
        name="category.html",
        context={
            "property_name": "realization_type",
            "property_value": value,
            "category_display_name": f"Realization Type: {value.replace('_', ' ').title()}",
            "systems": systems
        }
    )

@app.get("/ontoc/computation_model/{value}", response_class=HTMLResponse)
async def computation_model_page(request: Request, value: str):
    systems = database.get_systems_by_property("computation_model", value)
    return templates.TemplateResponse(
        request=request,
        name="category.html",
        context={
            "property_name": "computation_model",
            "property_value": value,
            "category_display_name": f"Computation Model: {value.replace('_', ' ').replace('-', ' ').title()}",
            "systems": systems
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)