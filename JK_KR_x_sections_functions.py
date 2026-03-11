import os
import arcpy
import numpy as np
from sklearn.linear_model import LinearRegression


# Projections
GDA_1994_MGA_Zone_55 = "PROJCS['GDA_1994_MGA_Zone_55'," \
               "GEOGCS['GCS_GDA_1994',DATUM['D_GDA_1994',SPHEROID['GRS_1980',6378137.0,298.257222101]]," \
               "PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator']," \
               "PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',10000000.0]," \
               "PARAMETER['Central_Meridian',147.0],PARAMETER['Scale_Factor',0.9996]," \
               "PARAMETER['Latitude_Of_Origin',0.0]," \
               "UNIT['Meter',1.0]];-5120900 1900 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"

GDA2020_MGA_Zone_55 = "PROJCS['GDA2020_MGA_Zone_55',GEOGCS['GDA2020',DATUM['GDA2020',SPHEROID['GRS_1980'," \
           "6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]," \
           "PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing'," \
           "10000000.0],PARAMETER['Central_Meridian',147.0],PARAMETER['Scale_Factor',0.9996]," \
           "PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]],VERTCS['AHD',VDATUM['Australian_Height_Datum']," \
           "PARAMETER['Vertical_Shift',0.0],PARAMETER['Direction',1.0],UNIT['Meter',1.0]]"

# *********************************************************************************************************************
# Functions: To get inputs
# *********************************************************************************************************************


def get_valid_function_id(prompt):
    """
    Prompts the user for input and validates it to be either 1, 2, 3, or 4.

    Args:
        prompt (str): The prompt message to display.

    Returns:
        str: The validated FunctionID ('1', '2', '3', or '4').
    """
    while True:
        user_input = input(prompt)
        if user_input in ('1', '2', '3', '4'):
            return user_input
        else:
            print("Invalid input. Please enter either '1', '2', '3', or '4'.")


def get_valid_interval():
    """
    Prompts the user to enter a station points interval in meters and validates it to be between 5 and 1000.
    If no input is provided, the default value of 25 is used.

    Returns:
        int: A valid station points interval.
    """
    while True:
        try:
            user_input = input("Enter the station points interval (between 5 and 1000 meters, or press Enter for default 25): ")
            if not user_input:
                return 25  # Default value
            interval = int(user_input)
            if 5 <= interval <= 1000:
                return interval
            else:
                print("Interval must be between 5 and 1000 meters.")
        except ValueError:
            print("Invalid input. Please enter an integer value.")


def get_valid_x_section_width():
    """
    Prompts the user to enter an X-Section full width in meters and validates it to be between 20 and 100,
    divisible by 10. If no input is provided, the default value of 60 is used.

    Returns:
        int: A valid X-Section full width (half of the value).
    """
    while True:
        try:
            user_input = input("Enter x-section width (between 20 and 100 m, divisible by 10, "
                               "or press Enter for default 60): ")
            if not user_input:
                return 30  # Default value (half of 60)
            x_section_width = int(user_input)
            if 20 <= x_section_width <= 100 and x_section_width % 10 == 0:
                return x_section_width // 2
            else:
                print("Width must be between 20 and 100 meters and divisible by 10.")
        except ValueError:
            print("Invalid input. Please enter an integer value.")


def get_valid_slope_threshold():
    """
    Prompts the user to enter a slope threshold in degrees and validates it to be between 5 and 15.
    If no input is provided, the default value of 7 is used.

    Returns:
        int: A valid slope threshold.
    """
    while True:
        try:
            user_input = input("Enter the slope threshold (between 5 and 15 degrees, or press Enter for default 7): ")
            if not user_input:
                return 7  # Default value
            slope = int(user_input)
            if 5 <= slope <= 15:
                return slope
            else:
                print("Slope must be between 5 and 15 degrees.")
        except ValueError:
            print("Invalid input. Please enter an integer value.")


def get_valid_directory_path(prompt="Enter a directory path: "):
    """
    Prompts the user to enter a directory path and validates its existence.
    If the path does not exist, prompts the user again.

    Returns:
        str: A valid directory path.
    """
    while True:
        user_path = input(prompt)
        if os.path.exists(user_path) and os.path.isdir(user_path):
            return user_path
        else:
            print(f"Error: The path '{user_path}' does not exist or is not a valid directory. Please try again.")


def get_valid_spatialdata_path(prompt="Enter a spatial path: "):
    """
    Prompts the user to enter the path and validates its existence.
    If the path does not exist, prompts the user again.

    Returns:
        str: A valid spatial path.
    """
    while True:
        user_path = input(prompt)
        if arcpy.Exists(user_path):
            return user_path
        else:
            print(f"Error: The path '{user_path}' does not exist or is not a valid directory. Please try again.")


def get_projection_input(prompt):
    """
    Prompts the user for input and validates it to be either 1 or 2.

    Args:
        prompt (str): The prompt message to display.

    Returns:
        str: Either '1' or '2'.
    """
    while True:
        user_input = input(prompt)
        if user_input == '1' or user_input == '2':
            return user_input
        else:
            print("Invalid input. Please enter either '1' or '2'.")


def get_inputs():

    user_function_id = get_valid_function_id("Enter a Function ID (1, 2, 3, or 4): ")

    project_folder = get_valid_directory_path("Enter Project Folder: ")

    str_path = get_valid_spatialdata_path("Input Stream: ")

    valid_interval = get_valid_interval()
    print(f"Station points interval: {valid_interval} meters")

    x_section_half_width = get_valid_x_section_width()
    print(f"x-section half width: {x_section_half_width} meters")

    dem_path = None
    slope_at = None
    if user_function_id == '3':
        dem_path = get_valid_spatialdata_path("Input 1m DEM: ")
        print(f"DEM : {dem_path}")
    elif user_function_id == '4':
        dem_path = get_valid_spatialdata_path("Input 1m DEM: ")
        print(f"DEM : {dem_path}")
        # Get a valid slope threshold from the user
        slope_at = get_valid_slope_threshold()
        print(f"slope threshold as: {slope_at} degrees")

    user_choice = get_projection_input("Projection: Enter '1' for GDA2020_MGA_Zone_55 or '2' for GDA_1994_MGA_Zone_55: ")
    # Set prj based on user's choice
    prj = None
    if user_choice == '1':
        prj = GDA2020_MGA_Zone_55
    else:
        prj = GDA_1994_MGA_Zone_55
    print(f"Selected Projection: {user_choice}")

    return user_function_id, project_folder, str_path, valid_interval, x_section_half_width, dem_path, slope_at, prj


def create_project_environment(proj_folder):

    delete_temps([f"{proj_folder}\\temp.gdb"])
    arcpy.CreateFileGDB_management(proj_folder, "temp.gdb")

    if not arcpy.Exists(f"{proj_folder}\\x_sec_outputs.gdb"):
        arcpy.CreateFileGDB_management(proj_folder, "x_sec_outputs.gdb")


# *********************************************************************************************************************
# Functions: Stations Points
# *********************************************************************************************************************


def dissolve_stream(project_folder, str_path):
    add_field_with_a_value(str_path, "ggis_id", "SHORT", 1)

    str_dis_temp = f"{project_folder}\\temp.gdb\\str_dis_temp"
    str_dis = f"{project_folder}\\x_sec_outputs.gdb\\stream_dissolved"
    delete_temps([str_dis_temp])

    if not arcpy.Exists(str_dis):
        print(f"Dissolving streams...")
        arcpy.Dissolve_management(in_features=str_path, out_feature_class=str_dis_temp, dissolve_field="ggis_id",
                                  statistics_fields="", multi_part="SINGLE_PART", unsplit_lines="DISSOLVE_LINES")
        arcpy.Select_analysis(in_features=str_dis_temp,
                              out_feature_class=str_dis, where_clause="Shape_Length > 100")
        delete_temps([str_dis_temp])
        add_field_with_a_value(str_dis, "seg_id", "LONG", '!OBJECTID!')
    else:
        print(f'Using existing: {str_dis}..')

    return str_dis


def create_station_points(str_dis, x_section_half_width, valid_interval, station_pts):

    width_plus_1 = int(x_section_half_width) + 1
    buffers_list = range(10, width_plus_1, 2)
    station_points_sort_value = len(buffers_list) + 1
    station_distance = f'{str(valid_interval)} Meters'

    if not arcpy.Exists(station_pts):
        print(f'Processing: Station Points..')
        station_points(str_dis, station_pts, station_distance, station_points_sort_value)
        print(f'DONE: Station Points : {station_pts}')
    else:
        print(f'Using existing station Points.. {station_pts}..')


