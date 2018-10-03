#####################################################################
#FILE: project_files.py
#AUTHOR: Melinda Pullman
#EMAIL: Melinda.K.Pullman@usace.army.mil
#ORGANIZATION: USACE|SWG
#CREATION DATE: 08/07/2018
#LAST MOD DATE: N/A
#PURPOSE: This script will create an empty file geodatabase and
#         feature datasets for land characteristics
#DEPENDENCIES: arcpy, os
#####################################################################

def create_geodatabase(out_folder_path, file_gdb_name, feature_dataset_names, spatial_ref):

    """
    PARAMETERS:
    out_folder_path: string to the output folder where the geodatabase will be stored
    file_gdb_name: string of the file geodatabase name
    feature_dataset_names: an array storing the names of each feature dataset to create
    under the file geodatabase.  the names of the feature datasets will be in the form
    of strings
    USE:
    >>> out_folder_path = r"C:\Users\...\Datasbase"
    >>> file_gdb_name = r"geodatabase_name.gdb"
    >>> feature_dataset_name = ["geodataset1", "geodataset2", "geodataset3",...]
    >>> create_geodatabase(out_folder_path, file_gdb_name, feature_dataset_name)
    """

    ## Import Packages
    import arcpy
    import os
    
    ## Set Local Environment Variables
    arcpy.env.overwriteOutput = True 
    
    ## Create a Spatial Reference Object
    sr = arcpy.SpatialReference(spatial_ref)

    ## Create a File Geodatabase for the Feature Datasets
    arcpy.CreateFileGDB_management(out_folder_path, file_gdb_name)

    ## Get the Output Geodatabase Path
    out_gdb_path = os.path.join(out_folder_path, file_gdb_name)

    ## Create Feature Datasets
    for name in feature_dataset_names:
        arcpy.CreateFeatureDataset_management(out_gdb_path, name, sr)

        
## Set Local Variables
out_folder_path = r"C:\Users\m3rexmkp\Desktop\Database"
file_gdb_name = r"land_characteristics2.gdb"

feature_dataset_names = ["cbrs_polygons", "county_parcels", "county_zoning", "csrm_alternatives", \
                         "er_alternatives", "federal_lands", "fema_flood_hazard_layer", "land_use",\
                         "soils", "state_lands", "epa_brownfields", "superfund_sites", "wetlands"]

spatial_ref = "NAD 1983 StatePlane Texas S Central FIPS 4204 (US Feet)"

## Run the Function:
create_geodatabase(out_folder_path, file_gdb_name, feature_dataset_names, spatial_ref)
