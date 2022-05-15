from numba import jit
import random


"""
C accelerated route calculator, couldn't get this to work properly
"""

@jit
def calc_route(start_pos, end_pos, NAV_MESH, walls):
    """
    Calculates the shortest route to a point using the navmesh points
    """

    if check_los_points(start_pos, end_pos, walls):
        return [end_pos]
    dist_start = {}
    dist_end = {}
    for nav_point in NAV_MESH:
        point = nav_point["point"]
        if check_los_points(start_pos, point, walls):
            dist_start[get_dist_points(start_pos, point)] = nav_point
        if check_los_points(end_pos, point, walls):
            dist_end[get_dist_points(end_pos, point)] = nav_point
    try:
        start_nav_point = dist_start[min(dist_start.keys())]
        end_nav_point = dist_end[min(dist_end.keys())]
    except:
        return [end_pos]

    complete_routes = []
    routes = []
    for conne in start_nav_point["connected"]:
        routes.append([start_nav_point["point"], conne])

    while routes != []:
        if len(complete_routes) > 3:
            # print("ROUTES SHOOT OVER 2000!")
            # for route in routes:
            #
            #     print(route)   #sometimes continues infinetely, so the loop must be broken
            break

        route = routes[random.randint(0,len(routes)-1)]

        routes.remove(route)
        point = route[-1]
        point_2 = get_point_from_list(point, NAV_MESH)
        if end_nav_point["point"] in point_2["connected"]:
            route.append(end_nav_point["point"])
            complete_routes.append(route)

        else:
            for point_3 in point_2["connected"]:
                if point_3 in route:
                    continue
                if route.copy() + [point_3] in routes:
                    continue
                routes.append(route.copy() + [point_3])
    shortest_route = {"dist" : 10000, "route" : []}


    for route in complete_routes:
        route_ref = {"dist" : 0, "route" : route}
        last_pos = start_pos
        for point in route:
            route_ref["dist"] += get_dist_points(last_pos, point)

        if route_ref["dist"] < shortest_route["dist"]:
            shortest_route = route_ref


    return shortest_route["route"]

@jit
def get_point_from_list(point,dict):
    for point_2 in dict:
        if point == point_2["point"]:
            return point_2

@jit
def check_los_points(p1,p2,los_walls):
    for wall_1 in los_walls:
        point_1 = wall_1[0]
        point_2 = wall_1[1]
        intersection = intersect(p1, p2, point_1, point_2)
        if intersection == True:
            return False
    return True

@jit
def get_dist_points(point_1,point_2):
    return math.sqrt((point_2[0] - point_1[0])**2 + (point_2[1] - point_1[1])**2)

@jit
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

@jit
def ccw(A,B,C):
    return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])


if __name__ == "__main__":
    print("testing")
    print(calc_route([0,0], [2,0], [[(1,2), (2,2)]], [[(-2,-2), (-2, -3)]]))
    print("completed")
