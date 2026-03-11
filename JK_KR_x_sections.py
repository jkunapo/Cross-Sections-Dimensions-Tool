import arcpy

from GraceGIS_x_sections_functions import get_inputs, create_project_environment, dissolve_stream, \
    create_station_points, create_2D_x_sections, create_slope_raster, create_3D_x_sections, delete_temps,\
    create_3D_x_sections_pts_z_slope_sort_value, create_3D_x_sections_pts_cur_new_centre, add_field_with_a_value, \
    get_pts_high_slopes, welcome_banner, x_sec_level_points, get_lines_poly

# ---------------------------------------------------------------------------------------------------------------------
"""
This tool takes two inputs (a) stream and (b) a dem as inputs.
The tool outputs:
1. Station points at a defined interval.
2. 2D x-sections at defined width.
3. 3D x-sections with elevation and slope, and
4. Levelled bank full width at a slope threshold.
"""
# Welcome banner ------------------------------------------------------------------------------------------------------
welcome_banner()
# ---------------------------------------------------------------------------------------------------------------------
# Prompt and get inputs -----------------------------------------------------------------------------------------------
user_function_id, project_folder, str_path, valid_interval, x_section_half_width, dem_path, slope_at, prj = get_inputs()
# Create project environment-------------------------------------------------------------------------------------------
create_project_environment(project_folder)
# Dissolve input stream -----------------------------------------------------------------------------------------------
str_dis = dissolve_stream(project_folder, str_path)
# ---------------------------------------------------------------------------------------------------------------------
# Function 1 - Station points at a defined interval.
# --------------------------------------------------------------------------------------------------------------------
if user_function_id in ('1', '2', '3', '4'):
    station_pts = f'{project_folder}\\x_sec_outputs.gdb\\station_points_{str(valid_interval)}m'
    create_station_points(str_dis, x_section_half_width, valid_interval, station_pts)
# ---------------------------------------------------------------------------------------------------------------------
# Function 2 - 2D x-sections at defined width.
# --------------------------------------------------------------------------------------------------------------------
if user_function_id in ('2', '3', '4'):
    x_sec2d = f'{project_folder}\\x_sec_outputs.gdb\\x_sec_i{valid_interval}_w{x_section_half_width}'
    create_2D_x_sections(project_folder, x_section_half_width, str_dis, station_pts, prj, x_sec2d)
# ---------------------------------------------------------------------------------------------------------------------
# Function 3 - Develop 3D x-sections, points, current centre, new centre and attach slope values
# --------------------------------------------------------------------------------------------------------------------
if user_function_id in ('3', '4'):
    # Create Slope Raster in degrees ---------------------------------------------------------------------------------
    slope_deg = f'{project_folder}\\x_sec_outputs.gdb\\slope_deg'
    create_slope_raster(dem_path, slope_deg)

    # 3D x-sections  -------------------------------------------------------------------------------------------------
    x_sec3d = x_sec2d + "_3D"
    create_3D_x_sections(x_sec2d, dem_path, x_sec3d)

    # 3D x-sections points and  point_z, slope_deg, sort_value -------------------------------------------------------
    x_sec3d_pts = x_sec3d + "_pts"
    create_3D_x_sections_pts_z_slope_sort_value(project_folder, x_sec3d, x_sec3d_pts, slope_deg)

    # 3D x-sections points  - current centre, new centre -----------------------------------------------------------
    x_sec3d_pts_v2 = x_sec3d_pts + "_v2"
    create_3D_x_sections_pts_cur_new_centre(project_folder, station_pts, x_sec2d, x_sec3d_pts, x_sec3d_pts_v2)

# ---------------------------------------------------------------------------------------------------------------------
# Function 4 - Levelled bank full width at a slope threshold.
# --------------------------------------------------------------------------------------------------------------------
if user_function_id == '4':

    print(f'Developing Levelled 3D x-sections and points..')
    x_sec3d_pts_v3 = x_sec3d_pts + "_v3"
    if not arcpy.Exists(x_sec3d_pts_v3):
        arcpy.Select_analysis(in_features=x_sec3d_pts_v2, out_feature_class=x_sec3d_pts_v3, where_clause="")
        arcpy.DeleteField_management(in_table=x_sec3d_pts_v3, drop_field="MIN_Sort_Value;MAX_Sort_Value;MAX_NewCentre")
    else:
        print(f'Already Exists: {x_sec3d_pts_v3}')

    # --------------------------------------------
    # Step 1: Get high slope points
    # --------------------------------------------
    pts_at_slope = f'{project_folder}\\x_sec_outputs.gdb\\pts_at_slope_{slope_at}'
    delete_temps([pts_at_slope])
    print(f'Processing: Points with high slopes..')
    add_field_with_a_value(x_sec3d_pts_v3, "slope_at", "LONG", slope_at)
    get_pts_high_slopes(project_folder, x_sec3d_pts_v3, pts_at_slope)
    print(f'Done: Points with high slopes..{pts_at_slope}')

    # --------------------------------------------
    # Step 2: Levelling points
    # --------------------------------------------
    print(f'Processing: Levelling points (Takes time. Watch console.)')
    x_sec3d_levelled_pts = f'{x_sec3d}_s{slope_at}_levelled_pts'
    x_sec3d_levelled_pts_corrected = f'{x_sec3d}_s{slope_at}_levelled_pts_corrected'
    delete_temps([x_sec3d_levelled_pts, x_sec3d_levelled_pts_corrected])
    x_sec_level_points(project_folder, x_sec3d_pts_v3, pts_at_slope, x_sec3d_levelled_pts,
                       x_sec3d_levelled_pts_corrected)
    print(f'Done: Levelled points.')

    x_sec3d_levelled_lines = f'{x_sec3d}_s{slope_at}_levelled_lines'
    x_sec3d_levelled_bfw_poly = f'{x_sec3d}_s{slope_at}_levelled_poly'
    x_sec3d_levelled_lines_corrected = f'{x_sec3d}_s{slope_at}_levelled_lines_corrected'
    x_sec3d_levelled_bfw_poly_corrected = f'{x_sec3d}_s{slope_at}_levelled_poly_corrected'

    get_lines_poly(project_folder, x_sec3d_levelled_pts, x_sec3d_levelled_lines, x_sec3d_levelled_bfw_poly)
    get_lines_poly(project_folder, x_sec3d_levelled_pts_corrected, x_sec3d_levelled_lines_corrected,
                   x_sec3d_levelled_bfw_poly_corrected)
    print(f'Completed all the processes.')

# ---------------------------------------------------------------------------------------------------------------------
# Closing
# --------------------------------------------------------------------------------------------------------------------
delete_temps([f'{project_folder}\\temp.gdb'])
exit()