def station_points(mwstr_dis, station_points, station_dist, station_points_sort_value):
    temp_list = [station_points]
    delete_temps(temp_list)
    # ---Develop station_points_25m-----------------------------------------------------------------------------------
    arcpy.GeneratePointsAlongLines_management(mwstr_dis, station_points, "DISTANCE", station_dist, "", "")
    add_field_with_a_value(station_points, "x_sec_id", "LONG", '!OBJECTID!')
    add_field_with_a_value(station_points, "SortField", "SHORT", station_points_sort_value)


# *********************************************************************************************************************
# Functions: 2D cross sections
# *********************************************************************************************************************


def create_2D_x_sections(project_folder, x_section_half_width, str_dis, station_pts, prj, x_sec2d):

    width_plus_1 = int(x_section_half_width) + 1
    buffers_list = range(10, width_plus_1, 2)
    station_points_sort_value = len(buffers_list) + 1

    if not arcpy.Exists(x_sec2d):
        print(f'Processing: 2D x-sections..(Takes time)')
        # --------------------------------------------
        # For each seg_id in str_dis
        # --------------------------------------------
        merge_string = ""
        cursor = arcpy.SearchCursor(str_dis, ['seg_id'])
        for row in cursor:
            seg_id = row.getValue("seg_id")

            seg_line = f'{project_folder}\\temp.gdb\\seg_line_{str(seg_id)}'
            stn_pts_seg = f'{project_folder}\\temp.gdb\\stn_pts_{str(seg_id)}'
            x_sec2d_seg = f'{project_folder}\\temp.gdb\\x_sec2d_{str(seg_id)}'

            statement = f'seg_id = {seg_id}'
            arcpy.Select_analysis(str_dis, seg_line, statement)
            arcpy.Select_analysis(station_pts, stn_pts_seg, statement)
            # --------------------------------------------
            # Call function to process 2D x-sections..for a segment
            # --------------------------------------------
            print(f'Processing: 2D x-sections..for segment {seg_id}')
            x_sec_2D(project_folder, seg_line, stn_pts_seg, station_points_sort_value, buffers_list, x_sec2d_seg, prj)
            delete_temps([seg_line])

            add_field_with_a_value(x_sec2d_seg, "seg_id", "LONG", seg_id)
            merge_string += ";" + x_sec2d_seg
        # --------------------------------------------
        # Merge all segment-wise cross sections into one.
        # --------------------------------------------
        merge_string = merge_string[1:]
        arcpy.Merge_management(merge_string, x_sec2d, "")

        delete_temps(merge_string.split(";"))
        print(f'Done: 2D x_sec: {x_sec2d}')
    else:
        print(f'Already exists: {x_sec2d}')


def x_sec_2D(project_folder, segline, station_points, station_points_sort_value, buffers_list, out_transacts, prj):
    # Temp Datasets
    stn_pts = f"{project_folder}\\temp.gdb\\stn_pts"
    delete_temps([out_transacts, stn_pts])

    # ---------------------------------------------------------------------------------------------------------------
    # ---Run a for loop for each item in buffers list ----------------------------------------------------------------
    merge_string = ""
    station_points_25m_l = station_points
    station_points_25m_r = station_points
    i = 0

    for item in buffers_list:
        distance = str(item) + " Meters"
        distance_to_erase = str((item - 0.5)) + " Meters"

        # Buffer erase, left and right
        buf_erase = f"{project_folder}\\temp.gdb\\buf_erase"
        buf_l = f"{project_folder}\\temp.gdb\\buf_l"
        buf_r = f"{project_folder}\\temp.gdb\\buf_r"

        arcpy.Buffer_analysis(segline, buf_erase, distance_to_erase, "FULL", "ROUND", "ALL", "", "PLANAR")
        arcpy.Buffer_analysis(segline, buf_l, distance, "LEFT", "FLAT", "ALL", "", "PLANAR")
        arcpy.Buffer_analysis(segline, buf_r, distance, "RIGHT", "FLAT", "ALL", "", "PLANAR")

        # Develop left and right lines by erasing middle erase buffer
        buf_l_line = f"{project_folder}\\temp.gdb\\buf_l_line"
        buf_r_line = f"{project_folder}\\temp.gdb\\buf_r_line"
        l_line = f"{project_folder}\\temp.gdb\\l_line"
        r_line = f"{project_folder}\\temp.gdb\\r_line"

        arcpy.PolygonToLine_management(buf_l, buf_l_line, "IDENTIFY_NEIGHBORS")
        arcpy.Erase_analysis(buf_l_line, buf_erase, l_line, "")
        arcpy.PolygonToLine_management(buf_r, buf_r_line, "IDENTIFY_NEIGHBORS")
        arcpy.Erase_analysis(buf_r_line, buf_erase, r_line, "")

        # Process: Left -----------------------------------------------------------------------------------------------
        arcpy.Select_analysis(station_points_25m_l, stn_pts, "")
        arcpy.Near_analysis(stn_pts, l_line, "", "LOCATION", "NO_ANGLE", "PLANAR")
        # arcpy.MakeXYEventLayer_management(stn_pts, "NEAR_X", "NEAR_Y", "stn_pts_layer", proj_def, "")

        pts_l_item = f'{project_folder}\\temp.gdb\\pts_l_{str(item)}'

        arcpy.management.XYTableToPoint(stn_pts, pts_l_item, "NEAR_X", "NEAR_Y", None, prj)

        # arcpy.Select_analysis("stn_pts_layer", pts_l_item, "")
        arcpy.DeleteField_management(in_table=pts_l_item, drop_field="ORIG_FID;NEAR_FID;NEAR_DIST;NEAR_X;NEAR_Y")

        sort_value_l = len(buffers_list) - i

        arcpy.CalculateField_management(pts_l_item, "SortField", sort_value_l)

        station_points_25m_l = pts_l_item

        # delete outputs if the already exist.
        delete_temps([buf_l, buf_l_line, "stn_pts_layer", stn_pts, l_line])

        # Process: Right ----------------------------------------------------------------------------------------------
        arcpy.Select_analysis(station_points_25m_r, stn_pts, "")
        arcpy.Near_analysis(stn_pts, r_line, "", "LOCATION", "NO_ANGLE", "PLANAR")
        arcpy.MakeXYEventLayer_management(stn_pts, "NEAR_X", "NEAR_Y", "stn_pts_layer", prj, "")

        pts_r_item = f'{project_folder}\\temp.gdb\\pts_r_{str(item)}'

        arcpy.management.XYTableToPoint(stn_pts, pts_r_item, "NEAR_X", "NEAR_Y", None, prj)

        # arcpy.Select_analysis("stn_pts_layer", pts_r_item, "")
        arcpy.DeleteField_management(in_table=pts_r_item, drop_field="ORIG_FID;NEAR_FID;NEAR_DIST;NEAR_X;NEAR_Y")

        sort_value_r = station_points_sort_value + 1 + i

        arcpy.CalculateField_management(pts_r_item, "SortField", sort_value_r)

        station_points_25m_r = pts_r_item

        # delete outputs if the already exist.
        delete_temps([buf_r, buf_r_line, buf_erase, "stn_pts_layer", stn_pts, r_line])

        i += 1

        # Construct a merge string
        merge_string += ";" + pts_l_item + ";" + pts_r_item
        print("Processed: " + pts_l_item + " and " + pts_r_item)

    # Merge files-----------------------------------------------------------------------------------------------------
    pts_all = f"{project_folder}\\temp.gdb\\pts_all"

    merge_string = merge_string[1:] + ";" + station_points
    arcpy.Merge_management(merge_string, pts_all, "")
    print("Processed: Merged points " + pts_all)

    # Process: Points To Transacts -----------------------------------------------------------------------------------
    arcpy.PointsToLine_management(pts_all, out_transacts, "x_sec_id", "SortField", "NO_CLOSE")

    # Delete buffer files
    delete_temps(merge_string.split(";"))
    delete_temps([pts_all])

    print("2D Cross section process completed.")


# *********************************************************************************************************************
# Functions: 3D cross sections
# *********************************************************************************************************************

def welcome_banner():
    print(f"")
    print(
        f"***********************************************************************************************************")
    print(f"")
    print(
        f"                                                   Welcome                                                 ")
    print(f"")
    print(
        f"                                     Cross Sections & Dimensions 2.0                                       ")
    print(f"")
    print(
        f"                                     Developed by: Dr Joshphar Kunapo                                      ")
    print(f"")
    print(f"List of functions: ")
    print(f"    1. Station points at a defined interval.")
    print(f"    2. 2D x-sections at defined width.")
    print(f"    3. 3D x-sections with elevation and slope, and")
    print(f"    4. Levelled bank full width at a slope threshold.")
    print(f"")
    print(
        f"***********************************************************************************************************")
    print(f"")


