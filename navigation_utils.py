import math
import re
from dataclasses import dataclass


@dataclass
class DMS:
    degrees: int
    minutes: int
    seconds: float
    sign: int


### BASIC CONVERTERS AND DEGREE FUNCTIONS ###
def degrees_to_radians(deg: float) -> float:
    return math.radians(deg)


def radians_to_degrees(rad: float) -> float:
    return math.degrees(rad)


def degrees_cos(deg: float) -> float:
    return math.cos(math.radians(deg))


def degrees_sin(deg: float) -> float:
    return math.sin(math.radians(deg))


def degrees_acos(deg: float) -> float:
    return math.degrees(math.acos(deg))


def degrees_asin(deg: float) -> float:
    return math.degrees(math.asin(deg))


def degrees_atan(deg: float) -> float:
    return math.degrees(math.atan(deg))


def degrees_atan2(sin_numerator: float, cos_denominator: float) -> float:
    """returns a degree value for atan2. atan2 is a 2 argument form of atan, splitting the sinx/cosx parts.
    this allows us to pass signs in to the function, which is important since heading needs to encode +/- for e/w and n/s
    :returns atan2( sin_numerator / cos_denominator ), measured in degrees"""
    return math.degrees(math.atan2(sin_numerator, cos_denominator))


def degrees_heading_atan2(sin_numerator: float, cos_denominator: float) -> float:
    """function used to determine a heading from a sin(x) term and a cos(x) term.
    use this to get a signed degree value for the heading angle from a point
    also does angle % 360 in order to return a degree value mapping off 0* as north
    calls degrees_atan2 inside"""
    return degrees_atan2(sin_numerator, cos_denominator) % 360


### HELPER FUNCTIONS FOR PRACTICE PROBLEMS ###
def convert_time_diff_to_longitude_degrees(hours, minutes, seconds):
    hour_minutes = hours * 60
    hour_seconds = float(seconds) / 60
    total_minutes = hour_minutes + minutes + hour_seconds
    return total_minutes / 4


### PARSERS, DMS FUNCTIONS, DMS TO DECIMAL CONVERTERS ###
def dms_string_parser(dms_string: str) -> DMS:
    # count the number of number blocks, we have logic based on those
    count_pattern = r"[0-9]+(?:\.[0-9]+)?"
    groups_count = len(re.findall(count_pattern, dms_string))

    # depending on the number of groups in our input, search for degrees, minutes, seconds
    pattern = r"(?P<degrees_sign>-?)(?P<degrees>[0-9]{1,3})"
    if groups_count >= 2:
        pattern += r"[^0-9]+?(?P<minutes>[0-9]{1,3})"
    if groups_count >= 3:
        pattern += r"[^0-9]+?(?P<seconds>[0-9]{1,3}(?:\.[0-9]+)?)"
    if groups_count >= 4:
        raise ValueError(f"too many numeric components in input: {dms_string}")
    pattern += r"[^0-9]+?(?P<direction>[NSEW])?$"

    match = re.search(pattern, dms_string)

    degrees_sign = match.group("degrees_sign")
    direction = match.group("direction")

    # figure out the direction for the sign
    output_sign_multiplier = 1
    if degrees_sign is not None and degrees_sign != "" and direction is None:
        output_sign_multiplier = -1 if degrees_sign == "-" else 1
    if direction is not None:
        output_sign_multiplier = -1 if direction == "S" or direction == "W" else 1

    # create output dict
    output = DMS(int(match.group("degrees")), int(match.group("minutes")) if groups_count >= 2 else 0,
              float(match.group("seconds")) if groups_count >= 3 else 0,
              output_sign_multiplier)

    return output


def to_dms(degrees: int, minutes: int, seconds: float, sign: int) -> DMS:
    return DMS(int(degrees), int(minutes), float(seconds), int(sign))


def decimal_degree_string_parser(decimal_degree_string: str) -> float:
    """returns decimal degrees where S or W is negative from a string input of a decimal degree value. accepts degrees, direction, and/or negatives as input"""
    pattern = r"(?P<degrees_sign>-?)(?P<degrees>[0-9]{1,3}(?:\.[0-9]+)?)[^0-9NSEW]*?(?P<direction>[NSEW]?)$"
    match = re.search(pattern, decimal_degree_string)

    degrees_sign = match.group("degrees_sign")
    direction = match.group("direction")
    degrees = float(match.group("degrees"))

    output_sign_multiplier = 1
    if degrees_sign is not None and degrees_sign != "" and direction is None:
        output_sign_multiplier = -1 if degrees_sign == "-" else 1
    if direction is not None:
        output_sign_multiplier = -1 if direction == "S" or direction == "W" else 1

    return degrees * output_sign_multiplier


def convert_dms_object_to_decimal_degrees(dms: DMS) -> float:
    """uses the DMS class created in utils to return a degree with decimals, not minutes/seconds"""
    return float(dms.sign) * (float(dms.degrees) + float(dms.minutes) / 60 + float(dms.seconds) / 3600)


def convert_dms_string_to_decimal_degrees(dms_string: str) -> float:
    """assembler function which first parses a string input then converts that to decimal degrees using dms_string_parser() and convert_dms_object_to_decimal_degrees()"""
    dms_object = dms_string_parser(dms_string)
    return convert_dms_object_to_decimal_degrees(dms_object)


