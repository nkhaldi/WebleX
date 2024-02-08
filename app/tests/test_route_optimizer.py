"""Tests for the route optimizer function."""

import unittest

from routes.database import RoutePoint
from routes.utils import optimize_route


class TestRouteOptimizer(unittest.TestCase):
    """Tests for the route optimizer function."""

    def test_optimize_route_simple_case(self):
        """Test the route optimizer with a simple case."""
        points = [
            RoutePoint(lat=0, lng=0),
            RoutePoint(lat=1, lng=1),
            RoutePoint(lat=2, lng=2),
            RoutePoint(lat=3, lng=3),
        ]

        optimized_route = optimize_route(points)

        self.assertEqual(optimized_route[0].lat, 0)
        self.assertEqual(optimized_route[0].lng, 0)

        self.assertEqual(optimized_route[-1].lat, 3)
        self.assertEqual(optimized_route[-1].lng, 3)

        # Проверяем, что все точки присутствуют в маршруте
        self.assertEqual(len(optimized_route), 4)


if __name__ == "__main__":
    unittest.main()