def create_slope_raster(dem_path, slope_deg):
    if not arcpy.Exists(slope_deg):
        print(f'Processing: Slope in degrees..')
        arcpy.gp.Slope_sa(dem_path, slope_deg, "DEGREE", "1")
        print(f'Done: Slope in degrees.')
    else:
        print(f'Already exists: {slope_deg}..')


def create_3D_x_sections(x_sec2d, dem_path, x_sec3d):
    if not arcpy.Exists(x_sec3d):
        print(f'Processing: 3D x-sections..')
        arcpy.InterpolateShape_3d(in_surface=dem_path, in_feature_class=x_sec2d, out_feature_class=x_sec3d,
                                  sample_distance="1", z_factor="1", method="BILINEAR",
                                  vertices_only="DENSIFY", pyramid_level_resolution="0")
    else:
        print(f'Already exists: {x_sec3d}..')


def create_3D_x_sections_pts_z_slope_sort_value(project_folder, x_sec3d, x_sec3d_pts, slope_deg):
    if not arcpy.Exists(x_sec3d_pts):
        arcpy.FeatureVerticesToPoints_management(in_features=x_sec3d, out_feature_class=x_sec3d_pts,
                                                 point_location="ALL")
        arcpy.AddGeometryAttributes_management(Input_Features=x_sec3d_pts, Geometry_Properties="POINT_X_Y_Z_M",
                                               Length_Unit="", Area_Unit="", Coordinate_System="")
        get_raster_value_for_points(project_folder, x_sec3d_pts, dem=slope_deg, elev_field="slope_deg")

        id_min = f'{project_folder}\\temp.gdb\\id_min'
        delete_temps([id_min])

        print(f'Add field for sorting and get sorted values for each transact.')
        arcpy.AddField_management(in_table=x_sec3d_pts, field_name="UNQID", field_type="LONG")
        arcpy.CalculateField_management(x_sec3d_pts, "UNQID", "!OBJECTID!", "PYTHON_9.3", "")
        arcpy.Statistics_analysis(x_sec3d_pts, id_min, "UNQID MIN", "x_sec_id")
        arcpy.CalculateField_management(in_table=id_min, field="MIN_UNQID", expression="!MIN_UNQID! - 1",
                                        expression_type="PYTHON_9.3", code_block="")
        # make a copy and join and make it original again
        x_sec3d_pts_temp = f'{project_folder}\\temp.gdb\\x_sec3d_pts_temp'
        delete_temps([x_sec3d_pts_temp])
        arcpy.Select_analysis(in_features=x_sec3d_pts, out_feature_class=x_sec3d_pts_temp, where_clause="")
        delete_temps([x_sec3d_pts])
        arcpy.DeleteField_management(in_table=x_sec3d_pts_temp, drop_field="MIN_UNQID")
        arcpy.JoinField_management(in_data=x_sec3d_pts_temp, in_field="x_sec_id", join_table=id_min,
                                   join_field="x_sec_id", fields="MIN_UNQID")
        # rename it back to normal
        arcpy.Select_analysis(in_features=x_sec3d_pts_temp, out_feature_class=x_sec3d_pts, where_clause="")

        arcpy.AddField_management(in_table=x_sec3d_pts, field_name="Sort_Value", field_type="LONG")
        arcpy.CalculateField_management(in_table=x_sec3d_pts, field="Sort_Value",
                                        expression="!OBJECTID! - !MIN_UNQID!", expression_type="PYTHON_9.3",
                                        code_block="")
        arcpy.DeleteField_management(in_table=x_sec3d_pts, drop_field="ORIG_FID;MIN_UNQID")
        delete_temps([id_min])
    else:
        print(f'Already exists: {x_sec3d_pts}..')


def create_3D_x_sections_pts_cur_new_centre(project_folder, station_pts, x_sec2d, x_sec3d_pts, x_sec3d_pts_v2):
    if not arcpy.Exists(x_sec3d_pts_v2):
        arcpy.Select_analysis(in_features=x_sec3d_pts, out_feature_class=x_sec3d_pts_v2, where_clause="")
        print(f'Processing: Current and new centres (Takes time.)')
        x_sec_current_new_centre(project_folder, x_sec3d_pts_v2, x_sec2d, station_pts)
        print(f'Done: Current and new centres.')
    else:
        print(f'Already Exists: {x_sec3d_pts_v2}')