def minutes_from_degrees_no_whole_num(deg: float) -> float:
    """converts minutes after a decimal to degrees without returning the whole number of degrees"""
    whole_num = float(math.floor(abs(deg)))
    decimal = abs(deg) - whole_num
    return decimal * 3 / 5


def decimal_degrees_from_minutes_no_whole_num(minutes: float) -> float:
    """converts decimal degrees after a decimal to minutes without returning the whole number of degrees"""
    whole_num = float(math.floor(abs(minutes)))
    output = abs(minutes) - whole_num
    return output * 5 / 3


def degrees_to_minutes(deg: float) -> float:
    """converts a measurement in degrees.decimal_degrees to degrees.minutes"""
    sign = -1 if deg < 0 else 1
    whole_num = float(math.floor(abs(deg)))
    return (whole_num + minutes_from_degrees_no_whole_num(deg)) * sign


def minutes_to_degrees(minutes: float) -> float:
    """converts a measurement in degrees.minutes to degrees.decimal_degrees"""
    sign = -1 if minutes < 0 else 1
    whole_num = float(math.floor(abs(minutes)))
    return (whole_num + decimal_degrees_from_minutes_no_whole_num(minutes)) * sign


### HELPERS AND HANDLERS FOR FORMATTING, OUTPUT, REGULARIZATION ###
def normalize_longitude(longitude: float) -> float:
    """cleans up a degree measurement of longitude to make sure it's in range [-180, 180)"""
    return ((longitude + 180) % 360) - 180


def get_nautical_miles_from_central_angle_dms(angle: float) -> float:
    """converts degrees.minutes to nautical miles (minutes)"""
    extra_minutes = minutes_from_degrees_no_whole_num(angle) * 100
    degree_minutes = math.floor(angle) * 60
    return extra_minutes + degree_minutes


def get_nautical_miles_from_central_angle(angle: float) -> float:
    """converts degrees to nautical miles (minutes)"""
    return angle * 60


def get_central_angle_degrees_from_nautical_miles_dms(nautical_miles: float) -> float:
    """
    converts nautical miles to degrees (minutes)
    :param nautical_miles:
    :return: degrees.minutes
    """
    decimal = decimal_degrees_from_minutes_no_whole_num((nautical_miles % 60) / 100)
    rest = int(round(nautical_miles - (nautical_miles % 60)))/60
    return rest + decimal


def get_central_angle_degrees_from_nautical_miles(nautical_miles: float) -> float:
    """converts nautical miles (minutes) to degrees"""
    return nautical_miles / 60


def calculate_central_angle_from_lat(latitude: float) -> float:
    """use negatives for degrees south"""
    return 90 - latitude


def calculate_polar_surface_angle_between_points_from_lons_no_sign(m: float, n: float) -> float:
    """use negatives for degrees west, puts largest value first so you're always going to get a positive angle"""
    initial = max(m, n) - min(m, n)

    return initial if initial <= 180 else 360 - initial


def calculate_polar_surface_angle_between_points_from_lons_signed(lon1: float, lon2: float) -> float:
    """use negatives for degrees west. gives a signed value rather than giving some value between 0 and 180 in all cases"""
    return lon2 - lon1


