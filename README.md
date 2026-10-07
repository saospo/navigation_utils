Simple library for handling spherical trigonometry math, primarily denominated in degrees (so watch those floats!).

Various functionality enclosed. Major groupings:

- a class DMS (degrees, minutes, seconds) which handles data in that format.
- various simple wrappers on math functions which allow easy use of degree-based values as opposed to radian values. (and alternate versions of some of the above which allow mathematically valid but less human-digestible values to be converted to relevant values: think compass headings, or longitude.)
- functions designed to help complete the problem set found on the Stonybrook spherical trig page (https://www.math.stonybrook.edu/~tony/archive/336f06/spher-trig.html)
- functions for parsing string-based inputs in DMS and decimal degree formats.
- a suite of functions using the spherical laws of sine and cosine to allow for calculation of various latitudes, longitudes, central angle distances, and heading values from different pieces of that information
- further functions based on compositions and derivations of the above which allow users to calculate key data points about a great circle route
- functions built to automate unit tests for certain parts of the library

Also included are a variety of test suites yours truly used when writing this library.

Sources:

I primarily used the following two pages. I developed my intuition by grinding against that Stonybrook page for a day. Some of the more advanced identities (Clairaut's, vector-based circle identification) come from Aviation Formulary. It's a great resource.

Aviation Formulary: https://edwilliams.org/avform147.htm
Stonybrook spherical trig: https://www.math.stonybrook.edu/~tony/archive/336f06/spher-trig.html

I have also used these for reference.

Wikipedia on spherical trig: https://en.wikipedia.org/wiki/Spherical_trigonometry
Wikipedia on great circles: https://en.wikipedia.org/wiki/Great-circle_navigation

Dependencies:
math
re
dataclasses.dataclass

Classes:
DMS
- dataclasses.dataclass for holding values in Degrees, Minutes, Seconds

Functions:
- Degree math handlers:
  - degrees_to_radians(deg: float) -> float
  - radians_to_degrees(rad: float) -> float
  - degrees_cos(deg: float) -> float
  - degrees_sin(deg: float) -> float
  - degrees_acos(deg: float) -> float
  - degrees_asin(deg: float) -> float
  - degrees_atan(deg: float) -> float
  - degrees_atan2(sin_numerator: float, cos_denominator: float) -> float
  - degrees_heading_atan2(sin_numerator: float, cos_denominator: float) -> float
- Parsing and conversion:
  - convert_time_diff_to_longitude_degrees(hours, minutes, seconds)
  - dms_string_parser(dms_string: str) -> DMS
  - to_dms(degrees: int, minutes: int, seconds: float, sign: int) -> DMS
  - decimal_degree_string_parser(decimal_degree_string: str) -> float
  - convert_dms_object_to_decimal_degrees(dms: DMS) -> float
  - convert_dms_string_to_decimal_degrees(dms_string: str) -> float
  - minutes_from_degrees_no_whole_num(deg: float) -> float
  - decimal_degrees_from_minutes_no_whole_num(minutes: float) -> float
  - degrees_to_minutes(deg: float) -> float
  - minutes_to_degrees(minutes: float) -> float
  - normalize_longitude(longitude: float) -> float
  - get_nautical_miles_from_central_angle_dms(angle: float) -> float
  - get_nautical_miles_from_central_angle(angle: float) -> float
  - get_central_angle_degrees_from_nautical_miles_dms(nautical_miles: float) -> float
  - get_central_angle_degrees_from_nautical_miles(nautical_miles: float) -> float
- Conversions between latitudes, longitudes, and angle measurements
  - calculate_central_angle_from_lat(latitude: float) -> float
  - calculate_polar_surface_angle_between_points_from_lons_no_sign(m: float, n: float) -> float
  - calculate_polar_surface_angle_between_points_from_lons_signed(lon1: float, lon2: float) -> float
- Spherical law of cosines
  - spherical_law_of_cosines_sas_get_central_angle_using_latlon(lat1: float, lon1: float, lat2: float, lon2: float) -> float
  - spherical_law_of_cosines_sas_get_central_angle_given_lat_angles_and_polar_surface(l: float, r: float, P: float) -> float
  - spherical_law_of_cosines_sas_get_surface_angle(central_angle_corresponding: float, central_angle_2: float, central_angle_3: float) -> float
  - spherical_law_of_cosines_asa_get_surface_angle(surface_angle_1: float, surface_angle_2: float, corresponding_central_angle: float) -> float
  - spherical_law_of_cosines_asa_get_central_angle(surface_angle_corresponding: float, surface_angle_1: float, surface_angle_2: float) -> float
- Spherical law of sines
  - spherical_law_of_sines_missing_central_angle(surface_angle_corresponding: float, other_central: float, other_surface: float) -> float
  - spherical_law_of_sines_missing_surface_angle(central_angle_corresponding: float, other_central: float, other_surface: float) -> float
- Functions related to Clairaut's Relation (and vertices)
  - get_clairaut_constant_from_heading_and_lat(current_lat: float, current_heading: float) -> float
  - get_sin_of_heading_from_lat_clairaut(current_lat: float, clairaut_constant: float) -> float
  - get_vertex_latitude(lat1: float, azimuth: float) -> float
  - is_latitude_reachable(lat1: float, lat2: float, azimuth: float) -> bool
  - get_both_vertex_latitudes(lat1: float, azimuth: float) -> tuple
  - get_distances_to_both_vertices(lat1: float, azimuth: float) -> tuple
  - get_distances_to_both_vertices_tag_with_latitudes(lat1: float, azimuth: float, verbose: bool=False) -> tuple
- Functions to find a missing latitude value
  - get_lat2_given_point1_lon2_azimuth(lat1: float, lon1: float, lon2: float, azimuth: float, verbose: bool=False) -> float
  - get_lat2_given_point1_lon2_azimuth_atan2_inside_handler(lat1: float, azimuth: float, destination_heading: float, polar_surface_angle: float, verbose: bool=False) -> float
  - get_lat2_given_point1_lon2_azimuth_acos_inside_handler(lat1: float, azimuth: float, destination_heading: float, polar_surface_angle: float, verbose: bool=False) -> float
  - get_lat2_given_point1_lon2_azimuth_atan2(lat1: float, lon1: float, lon2: float, azimuth: float, verbose: bool=False) -> float
  - get_lat2_given_point1_lon2_azimuth_acos(lat1: float, lon1: float, lon2: float, azimuth: float, verbose: bool=False) -> float
  - get_lat2_from_initial_point_azimuth_and_distance_in_nm(lat1: float, azimuth: float, central_angle_polar: float) -> float
- Functions to find a missing longitude value
  - get_lon2_from_point1_lat2_azimuth_and_distance_in_nm(lat1: float, lon1: float, lat2: float, azimuth: float, central_angle_polar: float) -> float
  - get_lons_for_lat_intercepts_from_point1_lat2_azimuth(lat1: float, lon1: float, lat2: float, azimuth: float) -> tuple
  - get_lon2_given_point1_lat2_azimuth_distance_so_far(lat1: float, lon1: float, lat2: float, azimuth: float, distance_so_far: float, verbose: bool=False) -> float
- Functions to find a point based on inputs
  - get_point2_from_point1_azimuth_and_distance(lat1: float, lon1: float, azimuth: float, central_angle_polar: float) -> tuple
  - get_point2_from_point1_azimuth_and_distance_in_nm(lat1: float, lon1: float, azimuth: float, distance: float) -> tuple
- Functions for finding headings
  - get_initial_heading_from_point1_and_point2(lat1: float, lon1: float, lat2: float, lon2: float, verbose: bool=False) -> float
  - get_point2_surface_angle_using_asa_from_point1_lon2_and_azimuth(lat1: float, lon1: float, lon2: float, azimuth: float) -> float
- Functions to find distance angle (polar central angle value)
  - get_distance_between_points_lat1_lat2_azimuth_using_auxiliary_angle_id_two_solutions(lat1: float, lat2: float, azimuth: float) -> tuple
  - get_distance_between_points_lat1_lat2_azimuth_distance_so_far(lat1: float, lat2: float, azimuth: float, distance_so_far: float, verbose: bool=False) -> float
- Functions using unit-vector derivations
  - get_lat3_given_point1_point2_lon3(lat1: float, lon1: float, lat2: float, lon2: float, lon3: float, verbose: bool=False) -> float
- Test suite functions
  - points_test(lat1: float, lon1: float, lat2: float, lon2: float, azimuth: float=None, distance: float=None, error: float=0.0001, prints: bool=True) -> bool
  - oblique_angle_test(test: dict, verbose: bool=True) -> bool



