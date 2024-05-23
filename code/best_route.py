import math
import itertools
from typing import List, Tuple


# Utility class to calculate distances
class DistanceCalculator:
    @staticmethod
    def haversine_distance(loc1, loc2) -> float:
        """
        Calculate the haversine distance between two geo-locations.
        Refernces: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude

        Args:
            loc1 (GeoLocation): The first location.
            loc2 (GeoLocation): The second location.

        Returns:
            float: The distance between loc1 and loc2 in kilometers.
        """

        R = 6371  # Radius of Earth in km
        lat1, lon1 = math.radians(loc1.latitude), math.radians(loc1.longitude)
        lat2, lon2 = math.radians(loc2.latitude), math.radians(loc2.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c  # Distance in km
        return distance

    @staticmethod
    def travel_time(distance, speed_kmh=20) -> float:
        """
        Calculate travel time based on distance and speed.

        Args:
            distance (float): The distance in kilometers.
            speed_kmh (float): Speed in kilometers per hour.

        Returns:
            float: Travel time in hours.
        """
        return distance / speed_kmh  # Time in hours


# GeoLocation class
class GeoLocation:
    def __init__(self, name: str, latitude: float, longitude: float):
        """
        Initialize a geo-location.

        Args:
            name (str): Name of the location.
            latitude (float): Latitude of the location.
            longitude (float): Longitude of the location.
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return self.name


# Order class
class Order:
    def __init__(
        self, restaurant: GeoLocation, consumer: GeoLocation, preparation_time: float
    ):
        """
        Initialize an order.

        Args:
            restaurant (GeoLocation): The restaurant location.
            consumer (GeoLocation): The consumer location.
            preparation_time (float): Preparation time in hours.
        """
        self.restaurant = restaurant
        self.consumer = consumer
        self.preparation_time = preparation_time


# DeliveryOptimizer class
class DeliveryOptimizer:
    def __init__(self, start_location: GeoLocation, orders: List[Order]):
        """
        Initialize the delivery optimizer.

        Args:
            start_location (GeoLocation): The starting location (delivery executive's location).
            orders (List[Order]): List of orders to be delivered.
        """
        self.start_location = start_location
        self.orders = orders

    def _generate_permutations(self, elements: List) -> List[List]:
        """
        Generate all permutations of a list of elements with the constraint that each consumer
        location comes after its corresponding restaurant location.

        Args:
            elements (List[Order]): List of orders to permute.

        Returns:
            List[List[GeoLocation]]: List of all permutations satisfying the constraint.
        """
        mapper = {}
        rs = []
        cs = []
        for order in elements:
            rs.append(order.restaurant)
            cs.append(order.consumer)
            mapper[order.consumer] = order.restaurant

        combinations = []

        def backtrack(current_list, visited_rs, used_cs):
            """
            Backtracks to find all possible combinations.

            Args:
                current_list: The current combination being built.
                visited_rs: A set of already visited elements from rs.
                used_cs: A set of already used elements from cs.
            """
            if len(current_list) == len(rs) + len(cs):
                combinations.append(current_list.copy())
                return

            for element in rs:
                if element not in visited_rs:
                    visited_rs.add(element)
                    current_list.append(element)
                    backtrack(current_list, visited_rs.copy(), used_cs.copy())
                    current_list.pop()
                    visited_rs.remove(element)

            for element in cs:
                if (
                    element in mapper
                    and mapper[element] in visited_rs
                    and element not in used_cs
                ):
                    current_list.append(element)
                    used_cs.add(element)
                    backtrack(current_list, visited_rs.copy(), used_cs.copy())
                    current_list.pop()
                    used_cs.remove(element)

        backtrack([], set(), set())
        return combinations

    def calculate_total_time(
        self, sequence: List[GeoLocation], preparation_times: List[float]
    ) -> float:
        """
        Calculate the total time to complete a delivery route.

        Args:
            sequence (List[GeoLocation]): List of locations in the route.
            preparation_times (List[float]): List of preparation times for each order.

        Returns:
            float: Total time in hours to complete the route.
        """
        total_time = 0
        current_location = sequence[0]

        for i in range(1, len(sequence)):
            next_location = sequence[i]
            distance = DistanceCalculator.haversine_distance(
                current_location, next_location
            )
            travel_time = DistanceCalculator.travel_time(distance)

            # Add preparation time for the current location before moving to the next location
            if i - 1 < len(preparation_times):
                total_time += preparation_times[i - 1]

            total_time += travel_time
            current_location = next_location

        return total_time

    def find_best_route(self) -> Tuple[str, float]:
        """
        Find the best route to deliver all orders in the shortest time.

        Returns:
            Tuple[str, float]: Best route as a string and the total time to complete the route.
        """
        all_locations = []
        preparation_times = []

        # Add restaurants & consumer to the location list and collect preparation times
        for order in self.orders:
            all_locations.append(order.restaurant)
            all_locations.append(order.consumer)
            preparation_times.append(order.preparation_time)

        # Generate all possible routes
        routes = self._generate_permutations(self.orders)

        best_route = []
        best_time = float("inf")

        # Evaluate each route to find the one with the shortest time
        for route in routes:
            total_time = self.calculate_total_time(
                [self.start_location] + route, preparation_times
            )
            if total_time < best_time:
                best_time = total_time
                best_route = route

        # Format the best route as a string
        best_route_str = " -> ".join(
            [self.start_location.name] + [loc.name for loc in best_route]
        )
        return best_route_str, best_time


if __name__ == "__main__":
    delivery_executive = GeoLocation("delivery_executive", 12.935192, 77.624480)
    r1 = GeoLocation("r1", 12.934533, 77.626579)
    r2 = GeoLocation("r2", 12.927923, 77.627107)
    c1 = GeoLocation("c1", 12.935800, 77.619234)
    c2 = GeoLocation("c2", 12.929327, 77.620556)
    pt1 = 0.5  # 30 minutes
    pt2 = 0.4  # 24 minutes

    orders = [
        Order(r1, c1, pt1),
        Order(r2, c2, pt2),
    ]

    optimizer = DeliveryOptimizer(delivery_executive, orders)
    best_route, best_time = optimizer.find_best_route()
    print(f"Best Route: {best_route}")
    print(f"Total Time: {round(best_time,2)} hours")

