from .best_route import GeoLocation, Order, DeliveryOptimizer

def test_delivery_optimizer():
    # Test Case 1
    delivery_executive = GeoLocation("delivery_executive", 12.935192, 77.624480)
    r1 = GeoLocation("r1", 12.934533, 77.626579)
    r2 = GeoLocation("r2", 12.927923, 77.627107)
    c1 = GeoLocation("c1", 12.935800, 77.619234)
    c2 = GeoLocation("c2", 12.929327, 77.620556)
    pt1 = 0.5  # 30 minutes
    pt2 = 0.4  # 24 minutes
    orders = [Order(r1, c1, pt1), Order(r2, c2, pt2)]
    optimizer = DeliveryOptimizer(delivery_executive, orders)
    best_route, best_time = optimizer.find_best_route()
    assert (
        best_route == "delivery_executive -> r1 -> r2 -> c2 -> c1"
    ), "Test Case 1 failed"
    print("Test Case 1 PASSED")

    # Test Case 2
    delivery_executive = GeoLocation("delivery_executive", 12.934533, 77.626579)
    r1 = GeoLocation("r1", 12.934533, 77.626579)
    c1 = GeoLocation("c1", 12.935800, 77.619234)
    pt1 = 0.5  # 30 minutes
    orders = [Order(r1, c1, pt1)]
    optimizer = DeliveryOptimizer(delivery_executive, orders)
    best_route, best_time = optimizer.find_best_route()
    assert best_route == "delivery_executive -> r1 -> c1", "Test Case 2 failed"
    print("Test Case 2 PASSED")

    # Test Case 3
    delivery_executive = GeoLocation("delivery_executive", 12.935192, 77.624480)
    r1 = GeoLocation("r1", 12.934533, 77.626579)
    r2 = GeoLocation("r2", 12.927923, 77.627107)
    c1 = GeoLocation("c1", 12.935800, 77.619234)
    c2 = GeoLocation("c2", 12.929327, 77.620556)
    pt1 = 0.5  # 30 minutes
    pt2 = 1.0  # 60 minutes
    orders = [Order(r1, c1, pt1), Order(r2, c2, pt2)]
    optimizer = DeliveryOptimizer(delivery_executive, orders)
    best_route, best_time = optimizer.find_best_route()
    assert (
        best_route == "delivery_executive -> r1 -> r2 -> c2 -> c1"
    ), "Test Case 3 failed"
    print("Test Case 3 PASSED")

    # Test Case 4
    delivery_executive = GeoLocation("delivery_executive", 12.935192, 77.624480)
    r1 = GeoLocation("r1", 12.934533, 77.626579)
    r2 = GeoLocation("r2", 12.927923, 77.627107)
    c1 = GeoLocation("c1", 12.935800, 77.619234)
    c2 = GeoLocation("c2", 12.929327, 77.620556)
    pt1 = 0.0  # 0 minutes
    pt2 = 0.0  # 0 minutes
    orders = [Order(r1, c1, pt1), Order(r2, c2, pt2)]
    optimizer = DeliveryOptimizer(delivery_executive, orders)
    best_route, best_time = optimizer.find_best_route()
    assert (
        best_route == "delivery_executive -> r1 -> r2 -> c2 -> c1"
    ), "Test Case 4 failed"
    print("Test Case 4 PASSED")



if __name__ == "__main__":
    # Run test cases
    test_delivery_optimizer()