def spherical_law_of_cosines_sas_get_central_angle_using_latlon(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """calculates internal angle p of great circle arc between latlong pairs m and n"""
    P = calculate_polar_surface_angle_between_points_from_lons_signed(lon1, lon2)
    m = calculate_central_angle_from_lat(lat1)
    n = calculate_central_angle_from_lat(lat2)
    p = spherical_law_of_cosines_sas_get_central_angle_given_lat_angles_and_polar_surface(m, n, P)
    return p


def spherical_law_of_cosines_sas_get_central_angle_given_lat_angles_and_polar_surface(l: float, r: float, P: float) -> float:
    """for surface points left and right, and given central polar angle, gives the measure of polar central angle p"""
    cosp_term1 = degrees_cos(l) * degrees_cos(r)
    cosp_term2 = degrees_sin(l) * degrees_sin(r) * degrees_cos(P)
    cosp = cosp_term1 + cosp_term2
    p = degrees_acos(cosp)
    return p


def spherical_law_of_cosines_sas_get_surface_angle(central_angle_corresponding: float, central_angle_2: float, central_angle_3: float) -> float:
    """calculates the surface angle corresponding to central_angle_corresponding based on central_angle_2 and central_angle_3.
    angles should be supplied in degrees with decimals following the decimal point"""
    term1 = degrees_cos(central_angle_corresponding) - degrees_cos(central_angle_2) * degrees_cos(central_angle_3)
    term2 = degrees_sin(central_angle_2) * degrees_sin(central_angle_3)

    cosM = term1 / term2

    return degrees_acos(cosM)


def spherical_law_of_cosines_asa_get_surface_angle(surface_angle_1: float, surface_angle_2: float, corresponding_central_angle: float) -> float:
    """uses the ASA version of the spherical law of cosines to derive the third (unknown) surface angle
    M = acos( -cosP cosN + sinP sinN cosm ) for a spherical triangle with surface angles M, N, P and central angles m, n, p"""
    term1 = -1 * degrees_cos(surface_angle_1) * degrees_cos(surface_angle_2)
    term2 = degrees_sin(surface_angle_1) * degrees_sin(surface_angle_2) * degrees_cos(corresponding_central_angle)
    return degrees_acos(term1 + term2)


def spherical_law_of_cosines_asa_get_central_angle(surface_angle_corresponding: float, surface_angle_1: float, surface_angle_2: float) -> float:
    """uses the ASA version of the spherical law of cosines to derive a central angle corresponding to one of the surface angles
    m = acos( (cosM + cosP cosN)/(sinP sinN) )for a spherical triangle with surface angles M, N, P and central angles m, n, p"""
    numerator = degrees_cos(surface_angle_corresponding) + degrees_cos(surface_angle_1) * degrees_cos(surface_angle_2)
    denominator = degrees_sin(surface_angle_1) * degrees_sin(surface_angle_2)
    return degrees_acos(numerator / denominator)


def spherical_law_of_sines_missing_central_angle(surface_angle_corresponding: float, other_central: float, other_surface: float) -> float:
    """finds a central angle based on the corresponding surface angle and a known central angle/surface angle corresponding pair"""
    sin_a = degrees_sin(surface_angle_corresponding) * degrees_sin(other_central) / degrees_sin(other_surface)
    return degrees_asin(sin_a)


def spherical_law_of_sines_missing_surface_angle(central_angle_corresponding: float, other_central: float, other_surface: float) -> float:
    """finds a surface angle based on the corresponding central angle and a known central angle/surface angle corresponding pair"""
    sin_A = degrees_sin(central_angle_corresponding) * degrees_sin(other_surface) / degrees_sin(other_central)
    return degrees_asin(sin_A)


def get_lat2_from_initial_point_azimuth_and_distance_in_nm(lat1: float, azimuth: float, central_angle_polar: float) -> float:
    """converts initial point, azimuth, and distance (in NM) to destination's latitude in degrees"""
    term1 = degrees_cos(central_angle_polar) * degrees_sin(lat1)
    term2 = degrees_sin(central_angle_polar) * degrees_cos(lat1) * degrees_cos(azimuth)
    return degrees_asin(term1 + term2)


def get_clairaut_constant_from_heading_and_lat(current_lat: float, current_heading: float) -> float:
    """gets the Clairaut constant c for a given great circle sin(heading) * cos(lat) = c
    :param current_lat: latitude of current point
    :param current_heading: heading of current point
    :return: float, Clairaut constant c"""
    return degrees_sin(current_heading) * degrees_cos(current_lat)


def get_sin_of_heading_from_lat_clairaut(current_lat: float, clairaut_constant: float) -> float:
    """uses the Clairaut constant c for a great circle [sin(heading) * cos(lat) = c] to compute the current heading
    :param current_lat: latitude of current point
    :param clairaut_constant: Clairaut constant c for the given great circle
    :return: float, sin(heading) of the current point

    WARNING: because this returns the sin(heading), if you simply take degrees_asin(this) you will potentially miss your heading
    because heading is a value 0-360 and not -90 to 90"""
    return clairaut_constant / degrees_cos(current_lat)


def get_lon2_from_point1_lat2_azimuth_and_distance_in_nm(lat1: float, lon1: float, lat2: float, azimuth: float, central_angle_polar: float) -> float:
    """converts lat2, lon1, azimuth, and distance (in NM) to destination's longitude in degrees
    need to use atan2 here as well for hemisphere correctness. so we require lat1 in order to use the four angle relationships to calculate sinP and cosP"""
    sinP = degrees_sin(azimuth) * degrees_sin(central_angle_polar) / degrees_cos(lat2)
    cosP_numerator = degrees_cos(central_angle_polar) - degrees_cos(calculate_central_angle_from_lat(lat1)) * degrees_cos(calculate_central_angle_from_lat(lat2))
    cosP_denominator = degrees_sin(calculate_central_angle_from_lat(lat1)) * degrees_sin(calculate_central_angle_from_lat(lat2))
    cosP = cosP_numerator / cosP_denominator
    return normalize_longitude(lon1 + degrees_atan2(sinP, cosP))


def get_point2_from_point1_azimuth_and_distance(lat1: float, lon1: float, azimuth: float, central_angle_polar: float) -> tuple:
    lat2 = get_lat2_from_initial_point_azimuth_and_distance_in_nm(lat1, azimuth, central_angle_polar)
    lon2 = get_lon2_from_point1_lat2_azimuth_and_distance_in_nm(lat1, lon1, lat2, azimuth, central_angle_polar)
    return lat2, normalize_longitude(lon2)


def get_lons_for_lat_intercepts_from_point1_lat2_azimuth(lat1: float, lon1: float, lat2: float, azimuth: float) -> tuple:
    """function for debug. returns BOTH longitudes for the points where a given great circle (defined by origin and azimuth) crosses a given latitude
    :returns ({"lat": float, "lon": float}, {"lat": float, "lon": float}) for intercept1, intercept2"""
    distances = get_distance_between_points_lat1_lat2_azimuth_using_auxiliary_angle_id_two_solutions(lat1, lat2, azimuth)
    points = []
    for distance in distances:
        points.append(get_point2_from_point1_azimuth_and_distance(lat1, lon1, azimuth, distance))
    return {"lat": points[0][0], "lon": points[0][1]}, {"lat": points[1][0], "lon": points[1][1]}


def get_point2_from_point1_azimuth_and_distance_in_nm(lat1: float, lon1: float, azimuth: float, distance: float) -> tuple:
    """given a starting point and an azimuth, calculates the latlong of destination coords. returns (lat2, lon2)"""
    central_angle_polar = get_central_angle_degrees_from_nautical_miles(distance)
    return get_point2_from_point1_azimuth_and_distance(lat1, lon1, azimuth, central_angle_polar)


def get_initial_heading_from_point1_and_point2(lat1: float, lon1: float, lat2: float, lon2: float, verbose: bool=False) -> float:
    """given 2 latlon coordinates, gives you the initial heading to reach the second from the first
    uses math.atan2 to get a signed version of the heading.
    to use this we need to calculate sin M and cos M in order to pass them to atan2
    """
    if verbose:
        print("START get_initial_heading_from_point1_and_point2:","lat1:", lat1, "lon1:", lon1, "lat2:", lat2, "lon2:", lon2)
    # find central angle p corresponding to length of great circle arc
    p = spherical_law_of_cosines_sas_get_central_angle_using_latlon(lat1, lon1, lat2, lon2)
    # magnitude gets how big the angle needs to be: basically n/s sign
    cosM_numerator = (degrees_cos(calculate_central_angle_from_lat(lat2)) - degrees_cos(calculate_central_angle_from_lat(lat1)) * degrees_cos(p))
    cosM_denominator = degrees_sin(calculate_central_angle_from_lat(lat1)) * degrees_sin(p)
    cosM = cosM_numerator / cosM_denominator
    sinM_numerator = degrees_sin(calculate_polar_surface_angle_between_points_from_lons_signed(lon1, lon2)) * degrees_sin(calculate_central_angle_from_lat(lat2))
    sinM_denominator = degrees_sin(p)
    sinM = sinM_numerator / sinM_denominator
    if verbose:
        print("p:", p, "cosM_numerator:", cosM_numerator, "cosM_denominator:", cosM_denominator, "sinM_numerator:", sinM_numerator)
        print("cosM:", cosM, "sinM:", sinM)
        print("END get_initial_heading_from_point1_and_point2")

    return degrees_heading_atan2(sinM, cosM)


def get_point2_surface_angle_using_asa_from_point1_lon2_and_azimuth(lat1: float, lon1: float, lon2: float, azimuth: float) -> float:
    """using ASA version of spherical law of cosines, calculates the surface angle for point2 from point1 lat/lon, lon of point2, and the azimuth for point1"""
    term1 = -1 * degrees_cos(azimuth) * degrees_cos(calculate_polar_surface_angle_between_points_from_lons_signed(lon1, lon2))
    term2 = degrees_sin(azimuth) * degrees_sin(calculate_polar_surface_angle_between_points_from_lons_signed(lon1, lon2)) * degrees_cos(calculate_central_angle_from_lat(lat1))
    return degrees_acos(term1 + term2)


def get_vertex_latitude(lat1: float, azimuth: float) -> float:
    """gets the latitude of the closest vertex, based on the azimuth from the origin and the latitude of the origin. if cos(azimuth) > 0, we're heading north, otherwise south
    sin 90 / sin 90 - lat1 = sin azimuth / sin 90 - lat2
    1 / cos lat1 = sin azimuth / cos lat2
    1 = sin azimuth cos lat1 / cos lat2
    cos lat2 = sin azimuth cos lat1"""
    absolute_value = degrees_acos(abs(degrees_cos(lat1) * degrees_sin(azimuth)))
    return absolute_value if degrees_cos(azimuth) > 0 else -1 * absolute_value


def is_latitude_reachable(lat1: float, lat2: float, azimuth: float) -> bool:
    """uses get_vertex_latitude to determine if the great circle given by azimuth reaches lat2"""
    return abs(get_vertex_latitude(lat1, azimuth)) >= abs(lat2)


def get_both_vertex_latitudes(lat1: float, azimuth: float) -> tuple:
    """gets both vertex latitudes for a given great circle defined by the latitude of the origin and the azimuth. no lon term
    since any great circle in the same direction from the same lat will have the same max and min lats.

    calls get_vertex_latitude twice

    :param lat1: latitude of the origin point
    :param azimuth: azimuth from the origin point
    :returns (vertex_latitude1, vertex_latitude2) in no particular order. vertex_latitude2 could be the closer one!"""
    return get_vertex_latitude(lat1, azimuth), -1 * get_vertex_latitude(lat1, azimuth)


def get_distances_to_both_vertices(lat1: float, azimuth: float) -> tuple:
    """finds distances to both vertex latitudes given the origin latitude and the initial azimuth.
    calls get_both_vertex_latitudes. then uses those in get_distance_between_points_lat1_lat2_azimuth_using_auxiliary_angle_id_two_solutions
    we find the maximum of those two solutions for each given vertex latitude and use that. this is correct because that function
    will either return two identical values, or will return two values which are +-180 from a defined value. choosing the max just ensures that
    both distances we return will be positive. this is desirable because we conceive of the azimuth as defining a single direction of motion for the full
    navigation
    :param lat1: latitude of the origin point
    :param azimuth: azimuth from the origin point

    :returns distance1, distance2 in form of degrees of central angle"""
    vertex_lats = get_both_vertex_latitudes(lat1, azimuth)

    distances_to_vertex = []
    for lat in vertex_lats:
        distances_to_vertex.append(max(get_distance_between_points_lat1_lat2_azimuth_using_auxiliary_angle_id_two_solutions(lat1, lat, azimuth)))

    return distances_to_vertex[0], distances_to_vertex[1]


def get_distances_to_both_vertices_tag_with_latitudes(lat1: float, azimuth: float, verbose: bool=False) -> tuple:
    """same as get_distances_to_both_vertices except different return data structure
    :param lat1: latitude of the origin point
    :param azimuth: azimuth from the origin point

    :returns ({"lat": vertex_lat_1, "distance": distance1}, {"lat": vertex_lat_2, "distance": distance2}) distances in form of central angle degrees. the vertex closer to the origin is given first"""
    vertex_lats = get_both_vertex_latitudes(lat1, azimuth)

    distances_to_vertex = []
    for lat in vertex_lats:
        distances_to_vertex.append({"lat": lat, "distance": max(get_distance_between_points_lat1_lat2_azimuth_using_auxiliary_angle_id_two_solutions(lat1, lat, azimuth))})

    if verbose:
        print(distances_to_vertex)

    if distances_to_vertex[0]["distance"] < distances_to_vertex[1]["distance"]:
        closer_vertex = distances_to_vertex[0]
        further_vertex = distances_to_vertex[1]
    else:
        closer_vertex = distances_to_vertex[1]
        further_vertex = distances_to_vertex[0]

    if verbose:
        print(closer_vertex, further_vertex)

    return closer_vertex, further_vertex


def get_distance_between_points_lat1_lat2_azimuth_using_auxiliary_angle_id_two_solutions(lat1: float, lat2: float, azimuth: float) -> tuple:
    """designed to be called downstream of sanitized inputs (i.e. check is_latitude_reachable). if you don't ensure that you are passing two valid latitudes, this WILL silently warp them into true values
    because we bound value C/R (of which we take acos to get the return values) in order to ensure that the values passed to acos will not return a ValueError

    uses the auxiliary angle ID A cosp + B cosp = C (from cosm = cosn cosp + sinn sinp cosM) and C = R cos( p - x) to calculate the distance to point2
    since A and B are known, as is C, we can use them as constants and can derive that R = sqrt( A^2 + B^2 ). x = atan2( B / A).
    then we can solve C = R cos( p - x).

    this function returns two values since there are two valid solutions: either acos( C / R ) + x or acos( C / R ) - x
    you need to sort through these using a handler to find which is correct

    :returns (degrees_acos(C / R) + x, degrees_acos(C / R) - x)"""
    A = degrees_cos(90 - lat1)
    B = degrees_sin(90 - lat1) * degrees_cos(azimuth)
    C = degrees_cos(90 - lat2)
    R = math.sqrt(A**2 + B**2)
    x = degrees_atan2(B, A)
    # lots of floating points. do this to ensure that values which drift outside of [-1, 1] can actually work
    bounded = max(-1.0, min(1.0, C/R))
    return x + degrees_acos(bounded), x - degrees_acos(bounded)


def get_distance_between_points_lat1_lat2_azimuth_distance_so_far(lat1: float, lat2: float, azimuth: float, distance_so_far: float, verbose: bool=False) -> float:
    """to use the function to get distance between lat1 and lat2 using an azimuth, we need to sort out which of the two possible solutions is correct.
    this handler is designed for use when calculating hops to download the next tile. it takes in the distance traveled from the origin to the corner point of the previous hop
    and identifies which of the possible solutions comes next (i.e. min() of the options where distance_to_point > distance_so_far)
    :param lat1: latitude of the first point
    :param lat2: latitude of the second point
    :param azimuth: azimuth from first point to the second
    :param distance_so_far: distance traveled from the origin to the corner point of the previous hop IN DEGREES"""
    possible_distances = [x for x in get_distance_between_points_lat1_lat2_azimuth_using_auxiliary_angle_id_two_solutions(lat1, lat2, azimuth)]
    distances_ahead = [x for x in possible_distances if x > distance_so_far]
    if len(distances_ahead) == 0:
        raise ValueError(f"all possible distances: {possible_distances} are behind us when we're {distance_so_far} into the trip")
    if verbose:
        print(possible_distances, distances_ahead)
    return min(distances_ahead)


def get_lat3_given_point1_point2_lon3(lat1: float, lon1: float, lat2: float, lon2: float, lon3: float, verbose: bool=False) -> float:
    """uses an arc of a great circle between point1 and point2 to find the latitude of a point with lon3 somewhere on the great circle defined by those two points
    useful when we know what two points are and care about something in the middle or elsewhere along the line.
    :param lat1: latitude of the first point
    :param lon1: longitude of the first point
    :param lat2: latitude of the second point (arc endpoint)
    :param lon2: longitude of the second point (arc endpoint)
    :param lon3: longitude of the third, target point which lies on an arc between point1 and point3
    :param verbose: prints extra debug messages

    :returns: lat3: latitude of the target point, as a float, in degrees"""
    if verbose:
        print("lat1:", lat1, "lon1:", lon1, "lat2:", lat2, "lon2:", lon2, "lon3:", lon3)
    num_part_one = degrees_sin(lat1) * degrees_cos(lat2) * degrees_sin(lon3 - lon2)
    num_part_two = degrees_sin(lat2) * degrees_cos(lat1) * degrees_sin(lon3 - lon1)
    numerator = num_part_one - num_part_two
    denominator = degrees_cos(lat1) * degrees_cos(lat2) * degrees_sin(lon1 - lon2)
    return degrees_atan(numerator/denominator)


def get_lat2_given_point1_lon2_azimuth(lat1: float, lon1: float, lon2: float, azimuth: float, verbose: bool=False) -> float:
    """function which returns the lat2 of a great circle crossing a given longitude given the origin point of that great circle, the target longitude, and the azimuth
    actually a handler function. calculates destination_heading, polar_surface_angle, and then uses those and azimuth to determine which of two sub-functions will be
    more likely to return a robust and accurate answer. then calls that function and returns the answer.
    :param lat1: latitude of the first point
    :param lon1: longitude of the first point
    :param lon2: longitude of the second point
    :param azimuth: azimuth from first point to the second
    :param verbose: prints extra debug messages

    determines whether to call:
    - get_lat2_given_point1_lon2_azimuth_atan2_inside_handler
    - get_lat2_given_point1_lon2_azimuth_acos_inside_handler

    :returns lat2: latitude of the second point as a float"""
    if verbose:
        print("get_lat2_given_point1_lon2_azimuth called with verbose=True")
        print("lat1: ", lat1, "lon1", lon1, "lon2", lon2, "azimuth", azimuth)

    if degrees_sin(azimuth) < 0:
        azimuth = 360 - azimuth
        function_lon2 = 2 * lon1 - lon2
    else:
        function_lon2 = lon2

    destination_heading = get_point2_surface_angle_using_asa_from_point1_lon2_and_azimuth(lat1, lon1, function_lon2, azimuth)
    polar_surface_angle = calculate_polar_surface_angle_between_points_from_lons_signed(lon1, function_lon2)

    if verbose:
        print("destination_heading: ", destination_heading, "polar_surface_angle: ", polar_surface_angle)

    # atan2 seems to be more stable in more cases
    output = get_lat2_given_point1_lon2_azimuth_atan2_inside_handler(lat1, azimuth, destination_heading, polar_surface_angle, verbose)

    if verbose:
        # no verbose because we're really just trying to see the comparative here! but I guess you can edit it easy enough.
        print("atan2: ", get_lat2_given_point1_lon2_azimuth_atan2_inside_handler(lat1, azimuth, destination_heading, polar_surface_angle))
        print("acos: ", get_lat2_given_point1_lon2_azimuth_acos_inside_handler(lat1, azimuth, destination_heading, polar_surface_angle))
        # a final calculation which needs some other info
        test_distance_angle = 20
        second_point_latlon = get_point2_from_point1_azimuth_and_distance(lat1, lon1, azimuth, test_distance_angle)
        print("atan: ", get_lat3_given_point1_point2_lon3(lat1, lon1, second_point_latlon[0], second_point_latlon[1], lon2))

    # old version sometimes calculated output based on acos
    #if abs(destination_heading % 180) < tolerance and abs(polar_surface_angle) < tolerance:
        #output = get_lat2_given_point1_lon2_azimuth_acos_inside_handler(lat1, azimuth, destination_heading, polar_surface_angle, verbose)

    return output


def get_lat2_given_point1_lon2_azimuth_atan2_inside_handler(lat1: float, azimuth: float, destination_heading: float, polar_surface_angle: float, verbose: bool=False) -> float:
    """ function internal to get_lat2_given_point1_lon2_azimuth_atan2().
    gets the latitude of a second point from the first point, azimuth, heading angle at the destination, and surface angle at the pole
    not intended to be used independently

    this function is a little more robust around the poles than the acos version because it has certain values that are likely to be a bit larger.
    therefore it is less susceptible to error caused by conversion in and out of floats

    :returns float, latitude of a second point from the first point"""
    if verbose:
        print("lat1: ", lat1, "azimuth: ", azimuth, "destination_heading: ", destination_heading, "polar_surface_angle: ", polar_surface_angle)

    sinm = degrees_sin(azimuth) * degrees_sin(90 - lat1) / degrees_sin(destination_heading)
    cosm_numerator = degrees_cos(azimuth) + degrees_cos(polar_surface_angle) * degrees_cos(destination_heading)
    cosm_denominator = degrees_sin(polar_surface_angle) * degrees_sin(destination_heading)
    cosm = cosm_numerator / cosm_denominator
    return 90 - degrees_atan2(sinm, cosm)


def get_lat2_given_point1_lon2_azimuth_acos_inside_handler(lat1: float, azimuth: float, destination_heading: float, polar_surface_angle: float, verbose: bool=False) -> float:
    """ function internal to get_lat2_given_point1_lon2_azimuth_atan2().
        gets the latitude of a second point from the first point, azimuth, heading angle at the destination, and surface angle at the pole
        not intended to be used independently

        this function is a little more robust than the atan2 version in certain circumstances where the destination heading is near 90/270 because it is not dividing by extremely small values
        therefore it is less susceptible to error caused by conversion in and out of floats

        :returns float, latitude of a second point from the first point"""
    if verbose:
        print("lat1: ", lat1, "azimuth: ", azimuth, "destination_heading: ", destination_heading, "polar_surface_angle: ", polar_surface_angle)

    return 90 - spherical_law_of_cosines_asa_get_central_angle(destination_heading, azimuth, polar_surface_angle)


def get_lat2_given_point1_lon2_azimuth_atan2(lat1: float, lon1: float, lon2: float, azimuth: float, verbose: bool=False) -> float:
    """gets the latitude of a second point from the first point, the azimuth (surface angle) of the first point, and the longitude of the second point.
    uses atan2 since this seems to work a little better sometimes
    NOTE: this will CRASH on a divide by 0 error if lon1 and lon2 are the same!!!!!!"""
    # westward headings must be reflected because law of sines is unaaware/unable to differentiate
    if degrees_sin(azimuth) < 0:
        azimuth = 360 - azimuth
        function_lon2 = 2 * lon1 - lon2
    else:
        function_lon2 = lon2

    if verbose:
        print(lat1, lon1, function_lon2, azimuth)

    destination_heading = get_point2_surface_angle_using_asa_from_point1_lon2_and_azimuth(lat1, lon1, function_lon2, azimuth)
    polar_surface_angle = calculate_polar_surface_angle_between_points_from_lons_signed(lon1, function_lon2)
    sinm = degrees_sin(azimuth) * degrees_sin(90 - lat1) / degrees_sin(destination_heading)
    cosm_numerator = degrees_cos(azimuth) + degrees_cos(polar_surface_angle) * degrees_cos(destination_heading)
    cosm_denominator = degrees_sin(polar_surface_angle) * degrees_sin(destination_heading)
    cosm = cosm_numerator / cosm_denominator
    return 90 - degrees_heading_atan2(sinm, cosm)


def get_lat2_given_point1_lon2_azimuth_acos(lat1: float, lon1: float, lon2: float, azimuth: float, verbose: bool=False) -> float:
    """gets the latitude of a second point from the first point, the azimuth (surface angle) of the first point, and the longitude of the second point.
    uses the ASA version of the spherical law of cosines to get the heading angle of the destination.
    then uses the destination heading, the polar heading, and the ASA spherical law of cosines to get the central angle corresponding to the original azimuth.
    that should be safe because acos returns a value [0, 180] which we can safely subtract from 90 to get a valid latitude

    NOTE: this will CRASH on a divide by 0 error if lon1 and lon2 are the same!!!!!!

    USED TO USE: spherical law of sines to get side lengths, put through an atan2 for correct sign"""
    # we need to flip the azimuth + lon if azimuth is west-facing
    if degrees_sin(azimuth) < 0:
        azimuth = 360 - azimuth
        function_lon2 = 2 * lon1 - lon2
    else:
        function_lon2 = lon2

    if verbose:
        print(lat1, lon1, function_lon2, azimuth)

    # keeping the old version because if i have to repurpose or reuse this it would be really annoying to write/derive again
    #sinm = degrees_sin(azimuth) * degrees_sin(90 - lat1) / degrees_sin(destination_heading)
    #cosm_numerator = degrees_cos(azimuth) + degrees_cos(calculate_polar_surface_angle_between_points_from_lons_signed(lon1, lon2)) * degrees_cos(destination_heading)
    # cosm_denominator = degrees_sin(calculate_polar_surface_angle_between_points_from_lons_signed(lon1, lon2)) * degrees_sin(destination_heading)
    # cosm = cosm_numerator / cosm_denominator
    # return 90 - degrees_heading_atan2(sinm, cosm)

    destination_heading = get_point2_surface_angle_using_asa_from_point1_lon2_and_azimuth(lat1, lon1, function_lon2, azimuth)
    polar_surface_angle = calculate_polar_surface_angle_between_points_from_lons_signed(lon1, function_lon2)

    if verbose:
        print(lon1, function_lon2)
        print(polar_surface_angle, destination_heading)

    return 90 - spherical_law_of_cosines_asa_get_central_angle(azimuth, destination_heading, polar_surface_angle)


def get_lon2_given_point1_lat2_azimuth_distance_so_far(lat1: float, lon1: float, lat2: float, azimuth: float, distance_so_far: float, verbose: bool=False) -> float:
    """
    gets the lon2 of a given point, given that point's latitude, an origin point, and an azimuth from the origin. also the distance traveled so far
    needs to have feasibility checked upstream, ideally using is_latitude_reachable before calling
    :returns the target point's lon2
    """
    p = get_distance_between_points_lat1_lat2_azimuth_distance_so_far(lat1, lat2, azimuth, distance_so_far, verbose)
    cosP_numerator = degrees_cos(p) - degrees_cos(90 - lat1) * degrees_cos(90 - lat2)
    cosP_denominator = degrees_sin(90 - lat1) * degrees_sin(90 - lat2)
    cosP = cosP_numerator / cosP_denominator
    sinP = degrees_sin(azimuth) * degrees_sin(p) / degrees_sin(90 - lat2)
    return normalize_longitude(lon1 + degrees_atan2(sinP, cosP))


### DEBUG AND UNIT TEST ###
def points_test(lat1: float, lon1: float, lat2: float, lon2: float, azimuth: float=None, distance: float=None, error: float=0.0001, prints: bool=True) -> bool:
    """ made to be a unit test/for testing suite
    runs a check on a pair of lat/lon coordinates to test whether you can back derive all values correctly using formulas in navigation_utils_repo.py
    you don't need to supply azimuth and distance, but you can
    error is set to 0.0001 by default. that's roughly 11 meters. Copernicus satellite data (this is intended for use in an app using that dataset, and focusing on elevation) has a resolution of 30m. so that's more than sufficient
    tests the validity (i.e. uses) the following functions, and any they depend on"""
    if distance is None:
        distance = get_nautical_miles_from_central_angle(spherical_law_of_cosines_sas_get_central_angle_using_latlon(lat1, lon1, lat2, lon2))

    if azimuth is None:
        azimuth = get_initial_heading_from_point1_and_point2(lat1, lon1, lat2, lon2)

    if prints:
        print("distance: ", distance, "azimuth: ", azimuth, "lat1/lon1", lat1, lon1, "lat2/lon2", lat2, lon2)

    # get a test point2 and check it against the point2 given in arguments
    test_point2_lat, test_point2_lon = get_point2_from_point1_azimuth_and_distance_in_nm(lat1, lon1, azimuth, distance)
    acceptable_test_point2_and_real_point2_lat = abs(lat2 - test_point2_lat) < error
    acceptable_test_point2_and_real_point2_lon = abs(lon2 - test_point2_lon) < error
    derives_point2_from_point1_azimuth_distance = acceptable_test_point2_and_real_point2_lat and acceptable_test_point2_and_real_point2_lon
    if prints:
        print("point2 from azimuth and distance:\n", "\tlat:", acceptable_test_point2_and_real_point2_lat, "\n",
              "\tlon:", acceptable_test_point2_and_real_point2_lon, "\n",
              "\tboth:", derives_point2_from_point1_azimuth_distance, "\n",
              "\ttest_point2:", test_point2_lat, test_point2_lon)

    # is the distance between point1 and test_point2 within error bounds?
    test_distance = get_nautical_miles_from_central_angle(spherical_law_of_cosines_sas_get_central_angle_using_latlon(lat1, lon1, test_point2_lat, test_point2_lon))
    correct_test_distance = abs(test_distance - distance) < error
    if prints:
        print("correct test distance: ", correct_test_distance)

    # from the test point2, can we get the reverse heading and find point1 again?
    test_reverse_heading = get_initial_heading_from_point1_and_point2(test_point2_lat, test_point2_lon, lat1, lon1)
    test_reverse_point1_lat, test_reverse_point1_lon = get_point2_from_point1_azimuth_and_distance_in_nm(test_point2_lat, test_point2_lon, test_reverse_heading, test_distance)
    acceptable_test_point1_and_real_point1_lat = abs(test_reverse_point1_lat - lat1) < error
    acceptable_test_point1_and_real_point1_lon = abs(test_reverse_point1_lon - lon1) < error
    derives_point1_from_test_point2_reverse_azimuth_and_distance = acceptable_test_point1_and_real_point1_lon and acceptable_test_point1_and_real_point1_lat
    if prints:
        print("point1 from test_point2 and reverse_heading and distance:\n", "\tlat:", acceptable_test_point1_and_real_point1_lat, "\n", "\tlon:", acceptable_test_point1_and_real_point1_lon, "\n", "\tboth:", derives_point1_from_test_point2_reverse_azimuth_and_distance, "test_reverse_point1:", test_reverse_point1_lat, test_reverse_point1_lon)

    return derives_point1_from_test_point2_reverse_azimuth_and_distance and derives_point2_from_point1_azimuth_distance and correct_test_distance


def oblique_angle_test(test: dict, verbose: bool=True) -> bool:
    """test verifying the behavior of get_lat2_given_point1_lon2_azimuth function given certain troublesome inputs. eventually
    found that the root cause was the need to flip the spherical triangle, or flip lon value, when azimuth faced west. but all this was obviated by
    get_lat3_given_point1_point2_lon3(). currently, the function called here is not used in my copernicus library but if run with verbose=True will still output
    a comparison between various methods of calculating the relevant lat2."""
    if verbose:
        print("oblique_angle_test:")
        print("test:", test)
    test_lat2_without_point3 = get_lat2_given_point1_lon2_azimuth(test["lat1"], test["lon1"], test["lon2"], test["azimuth"], verbose)
    test_point2 = get_point2_from_point1_azimuth_and_distance(test["lat1"], test["lon1"], test["azimuth"], get_central_angle_degrees_from_nautical_miles(50))
    test_lat3 = get_lat3_given_point1_point2_lon3(test["lat1"], test["lon1"], test_point2[0], test_point2[1], test["lon2"], verbose)
    if verbose:
        print("test_lat2_without_point3:", test_lat2_without_point3, "test_point2:", test_point2, "test_lat3:", test_lat3)
    return test_lat2_without_point3 == test_lat3
