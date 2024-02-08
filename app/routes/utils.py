"""Functions for working with routes."""

import math

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from routes.database import AsyncSessionLocal, Route, RoutePoint


async def get_route_from_db(route_id: int) -> Route:
    """Get a route from the database by its ID."""
    async with AsyncSessionLocal() as session:
        statement = select(Route).where(Route.id == route_id).options(selectinload(Route.points))
        result = await session.execute(statement)
        route = result.scalar_one_or_none()
        return route


async def save_route_to_db(points: list[RoutePoint]) -> int:
    """Save a route to the database and return its ID."""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Create a new route and get its ID
            new_route = Route()
            session.add(new_route)
            await session.flush()

            # Add the route points to the database
            route_points = [RoutePoint(route_id=new_route.id, lat=point.lat, lng=point.lng) for point in points]
            session.add_all(route_points)

        return new_route.id


async def delete_route_from_db(route_id: int) -> bool:
    """Delete a route from the database by its ID."""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Find all points for the route
            points_statement = select(RoutePoint).where(RoutePoint.route_id == route_id)
            points_result = await session.execute(points_statement)
            points_to_delete = points_result.scalars().all()

            # Delete all points for the route
            for point in points_to_delete:
                await session.delete(point)

            #  Delete the route
            route_statement = select(Route).where(Route.id == route_id)
            route_result = await session.execute(route_statement)
            route_to_delete = route_result.scalar_one_or_none()

            if route_to_delete:
                await session.delete(route_to_delete)
                return True
            else:
                return False


def calculate_distance(point1: RoutePoint, point2: RoutePoint) -> float:
    """Calculate the distance between two points."""
    return math.sqrt((point1.lat - point2.lat) ** 2 + (point1.lng - point2.lng) ** 2)


def optimize_route(points: list[RoutePoint]) -> list[RoutePoint]:
    """Optimize a route using the nearest neighbor algorithm."""
    if not points:
        return []

    # Start with the first point and remove it from the list
    optimized_route = [points.pop(0)]
    while points:
        # Add the nearest point to the optimized route and remove it from the list
        last_point = optimized_route[-1]
        next_point = min(points, key=lambda point: calculate_distance(last_point, point))
        optimized_route.append(next_point)
        points.remove(next_point)

    return optimized_route