def x_sec_current_new_centre(project_folder, x_sec3d_pts, x_sec2d, stn_pts):

    # due to lines intersect this needs to be done for each cross section
    # loop through each x_sec_id to get new_centre ------------------------------------------------------------

    # Add fields CurCentre and NewCentre
    add_field_with_a_value(x_sec3d_pts, "CurCentre", "SHORT", "None")
    add_field_with_a_value(x_sec3d_pts, "NewCentre", "SHORT", 'None')

    # MakeFeatureLayer and delete at the end
    arcpy.MakeFeatureLayer_management(in_features=x_sec3d_pts, out_layer="x_sec3d_pts_lyr")

    # Use x_sec2d to loop through for each x_sec_id - cursor1
    # ----------------------------------------------------
    cursor1 = arcpy.SearchCursor(x_sec2d, ['x_sec_id'])
    for cursor1_row in cursor1:
        x_sec_id = cursor1_row.getValue("x_sec_id")
        # x_sec_id = 1706

        stn_pts_sel = f'{project_folder}\\temp.gdb\\stn_pts_sel'
        arcpy.Select_analysis(stn_pts, stn_pts_sel, f'x_sec_id = {x_sec_id}')

        # Getting current centre using select by location stn_pts_sel
        # -----------------------------------------------------------------
        print(f'Getting current centre for x_sec_id = {x_sec_id}')

        arcpy.SelectLayerByAttribute_management(in_layer_or_view="x_sec3d_pts_lyr",
                                                selection_type="NEW_SELECTION",
                                                where_clause=f'x_sec_id = {x_sec_id}')
        arcpy.SelectLayerByLocation_management(in_layer="x_sec3d_pts_lyr", overlap_type="INTERSECT",
                                               select_features=stn_pts_sel, search_distance="0.2 Meters",
                                               selection_type="SUBSET_SELECTION",
                                               invert_spatial_relationship="NOT_INVERT")
        arcpy.CalculateField_management("x_sec3d_pts_lyr", "CurCentre", '!Sort_Value!', "PYTHON_9.3", "")
        arcpy.SelectLayerByAttribute_management("x_sec3d_pts_lyr", "CLEAR_SELECTION")

        # Getting new centre
        # -------------------------------------------------------------------------
        # 1. Select x_sec3d_pts within 5 meters of stn_pts_sel of this x_sec_id and
        # get their POINT_Z MIN as min_z
        # -------------------------------------------------------------------------------
        print(f'Getting new centre for x_sec_id = {x_sec_id}')
        arcpy.SelectLayerByAttribute_management(in_layer_or_view="x_sec3d_pts_lyr",
                                                selection_type="NEW_SELECTION",
                                                where_clause=f'x_sec_id = {x_sec_id}')
        arcpy.SelectLayerByLocation_management(in_layer="x_sec3d_pts_lyr", overlap_type="INTERSECT",
                                               select_features=stn_pts_sel, search_distance="5 Meters",
                                               selection_type="SUBSET_SELECTION",
                                               invert_spatial_relationship="NOT_INVERT")
        x_sec3d_pts_sel = f'{project_folder}\\temp.gdb\\x_sec3d_pts_sel'
        arcpy.Select_analysis("x_sec3d_pts_lyr", x_sec3d_pts_sel, "")
        arcpy.SelectLayerByAttribute_management("x_sec3d_pts_lyr", "CLEAR_SELECTION")
        # MakeFeatureLayer and delete at the end
        arcpy.MakeFeatureLayer_management(in_features=x_sec3d_pts_sel, out_layer="x_sec3d_pts_sel_lyr")

        tbl_x_sec_min_z = f'{project_folder}\\temp.gdb\\tbl_x_sec_min_z'
        arcpy.Statistics_analysis(in_table=x_sec3d_pts_sel, out_table=tbl_x_sec_min_z,
                                  statistics_fields="POINT_Z MIN", case_field="x_sec_id")

        cursor2 = arcpy.SearchCursor(tbl_x_sec_min_z, ['MIN_POINT_Z'])
        for cursor2_row in cursor2:
            min_z = cursor2_row.getValue("MIN_POINT_Z") + 0.01
            # -------------------------------------------------------------------------
            # 2. Select records where POINT_Z <= min_z
            # --------------------------------------------------------------------------
            statement1 = f'x_sec_id = {x_sec_id} AND POINT_Z <= {min_z}'
            print(statement1)
            arcpy.SelectLayerByAttribute_management(in_layer_or_view="x_sec3d_pts_sel_lyr",
                                                    selection_type="NEW_SELECTION",
                                                    where_clause=statement1)
            # -------------------------------------------------------------------------
            # 3. There will be more than on record where POINT_Z <= round({min_z}, 4
            # Collect them and get their min and max sort_values for this x_sec_id.
            # --------------------------------------------------------------------------
            tbl_x_sec_sort_min_max = f'{project_folder}\\temp.gdb\\tbl_x_sec_sort_min_max'
            arcpy.Statistics_analysis(in_table="x_sec3d_pts_sel_lyr", out_table=tbl_x_sec_sort_min_max,
                                      statistics_fields="Sort_Value MIN;Sort_Value MAX", case_field="x_sec_id")
            arcpy.SelectLayerByAttribute_management(in_layer_or_view="x_sec3d_pts_sel_lyr",
                                                    selection_type="CLEAR_SELECTION", where_clause="")
            delete_temps([x_sec3d_pts_sel, "x_sec3d_pts_sel_lyr"])
            # -------------------------------------------------------------------------
            # 4. Get new value using below logic and set the new centre
            # --------------------------------------------------------------------------
            cursor3 = arcpy.SearchCursor(tbl_x_sec_sort_min_max, ['FREQUENCY', 'MIN_Sort_Value', 'MAX_Sort_Value'])
            for cursor3_row in cursor3:
                if cursor3_row.getValue("FREQUENCY") in (1, 2):
                    value_new = int(cursor3_row.getValue("MIN_Sort_Value"))
                else:
                    value_new = int(cursor3_row.getValue("MIN_Sort_Value") + (cursor3_row.getValue("FREQUENCY") // 2))

                statement2 = f'x_sec_id = {x_sec_id} AND Sort_Value = {value_new}'

                arcpy.SelectLayerByAttribute_management(in_layer_or_view="x_sec3d_pts_lyr",
                                                        selection_type="NEW_SELECTION", where_clause=statement2)
                arcpy.CalculateField_management(in_table="x_sec3d_pts_lyr", field="NewCentre",
                                                expression=value_new, expression_type="PYTHON", code_block="")
                arcpy.SelectLayerByAttribute_management(in_layer_or_view="x_sec3d_pts_lyr",
                                                        selection_type="CLEAR_SELECTION", where_clause="")
                print(f'x_sec_id = {x_sec_id} AND New Centre at = {value_new}')
            # exit()
            # Delete 3rd level temps
            delete_temps([tbl_x_sec_sort_min_max])
        # Delete 2nd level temps
        delete_temps([stn_pts_sel, tbl_x_sec_min_z, x_sec3d_pts_sel])
    # Delete 1st level temps
    delete_temps(["x_sec3d_pts_lyr"])


def get_lists_for_sv_and_z_for_xsec_id(x_sec_id, expression, side, var_pts_high_slopes):

    pts_high_slopes_for_a_x_sec = var_pts_high_slopes + str(x_sec_id)
    delete_temps([pts_high_slopes_for_a_x_sec])
    arcpy.Select_analysis(in_features=var_pts_high_slopes, out_feature_class=pts_high_slopes_for_a_x_sec,
                          where_clause=expression)
    list_sort_values = []
    list_POINT_Z = []
    if side in ("right", None):
        cursor = arcpy.da.SearchCursor(pts_high_slopes_for_a_x_sec, ['Sort_Value', 'POINT_Z'],
                                       sql_clause=(None, 'ORDER BY Sort_Value'))
    elif side == "left":
        cursor = arcpy.da.SearchCursor(pts_high_slopes_for_a_x_sec, ['Sort_Value', 'POINT_Z'],
                                       sql_clause=(None, 'ORDER BY Sort_Value DESC'))
    for row in cursor:
        list_sort_values.append(row[0])
        list_POINT_Z.append(row[1])

    delete_temps([pts_high_slopes_for_a_x_sec])
    return list_sort_values, list_POINT_Z


# *********************************************************************************************************************
# Functions: Levelling
# *********************************************************************************************************************


def get_pts_high_slopes(project_folder, x_sec3d_pts, var_pts_high_slopes):
    """
    1. get pts_high_slopes1 where (slope_deg >= slope_at) OR  (NewCentre is not NULL) OR (CurCentre is not NULL)
    2. get min and max sort values for pts_high_slopes1 and join them to x_sec3d_pts
    3.Select pts_high_slopes from x_sec3d_pts using (slope_deg >= slope_at) OR (NewCentre is not NULL) OR
    (CurCentre is not NULL) OR (Sort_Value = MIN_Sort_Value - 1) OR (Sort_Value = MAX_Sort_Value + 1)
    """
    # 1. get pts_high_slopes1 where (slope_deg >= slope_at) OR  (NewCentre is not NULL) OR (CurCentre is not NULL)
    # -------------------------------------------------------------------------------------------------------------
    pts_high_slopes1 = f'{project_folder}\\temp.gdb\\pts_high_slopes1'
    delete_temps([pts_high_slopes1])
    select_statement1 = "(slope_deg >= slope_at) OR (NewCentre is not NULL) OR (CurCentre is not NULL)"
    arcpy.Select_analysis(in_features=x_sec3d_pts, out_feature_class=pts_high_slopes1,
                          where_clause=select_statement1)

    # 2. get min and max sort values for pts_high_slopes1 and join them to x_sec3d_pts
    # -------------------------------------------------------------------------------------------------------------
    tbl_x_id_sort_start_ends = f'{project_folder}\\temp.gdb\\tbl_x_id_sort_start_ends'
    delete_temps([tbl_x_id_sort_start_ends])

    arcpy.Statistics_analysis(in_table=pts_high_slopes1, out_table=tbl_x_id_sort_start_ends,
                              statistics_fields="Sort_Value MIN;Sort_Value MAX", case_field="x_sec_id")
    arcpy.DeleteField_management(in_table=x_sec3d_pts, drop_field="MIN_Sort_Value;MAX_Sort_Value")
    arcpy.JoinField_management(in_data=x_sec3d_pts, in_field="x_sec_id",
                               join_table=tbl_x_id_sort_start_ends, join_field="x_sec_id",
                               fields="MIN_Sort_Value;MAX_Sort_Value")

    # 3.Select pts_high_slopes from x_sec3d_pts using (slope_deg >= slope_at) OR (NewCentre is not NULL) OR
    # (CurCentre is not NULL) OR (Sort_Value = MIN_Sort_Value - 1) OR (Sort_Value = MAX_Sort_Value + 1)"
    # -------------------------------------------------------------------------------------------------------------
    select_statement = "(slope_deg >= slope_at) OR (NewCentre is not NULL) OR (CurCentre is not NULL) OR " \
                       "(Sort_Value = MIN_Sort_Value - 1) OR (Sort_Value = MAX_Sort_Value + 1)"
    arcpy.Select_analysis(in_features=x_sec3d_pts, out_feature_class=var_pts_high_slopes, where_clause=select_statement)

    arcpy.DeleteField_management(in_table=x_sec3d_pts, drop_field="MIN_Sort_Value;MAX_Sort_Value")
    arcpy.DeleteField_management(in_table=var_pts_high_slopes, drop_field="MIN_Sort_Value;MAX_Sort_Value")

    delete_temps([pts_high_slopes1, tbl_x_id_sort_start_ends])


def x_sec_level_points(var_project_folder, var_x_sec3d_pts_v3, var_pts_at_slope, var_x_sec3d_levelled_pts,
                       var_x_sec3d_levelled_pts_corrected):
    # -----------------------------------------------------------------------------------------------
    # Step 1 - Using pts_high_slopes, get and join MIN_Sort_Value;MAX_Sort_Value;MAX_NewCentre
    # -----------------------------------------------------------------------------------------------
    arcpy.DeleteField_management(in_table=var_pts_at_slope, drop_field="MIN_Sort_Value;MAX_Sort_Value; MAX_NewCentre")
    tbl_x_id_new_centre_sort_start_ends = f'{var_project_folder}\\temp.gdb\\tbl_x_id_new_centre_sort_start_ends'
    delete_temps([tbl_x_id_new_centre_sort_start_ends])

    arcpy.Statistics_analysis(in_table=var_pts_at_slope, out_table=tbl_x_id_new_centre_sort_start_ends,
                              statistics_fields="Sort_Value MIN;Sort_Value MAX;NewCentre MAX", case_field="x_sec_id")
    arcpy.JoinField_management(in_data=var_pts_at_slope, in_field="x_sec_id",
                               join_table=tbl_x_id_new_centre_sort_start_ends, join_field="x_sec_id",
                               fields="MIN_Sort_Value;MAX_Sort_Value;MAX_NewCentre")
    add_field_with_a_value(var_pts_at_slope, "lvl_z", "DOUBLE", "None")  # for future use
    add_field_with_a_value(var_pts_at_slope, "flag_delete", "SHORT", "None")  # for future use

    # -----------------------------------------------------------------------------------------------
    # Step 2: Setup lists
    # ------------------------------------------------------------------------------------------------
    values = [row[0] for row in arcpy.da.SearchCursor(tbl_x_id_new_centre_sort_start_ends, 'x_sec_id')]
    list_x_sec_id = list(values)

    values = [row[0] for row in arcpy.da.SearchCursor(tbl_x_id_new_centre_sort_start_ends, 'MIN_Sort_Value')]
    list_MIN_Sort_Value = list(values)

    values = [row[0] for row in arcpy.da.SearchCursor(tbl_x_id_new_centre_sort_start_ends, 'MAX_Sort_Value')]
    list_MAX_Sort_Value = list(values)

    values = [row[0] for row in arcpy.da.SearchCursor(tbl_x_id_new_centre_sort_start_ends, 'MAX_NewCentre')]
    list_NewCentre = list(values)

    delete_temps([tbl_x_id_new_centre_sort_start_ends])

    # -----------------------------------------------------------------------------------------------
    # Step 3: For each x_sec_id
    # -----------------------------------------------------------------------------------------------
    """
    a. Get MIN_Sort_Value, MAX_Sort_Value and NewCentre
    b. Select pts_high_slopes_for_a_x_sec & get list_sort_values and list_POINT_Z
    c. Separate 4 lists - list_left_sort_values, list_left_point_z, list_right_sort_values, list_right_point_z
    d. Call the function x_sec_level_points_both_sides to get levelled list. 
    """
    i = 0
    for x_sec_id in list_x_sec_id:
        x_sec_id = list_x_sec_id[i]

        # a. Get MIN_Sort_Value, MAX_Sort_Value and NewCentre
        # ------------------------------------------------------
        print(f'-----------------------------------------------')
        print(f'x_sec_id = {x_sec_id}')
        print(f'-----------------------------------------------')
        MIN_Sort_Value = int(list_MIN_Sort_Value[i])
        MAX_Sort_Value = int(list_MAX_Sort_Value[i])
        NewCentre = int(list_NewCentre[i])

        # b. Select pts_high_slopes_for_a_x_sec & get list_sort_values and list_POINT_Z
        # -------------------------------------------------------------------------------
        expression = "x_sec_id = " + str(x_sec_id)
        list_sort_values, list_POINT_Z = get_lists_for_sv_and_z_for_xsec_id(x_sec_id, expression, None,
                                                                            var_pts_at_slope)

        # c. Separate 4 lists - list_left_sort_values, list_left_point_z, list_right_sort_values, list_right_point_z
        # ---------------------------------------------------------
        index_new_centre = list_sort_values.index(NewCentre)
        index_MIN_Sort_Value = list_sort_values.index(MIN_Sort_Value)
        index_MAX_Sort_Value = list_sort_values.index(MAX_Sort_Value)
        # Left values
        list_left_sort_values = list_sort_values[index_MIN_Sort_Value:index_new_centre+1]
        list_left_sort_values.reverse()
        list_left_point_z = list_POINT_Z[index_MIN_Sort_Value:index_new_centre+1]
        list_left_point_z.reverse()
        # Right values
        list_right_sort_values = list_sort_values[index_new_centre:index_MAX_Sort_Value+1]
        list_right_point_z = list_POINT_Z[index_new_centre:index_MAX_Sort_Value+1]
        print(f'original left sort values = {list_left_sort_values}')
        print(f'original left point_z = {list_left_point_z}')
        print(f'original right sort values = {list_right_sort_values}')
        print(f'original right point_z = {list_right_point_z}')

        # d. Call the function x_sec_level_points_both_sides to get levelled list.
        # ----------------------------------------------------------------------------------------
        if len(list_left_sort_values) <= 2 or len(list_right_sort_values) <= 2:
            print(f'One of the side is short. This x_sec_id = {x_sec_id} is ignored.')
            expression = f'x_sec_id = {x_sec_id}'
            delete_features_using_expression(var_pts_at_slope, expression)
        else:
            x_sec_level_points_both_sides(var_x_sec3d_pts_v3, x_sec_id, list_left_sort_values, list_left_point_z,
                                                  list_right_sort_values, list_right_point_z, var_pts_at_slope)
        # continue loop
        i += 1

    # finalise outputs -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # make a copy for upstream correction before levelling it.
    pts_high_slopes_2 = f'{var_project_folder}\\temp.gdb\\pts_high_slopes_2'
    delete_temps([pts_high_slopes_2])
    arcpy.Select_analysis(in_features=var_pts_at_slope, out_feature_class=pts_high_slopes_2, where_clause="")
    print("Finalising levelled points..")

    x_sec3d_pts_temp = f'{var_project_folder}\\temp.gdb\\x_sec3d_pts_temp1'
    tbl_new_start_ends = f'{var_project_folder}\\temp.gdb\\tbl_new_start_ends1'
    tbl_x_sec_id_lvl_z = f'{var_project_folder}\\temp.gdb\\tbl_x_sec_id_lvl_z1'
    delete_temps([x_sec3d_pts_temp, tbl_new_start_ends, tbl_x_sec_id_lvl_z])

    finalise_outputs(var_pts_at_slope, var_x_sec3d_pts_v3, var_x_sec3d_levelled_pts, x_sec3d_pts_temp,
                     tbl_new_start_ends, tbl_x_sec_id_lvl_z)
    delete_temps([x_sec3d_pts_temp, tbl_new_start_ends, tbl_x_sec_id_lvl_z])
    # upstream correction using previously saved copy of pts_high_slopes_2
    print("Upstream correction..")
    upstream_correction(var_project_folder, pts_high_slopes_2)
    print("")
    print("Finalising levelled points upstream corrected..")
    x_sec3d_pts_temp = f'{var_project_folder}\\temp.gdb\\x_sec3d_pts_temp2'
    tbl_new_start_ends = f'{var_project_folder}\\temp.gdb\\tbl_new_start_ends2'
    tbl_x_sec_id_lvl_z = f'{var_project_folder}\\temp.gdb\\tbl_x_sec_id_lvl_z2'
    delete_temps([x_sec3d_pts_temp, tbl_new_start_ends, tbl_x_sec_id_lvl_z])

    finalise_outputs(pts_high_slopes_2, var_x_sec3d_pts_v3, var_x_sec3d_levelled_pts_corrected, x_sec3d_pts_temp,
                     tbl_new_start_ends, tbl_x_sec_id_lvl_z)
    delete_temps([x_sec3d_pts_temp, tbl_new_start_ends, tbl_x_sec_id_lvl_z])


def x_sec_level_points_both_sides(x_sec3d_pts_v3, x_sec_id, list_left_sort_values, list_left_point_z,
                                          list_right_sort_values, list_right_point_z, pts_high_slopes):
    # if x_sec_id == 1827:
    #     print("1827")

    print(f'')
    print(f'Step 1: Level based on maximum elevation of sides..')
    print(f'------')
    lvl_z = lvl_elev(list_left_point_z, list_right_point_z)
    calc_lvl_for_a_x_sec(x_sec_id, lvl_z, pts_high_slopes)
    print(f'Starting lvl_z = {lvl_z}')
    list_left_sort_values_trim1, list_left_point_z_trim1 = trim_list_using_max_elev(lvl_z, list_left_sort_values,
                                                                                list_left_point_z)
    list_right_sort_values_trim1, list_right_point_z_trim1 = trim_list_using_max_elev(lvl_z, list_right_sort_values,
                                                                                  list_right_point_z)

    # delete one side banks, otherwise move on.
    if len(list_left_sort_values_trim1) <= 1 or len(list_right_sort_values_trim1) <= 1:  # if a list is empty
        print(f'One of the list is empty. This x_sec_id = {x_sec_id} is ignored.')
        expression = f'x_sec_id = {x_sec_id}'
        delete_features_using_expression(pts_high_slopes, expression)
        return None
    elif (len(list_left_sort_values_trim1) == len(list_left_sort_values)) and \
            (len(list_right_sort_values_trim1) == len(list_right_sort_values)):
        print(f'No changes to the list.')
    else:
        calc_lvl_for_a_x_sec(x_sec_id, lvl_z, pts_high_slopes)
        expression = f'x_sec_id = {x_sec_id} AND not (Sort_Value >= {min(list_left_sort_values_trim1)} ' \
                     f'AND Sort_Value <= {max(list_right_sort_values_trim1)})'
        delete_features_using_expression(pts_high_slopes, expression)
        print(f'Data trimmed.')
        print(f'left sort values = {list_left_sort_values_trim1}')
        print(f'left point_z = {list_left_point_z_trim1}')
        print(f'right sort values = {list_right_sort_values_trim1}')
        print(f'right point_z = {list_right_point_z_trim1}')
    # ---------------------------------------------------------
    print(f'')
    print(f'Step 2: Identify slope gaps and then level again..')
    print(f'------')
    list_left_sv_gap_adj, list_left_point_z_gap_adj, leftGap = slope_gap_adjustment(list_left_sort_values_trim1, list_left_point_z_trim1)
    list_right_sv_gap_adj, list_right_point_z_gap_adj, rightGap = slope_gap_adjustment(list_right_sort_values_trim1, list_right_point_z_trim1)

    if leftGap == 1 or rightGap == 1:  # if there is slope gap affect
        # get extra points and append them to pts_high_slopes
        minExtra = min(list_left_sv_gap_adj) - 1
        maxExtra = max(list_right_sv_gap_adj) + 1
        expression = f'x_sec_id = {x_sec_id} AND Sort_Value in ({minExtra}, {maxExtra})'
        extra_pts = pts_high_slopes + "extra"
        delete_temps([extra_pts])
        arcpy.Select_analysis(in_features=x_sec3d_pts_v3, out_feature_class=extra_pts, where_clause=expression)
        arcpy.Append_management(inputs=extra_pts, target=pts_high_slopes, schema_type="NO_TEST")
        delete_temps([extra_pts])

        # update delete flag
        expression = f'x_sec_id = {x_sec_id} AND not (Sort_Value >= {minExtra} AND Sort_Value <= {maxExtra})'
        flag_to_delete_features_using_expression(pts_high_slopes, expression, 1)

        # get new lists
        expression = f'x_sec_id = {x_sec_id} AND (Sort_Value >= {minExtra} AND Sort_Value <= {max(list_left_sv_gap_adj)})'
        list_left_sv_gap_adj, list_left_point_z_gap_adj = get_lists_for_sv_and_z_for_xsec_id(x_sec_id, expression, "left", pts_high_slopes)
        expression = f'x_sec_id = {x_sec_id} AND (Sort_Value >= {min(list_right_sv_gap_adj)} AND Sort_Value <= {maxExtra})'
        list_right_sv_gap_adj, list_right_point_z_gap_adj = get_lists_for_sv_and_z_for_xsec_id(x_sec_id, expression, "right", pts_high_slopes)

        lvl_z = lvl_elev(list_left_point_z_gap_adj, list_right_point_z_gap_adj)
        print(f'lvl_z after gap treatment = {lvl_z}')
        calc_lvl_for_a_x_sec(x_sec_id, lvl_z, pts_high_slopes)

        new_list_left_sort_values, new_list_left_point_z = trim_list_using_max_elev(lvl_z, list_left_sv_gap_adj,
                                                                                    list_left_point_z_gap_adj)
        new_list_right_sort_values, new_list_right_point_z = trim_list_using_max_elev(lvl_z, list_right_sv_gap_adj,
                                                                                      list_right_point_z_gap_adj)

        print(f'left sort values after gap adjustment = {list_left_sv_gap_adj}')
        print(f'left point_z after gap adjustment = {list_left_point_z_gap_adj}')
        print(f'right sort values after gap adjustment = {list_right_sv_gap_adj}')
        print(f'right point_z after gap adjustment = {list_right_point_z_gap_adj}')

        expression = f'x_sec_id = {x_sec_id} AND not (Sort_Value >= {min(new_list_left_sort_values)} ' \
                     f'AND Sort_Value <= {max(new_list_right_sort_values)})'
        flag_to_delete_features_using_expression(pts_high_slopes, expression, 1)

        print(f'')
        print(f'Data trimmed after slope gaps found:')
        print(f'final left sort_values = {new_list_left_sort_values}')
        print(f'final left point_z = {new_list_left_point_z}')
        print(f'final right sort_values = {new_list_right_sort_values}')
        print(f'final right point_z = {new_list_right_point_z}')
    else:
        print(f'No slope gaps found.')


def finalise_outputs(var_pts_high_slopes, x_sec3d_pts, x_sec3d_levelled_pts, x_sec3d_pts_temp,
                     tbl_new_start_ends, tbl_x_sec_id_lvl_z):
    # Step 7: delete flag_delete = 1 and recalculate lvl_z for final points after deletion
    # ---------------------------------------------------------
    expression = f'flag_delete = 1'
    delete_features_using_expression(var_pts_high_slopes, expression)

    # Step 8: gather final bounds and the outputs ----------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------
    arcpy.Statistics_analysis(in_table=var_pts_high_slopes, out_table=tbl_new_start_ends,
                              statistics_fields="Sort_Value MIN;Sort_Value MAX", case_field="x_sec_id")
    # make a copy and join and make it original again
    arcpy.DeleteField_management(in_table=x_sec3d_pts, drop_field="MIN_Sort_Value;MAX_Sort_Value")
    arcpy.Select_analysis(in_features=x_sec3d_pts, out_feature_class=x_sec3d_pts_temp, where_clause="")
    arcpy.JoinField_management(in_data=x_sec3d_pts_temp, in_field="x_sec_id", join_table=tbl_new_start_ends,
                               join_field="x_sec_id", fields="MIN_Sort_Value;MAX_Sort_Value")
    delete_temps([tbl_new_start_ends])
    # rename it back to normal
    delete_temps([x_sec3d_pts])
    arcpy.Select_analysis(in_features=x_sec3d_pts_temp, out_feature_class=x_sec3d_pts, where_clause="")
    delete_temps([x_sec3d_pts_temp])

    # Export newly trimmed transacts --------------------------------------------------------------------
    arcpy.Select_analysis(in_features=x_sec3d_pts, out_feature_class=x_sec3d_levelled_pts,
                          where_clause="Sort_Value >= MIN_Sort_Value AND Sort_Value <= MAX_Sort_Value")
    arcpy.DeleteField_management(in_table=x_sec3d_pts, drop_field="MIN_Sort_Value;MAX_Sort_Value")
    arcpy.DeleteField_management(in_table=x_sec3d_levelled_pts,
                                 drop_field="POINT_X;POINT_Y;UNQID;MIN_Sort_Value;MAX_Sort_Value")

    arcpy.Statistics_analysis(in_table=x_sec3d_levelled_pts, out_table=tbl_x_sec_id_lvl_z,
                              statistics_fields="POINT_Z MAX", case_field="x_sec_id")
    add_field_with_a_value(tbl_x_sec_id_lvl_z, "lvl_z", "DOUBLE", '!MAX_POINT_Z!')
    arcpy.DeleteField_management(in_table=x_sec3d_levelled_pts, drop_field="lvl_z")
    arcpy.JoinField_management(in_data=x_sec3d_levelled_pts, in_field="x_sec_id", join_table=tbl_x_sec_id_lvl_z,
                               join_field="x_sec_id", fields="lvl_z")
    delete_temps([tbl_x_sec_id_lvl_z])

    print("Process Completed: " + x_sec3d_levelled_pts)


def upstream_correction(project_folder, pts_high_slopes_2):
    # --------------------------------------------------------------------------------------------------------
    # Step 6 - Apply linear regression on data to fine tune outliers
    # a. get a table for each x_sec_id get Min_seg_id and Max_lvl_z
    # b. for each segment make x-sections of groups of 10 and each group has an id (reg_id).
    # c. for each group of 10 x-sections use their lvl_z values can apply linear regression function.
    # -------------------------------------------------------------------------------------------------------

    # export a unique table for each
    tbl_x_id_seg_id_lvl_z = f'{project_folder}\\temp.gdb\\tbl_x_id_seg_id_lvl_z'
    tbl_x_id_lvl_z_for_selected_reg = f'{project_folder}\\temp.gdb\\tbl_x_id_lvl_z_for_selected_reg'
    delete_temps([tbl_x_id_seg_id_lvl_z])

    arcpy.Statistics_analysis(in_table=pts_high_slopes_2, out_table=tbl_x_id_seg_id_lvl_z,
                              statistics_fields="seg_id MIN;lvl_z MAX", case_field="x_sec_id")
    # Set unique reg_id for each 10 points of a segment
    add_field_with_a_value(tbl_x_id_seg_id_lvl_z, "reg_id", "LONG", "None")

    # get list of seg_id
    values = [row[0] for row in arcpy.da.SearchCursor(tbl_x_id_seg_id_lvl_z, 'MIN_seg_id')]
    list_seg_ids = set(values)

    for seg_id in list_seg_ids:
        cur_seg_id = int(seg_id)
        # print(cur_seg_id)
        expression = arcpy.AddFieldDelimiters(tbl_x_id_seg_id_lvl_z, "MIN_seg_id") + f' = {cur_seg_id}'
        with arcpy.da.UpdateCursor(tbl_x_id_seg_id_lvl_z, ["x_sec_id", "reg_id"],
                                   where_clause=expression) as cursor_tbl:
            i = 1
            j = 1
            for row_tbl in cursor_tbl:
                x_sec_id = row_tbl[0]
                reg_id = int(f'{cur_seg_id}{j}')
                row_tbl[1] = reg_id
                # print(f'x_sec_id = {x_sec_id}, reg_id = {reg_id}')
                cursor_tbl.updateRow(row_tbl)
                i += 1
                if i > 10:  # 10 points only
                    i = 1  # set to look for next 20 points
                    j += 1  # set next reg_id

    # get list of reg_id
    values_reg_ids = [row[0] for row in arcpy.da.SearchCursor(tbl_x_id_seg_id_lvl_z, 'reg_id')]
    list_reg_ids = set(values_reg_ids)
    list_reg_ids = sorted(list_reg_ids)
    # -----------------------------------------------------------
    for reg_id in list_reg_ids:
        cur_reg_id = int(reg_id)
        print(f'-----------------------------')
        print(f'Batch list id: = {cur_reg_id}')
        print(f'-----------------------------')
        delete_temps([tbl_x_id_lvl_z_for_selected_reg])
        arcpy.TableSelect_analysis(in_table=tbl_x_id_seg_id_lvl_z, out_table=tbl_x_id_lvl_z_for_selected_reg,
                                   where_clause=f'reg_id = {cur_reg_id}')
        # apply linear regression on data to fine tune outliers
        apply_linear_regression(tbl_x_id_lvl_z_for_selected_reg, pts_high_slopes_2)


def list_without_outliers(list_x_org, list_y_org):
    # find general outliers
    # ------------------------------
    list_x_org2 = []
    list_y_org2 = []
    i = 0
    len_x = len(list_x_org) - 1
    for x_value in list_x_org:
        cur_x = list_x_org[i]
        cur_y = list_y_org[i]
        if i > 0:
            pre_y = list_y_org[i - 1]
        else:
            pre_y = cur_y

        if (i + 1) <= len_x:
            next_y = list_y_org[i + 1]
        else:
            next_y = cur_y

        # logic
        # print(f'{pre_y}, {cur_y}, {next_y}')
        if cur_y < (pre_y - 3) or cur_y < (next_y - 3):  # outlier
            print(f'Outlier value: {cur_y}')
        else:
            list_x_org2.append(cur_x)
            list_y_org2.append(cur_y)
        # increase i
        i += 1

    return list_x_org2, list_y_org2


def apply_linear_regression(tbl_x_id_lvl_z_seg_id, var_pts_high_slopes):
    """
    1. Get list without general outliers
    2. Model linear regression without outliers
    3. Get predicted and residuals using the Model that is without outliers
    4. Adjust values

    :param tbl_x_id_lvl_z_seg_id:
    :param pts_high_slopes:
    :return:
    """
    # this layer (pts_high_slopes_lyr) "lvl_z" will be updated
    # delete_temps(["pts_high_slopes_lyr"])
    # arcpy.MakeFeatureLayer_management(in_features=pts_high_slopes, out_layer="pts_high_slopes_lyr")

    # This temporary table (tbl_x_id_lvl_z_seg_id) will be used to get updated lvl_z values)
    # develop two lists
    values_x = [row[0] for row in arcpy.da.SearchCursor(tbl_x_id_lvl_z_seg_id, 'x_sec_id')]
    list_x_org = list(values_x)
    values_y = [row[0] for row in arcpy.da.SearchCursor(tbl_x_id_lvl_z_seg_id, 'MAX_lvl_z')]
    list_y_org = list(values_y)
    delete_temps([tbl_x_id_lvl_z_seg_id]) # this temp table no longer required.
    print(list_x_org)
    print(list_y_org)

    x_org = np.array(list_x_org).reshape((-1, 1))
    y_org = np.array(list_y_org)

    if len(list_x_org) < 5:  # if number of observations < 5
        print("No. of Observations < 5")
        return None

    # 1. Get list without general outliers
    # ------------------------------
    list_x_org2, list_y_org2 = list_without_outliers(list_x_org, list_y_org)
    if len(list_x_org2) == len(list_x_org):  # nothing has been removed.
        print(f'No outliers.')
        return None

    # 2. Model linear regression without outliers
    # ------------------------------------------
    x2 = np.array(list_x_org2).reshape((-1, 1))
    y2 = np.array(list_y_org2)

    model_no_outliers = LinearRegression().fit(x2, y2)  # this is developed using the lists that has NO outliers.
    r_sq = round(model_no_outliers.score(x2, y2), 2)
    m_slope = model_no_outliers.coef_
    print('R2 after removal of Outlier:', r_sq)
    # print('Intercept:', round(model_no_outliers.intercept_, 2))
    print('Slope:', m_slope)

    if m_slope > 0:
        print(f'Positive Slope.')
        return None

    # 3. Get predicted and residuals using the Model that is without outliers
    # -----------------------------------------------------

    y_org_pred = model_no_outliers.predict(x_org)
    list_y_org_pred = y_org_pred.tolist()  # make a list of predicted values for the original values
    y_diff = y_org - y_org_pred
    print(f'Residuals = {y_diff}')

    # 4. Adjust values
    # -----------------------------------------------------------------------
    i = 0
    for value in y_diff:
        if value < -1 or value > 1:  # if the difference is between +/- 1
            y_org[i] = y_org_pred[i]
            y_new = list_y_org_pred[i]
            print(f'Re-adjusted: {x_org[i]}, {y_org[i]}')
            calc_lvl_for_a_x_sec(list_x_org[i], y_new, var_pts_high_slopes)

            expression = f'x_sec_id = {list_x_org[i]} and POINT_Z <= {y_new}'
            flag_to_delete_features_using_expression(var_pts_high_slopes, expression, 0)
        i += 1


def lvl_elev(list_left_point_z, list_right_point_z):
    if max(list_left_point_z) < max(list_right_point_z):
        lvl_z = max(list_left_point_z)
    else:
        lvl_z = max(list_right_point_z)
    return lvl_z


def slope_gap_adjustment(list_sort_values, list_point_z):
    gap_found = 0
    if len(list_sort_values) < 5:
        return list_sort_values, list_point_z, 0
    else:
        gap_adjusted_list_sort_values = []
        gap_adjusted_list_point_z = []
        gap = 3

        i = 0
        for sv in list_sort_values:
            cur_sv = list_sort_values[i]
            cur_pt_z = list_point_z[i]
            # print(cur_sv)
            if i < 3:  # let the first two point go
                gap_adjusted_list_sort_values.append(cur_sv)
                gap_adjusted_list_point_z.append(cur_pt_z)
            else:
                sv_gap = cur_sv - list_sort_values[i - 1]
                if sv_gap < 0:
                    sv_gap = - sv_gap
                # print(sv_gap)
                if sv_gap <= gap:
                    gap_adjusted_list_sort_values.append(cur_sv)
                    gap_adjusted_list_point_z.append(cur_pt_z)
                else:
                    print(f'Slope discontinuity found.')
                    gap_found = 1
                    break
            i += 1
    return gap_adjusted_list_sort_values, gap_adjusted_list_point_z, gap_found


def flag_to_delete_features_using_expression(var_pts_high_slopes, expression, value):

    arcpy.MakeFeatureLayer_management(in_features=var_pts_high_slopes,
                                      out_layer="pts_high_slopes_lyr")
    arcpy.SelectLayerByAttribute_management(in_layer_or_view="pts_high_slopes_lyr",
                                            selection_type="NEW_SELECTION", where_clause=expression)
    arcpy.CalculateField_management(in_table="pts_high_slopes_lyr", field="flag_delete",
                                    expression=int(value), expression_type="PYTHON",
                                    code_block="")
    arcpy.SelectLayerByAttribute_management(in_layer_or_view="pts_high_slopes_lyr",
                                            selection_type="CLEAR_SELECTION", where_clause="")
    delete_temps(["pts_high_slopes_lyr"])


def calc_lvl_for_a_x_sec(x_sec_id, lvl_z, var_pts_high_slopes):
    expression = f'x_sec_id = {str(x_sec_id)}'
    # print(expression)
    arcpy.MakeFeatureLayer_management(in_features=var_pts_high_slopes,
                                      out_layer="pts_high_slopes_lyr")
    arcpy.SelectLayerByAttribute_management(in_layer_or_view="pts_high_slopes_lyr",
                                            selection_type="NEW_SELECTION", where_clause=expression)
    arcpy.CalculateField_management(in_table="pts_high_slopes_lyr", field="lvl_z",
                                    expression=lvl_z, expression_type="PYTHON",
                                    code_block="")
    arcpy.SelectLayerByAttribute_management(in_layer_or_view="pts_high_slopes_lyr",
                                            selection_type="CLEAR_SELECTION", where_clause="")
    delete_temps(["pts_high_slopes_lyr"])


def trim_list_using_max_elev(lvl_z, list_sort_values, list_point_z):
    """
    This will send the new limits based lvl_z
    """
    list_sort_values_lvl = []
    list_point_z_lvl = []

    if len(list_sort_values) < 3:
        list_sort_values_lvl = list_sort_values
        list_point_z_lvl = list_point_z
    else:
        i = 0
        for item in list_sort_values:
            sv = list_sort_values[i]
            z = list_point_z[i]
            if z <= lvl_z:
                list_sort_values_lvl.append(sv)
                list_point_z_lvl.append(z)
            i += 1
    # ----------------------
    return list_sort_values_lvl, list_point_z_lvl


def x_sec_bfw_poly(project_folder, x_sec3d_levelled_lines, output_bfw_poly):

    left_pts = f'{project_folder}\\temp.gdb\\left_pts'
    right_pts = f'{project_folder}\\temp.gdb\\right_pts'
    merge_pts = f'{project_folder}\\temp.gdb\\merge_pts'

    left_pts_line = f'{project_folder}\\temp.gdb\\left_pts_line'
    right_pts_line = f'{project_folder}\\temp.gdb\\right_pts_line'
    merge_pts_line = f'{project_folder}\\temp.gdb\\merge_pts_line'

    bfw_poly_v1 = f'{project_folder}\\temp.gdb\\bfw_poly_v1'

    delete_temps([left_pts, right_pts, merge_pts, left_pts_line, right_pts_line, merge_pts_line, bfw_poly_v1])

    arcpy.FeatureVerticesToPoints_management(in_features=x_sec3d_levelled_lines,
                                             out_feature_class=left_pts, point_location="START")
    arcpy.FeatureVerticesToPoints_management(in_features=x_sec3d_levelled_lines,
                                             out_feature_class=right_pts, point_location="END")
    arcpy.Merge_management(inputs=f'{right_pts};{left_pts}', output=merge_pts)

    arcpy.PointsToLine_management(Input_Features=left_pts, Output_Feature_Class=left_pts_line,
                                  Line_Field="seg_id", Sort_Field="x_sec_id", Close_Line="NO_CLOSE")
    arcpy.PointsToLine_management(Input_Features=right_pts, Output_Feature_Class=right_pts_line,
                                  Line_Field="seg_id", Sort_Field="x_sec_id", Close_Line="NO_CLOSE")
    arcpy.PointsToLine_management(Input_Features=merge_pts,
                                  Output_Feature_Class=merge_pts_line, Line_Field="seg_id",
                                  Sort_Field="x_sec_id", Close_Line="NO_CLOSE")

    arcpy.FeatureToPolygon_management(in_features=f'{merge_pts_line};{right_pts_line};{left_pts_line}',
                                      out_feature_class=bfw_poly_v1, cluster_tolerance="",
                                      attributes="NO_ATTRIBUTES", label_features="")
    arcpy.Dissolve_management(in_features=bfw_poly_v1, out_feature_class=output_bfw_poly,
                              dissolve_field="", statistics_fields="", multi_part="SINGLE_PART",
                              unsplit_lines="DISSOLVE_LINES")

    delete_temps([left_pts, right_pts, merge_pts, left_pts_line, right_pts_line, merge_pts_line, bfw_poly_v1])


# *********************************************************************************************************************
# Functions: General
# *********************************************************************************************************************

def has_fld(fc, field_name):
    lst_fields = arcpy.ListFields(fc)
    x = False
    for field in lst_fields:
        if field.name == field_name:
            x = True
            return x


def add_field_with_a_value(fc, fld_name, fld_type, fld_value):
    if not has_fld(fc, fld_name):
        arcpy.AddField_management(fc, fld_name, fld_type)
        arcpy.CalculateField_management(fc, fld_name, fld_value, "PYTHON")
    else:
        arcpy.CalculateField_management(fc, fld_name, fld_value, "PYTHON")


def delete_temps(temp_list):
    for item in temp_list:
        if arcpy.Exists(item):
            arcpy.Delete_management(item)
            # print(f'Deleted temp file {item}.')


def get_raster_value_for_points(project_folder, pts_shp, dem, elev_field):
    extract_pts = f'{project_folder}\\temp.gdb\\extract_pts'
    delete_temps([extract_pts])
    if not has_fld(pts_shp, elev_field):
        arcpy.AddField_management(pts_shp, elev_field, "DOUBLE")

    if pts_shp.endswith('.shp'):
        fldvalue = '!FID! + 1'
    else:
        fldvalue = '!OBJECTID!'

    add_field_with_a_value(pts_shp, "UNQID", "LONG", fldvalue)
    arcpy.gp.ExtractValuesToPoints_sa(pts_shp, dem, extract_pts, "NONE", "VALUE_ONLY")
    arcpy.JoinField_management(pts_shp, "UNQID", extract_pts, "UNQID", "RASTERVALU")
    arcpy.CalculateField_management(pts_shp, elev_field, '!RASTERVALU!', "PYTHON_9.3", "")
    arcpy.DeleteField_management(pts_shp, "RASTERVALU")

    # clean up
    delete_temps([extract_pts])


def delete_features_using_expression(pts_high_slopes, expression):
    # print(expression)
    arcpy.MakeFeatureLayer_management(in_features=pts_high_slopes,
                                      out_layer="pts_high_slopes_lyr")
    arcpy.SelectLayerByAttribute_management(in_layer_or_view="pts_high_slopes_lyr",
                                            selection_type="NEW_SELECTION", where_clause=expression)
    arcpy.DeleteFeatures_management(in_features="pts_high_slopes_lyr")
    arcpy.SelectLayerByAttribute_management(in_layer_or_view="pts_high_slopes_lyr",
                                            selection_type="CLEAR_SELECTION", where_clause="")
    delete_temps(["pts_high_slopes_lyr"])


def get_lines_poly(project_folder, x_sec3d_levelled_pts, x_sec3d_levelled_lines, x_sec3d_levelled_bfw_poly):
    # --------------------------------------------
    # Step 3: Get levelled lines
    # --------------------------------------------
    print(f'Processing: Levelled lines..')
    delete_temps([x_sec3d_levelled_lines, x_sec3d_levelled_bfw_poly])
    arcpy.PointsToLine_management(Input_Features=x_sec3d_levelled_pts,
                                  Output_Feature_Class=x_sec3d_levelled_lines,
                                  Line_Field="x_sec_id", Sort_Field="Sort_Value", Close_Line="NO_CLOSE")
    arcpy.JoinField_management(in_data=x_sec3d_levelled_lines, in_field="x_sec_id",
                               join_table=x_sec3d_levelled_pts, join_field="x_sec_id",
                               fields="seg_id")
    arcpy.JoinField_management(in_data=x_sec3d_levelled_lines, in_field="x_sec_id",
                               join_table=x_sec3d_levelled_pts,
                               join_field="x_sec_id", fields="lvl_z")

    w_d_stats = f'{project_folder}\\temp.gdb\\w_d_stats'
    arcpy.Statistics_analysis(in_table=x_sec3d_levelled_pts,
                              out_table=w_d_stats,
                              statistics_fields="POINT_Z MIN;POINT_Z MAX", case_field="x_sec_id")
    arcpy.AddField_management(in_table=w_d_stats, field_name="lvl_d", field_type="DOUBLE")
    arcpy.CalculateField_management(in_table=w_d_stats, field="lvl_d",
                                    expression="round ((!MAX_POINT_Z! - !MIN_POINT_Z!), 4)",
                                    expression_type="PYTHON", code_block="")

    arcpy.JoinField_management(in_data=x_sec3d_levelled_lines, in_field="x_sec_id",
                               join_table=w_d_stats, join_field="x_sec_id", fields="lvl_d")
    arcpy.AddField_management(in_table=x_sec3d_levelled_lines, field_name="lvl_w", field_type="DOUBLE")
    arcpy.CalculateField_management(in_table=x_sec3d_levelled_lines, field="lvl_w",
                                    expression="round (!Shape_Length!, 4)", expression_type="PYTHON",
                                    code_block="")
    delete_temps([w_d_stats])
    # --------------------------------------------
    # Step 4: Get BFW polygon
    # --------------------------------------------
    print(f'Processing: Bankfull polygon..')
    x_sec_bfw_poly(project_folder, x_sec3d_levelled_lines, x_sec3d_levelled_bfw_poly)
    print(f'Completed the process.')

