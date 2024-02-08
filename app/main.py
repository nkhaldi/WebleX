"""Основной файл приложения FastAPI."""

import csv
from io import StringIO

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from routes.database import RoutePoint, close_db, init_db
from routes.utils import delete_route_from_db, get_route_from_db, optimize_route, save_route_to_db

# Start the FastAPI app
app = FastAPI()

# Use Jinja2 for HTML templates
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_event():
    """Connect to the database when the app starts."""
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    """Disconnect from the database when the app stops."""
    await close_db()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/routes/{route_id}")
async def get_route(route_id: int):
    """Get a route by ID."""
    if route := await get_route_from_db(route_id):
        return {"id": route.id, "points": [{"lat": point.lat, "lng": point.lng} for point in route.points]}

    raise HTTPException(status_code=404, detail="Route not found")


@app.post("/api/routes/")
async def upload_routes(file: UploadFile = File(...)):
    """Upload a CSV file with route points and return the optimized route."""
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a csv file.")

    content = await file.read()
    reader = csv.DictReader(StringIO(content.decode("utf-8")))
    points = [RoutePoint(lat=float(row["lat"]), lng=float(row["lng"])) for row in reader]

    # Здесь логика оптимизации маршрута
    optimized_route = optimize_route(points)

    # Логика сохранения оптимизированного маршрута в базу данных
    route_id = await save_route_to_db(optimized_route)

    points = [{"lat": point.lat, "lng": point.lng} for point in optimized_route]

    return JSONResponse(status_code=200, content={"id": route_id, "points": points})


@app.delete("/api/routes/{route_id}")
async def delete_route(route_id: int):
    """Delete a route by ID."""
    is_deleted = await delete_route_from_db(route_id)
    if is_deleted:
        return {"message": "Route deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Route not found")
