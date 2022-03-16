from point import Point

def on_segment(p: Point, q: Point, r: Point):
    """
    Given three collinear points p, q, r, the function checks if
    point q lies on line segment 'pr'
    """
    if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False

def orientation(p: Point, q: Point, r: Point):
    """
    to find the orientation of an ordered triplet (p,q,r)
    function returns the following values:
    0 : Collinear points
    1 : Clockwise points
    2 : Counterclockwise

    See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
    for details of below formula.
    """

    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):

        # Clockwise orientation
        return 1
    elif (val < 0):

        # Counterclockwise orientation
        return 2
    else:

        # Collinear orientation
        return 0

def do_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    """
    Returns true if the line segment 'ab' and 'cd' intersect.
    """

    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)

    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases

    # a , b and c are collinear and c lies on segment ab
    if ((o1 == 0) and on_segment(a, c, b)):
        return True

    # a , b and d are collinear and d lies on segment ab
    if ((o2 == 0) and on_segment(a, d, b)):
        return True

    # c , d and a are collinear and a lies on segment cd
    if ((o3 == 0) and on_segment(c, a, d)):
        return True

    # c , d and b are collinear and b lies on segment cd
    if ((o4 == 0) and on_segment(c, b, d)):
        return True

    # If none of the cases
    return False

def get_intersect(a: Point, b: Point, c: Point, d: Point) -> Point:
    """
    Get the intersection point between two line segments
    Parameters
    ----------
    a : Point
        start point of first line segment ab
    b: Point
        end point of first line segment ab
    c: Point
        start point of second line segment cd
    d: Point
        end point of second line segment cd
    """
    if not do_intersect(a, b, c, d):
        return None
    
    # Line ab represented as a1x + b1y = c1
    a1 = b.y - a.y
    b1 = a.x - b.x
    c1 = a1 * a.x + b1 * a.y

    #line cd represented as a2x + b2y = c2
    a2 = d.y - c.y
    b2 = c.x - d.x
    c2 = a2 * c.x + b2 * c.y

    determinant = a1 * b2 - a2 * b1

    #lines are parallel - return either c or d as intersection point
    if determinant == 0:
        if on_segment(a, c, b):
            return c
        else:
            return d

    x = (b2 * c1 - b1 * c2) / determinant
    y = (a1 * c2 - a2 * c1) / determinant
    return Point(x, y)
