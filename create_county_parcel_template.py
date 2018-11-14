#####################################################################
#FILE: county_parcel_template_2.py
#AUTHOR: Melinda Pullman
#EMAIL: 
#ORGANIZATION: 
#CREATION DATE: 09/26/2018
#LAST MOD DATE: N/A
#PURPOSE: This script will create a template county feature class that 
#         can be used to copy attributes from the template feature class 
#         to other shapefiles
#DEPENDENCIES: arcpy, os
#####################################################################

def create_county_template(template_location, template_name, spatial_ref, field_names, field_types, field_lengths):

    """
    PARAMETERS:
    workspace - a string of the feature dataset or feature geodatabase in which to store the template feature class
    template_name - a string containing the name of the template feature class
    spatial_ref - a string of the spatial reference of the template feature class
    field_names - an array of strings containing the names of each field to store in the template feature class
    field_types - an array of strings containing the types of each field to store in the template feature class
    field_lengths - an array of strings containing the types of each field to store in the template feature class

    *** field_names, field_types, and field_lengths must all be arrays of the same length!! ***
    
    USE:
    >>> workspace = r"C:\Users\...\.gdb\template_county"
    >>> template_name = "county_parcels_template"
    >>> spatial_ref = "..."
    >>> field_names = ["field_name1", "field_name2", "field_name3",...]
    >>> field_types = ["field_type1", "field_type2", "field_type3",...]
    >>> field_legnths = ["field_length1", "field_length2", "field_length3",...]
    >>> create_county_template(workspace, template_name, spatial_ref, field_names, field_types, field_lengths)
    """

    ## Import Dependencies
    import arcpy
    import os

    ## Set Environmental Variables
    arcpy.env.overwriteOutput = True
    workspace = arcpy.env.workspace = template_location

    ## Set Local Variables
    sr = arcpy.SpatialReference(spatial_ref)
    
    ## Create a New Empty Feature Class
    template = arcpy.CreateFeatureclass_management(workspace, template_name, "POLYGON")

    ## Add Fields to New Feature Class
    for i in range(0, len(field_names)):
        arcpy.AddField_management(template, field_names[i], field_types[i], field_lengths[i])

## Define local variables
template_location = r'C:\Users\m3rexmkp\Desktop\Database\re_database_1.gdb\template_county'
template_name = "county_parcels_template4"
spatial_ref = "NAD 1983 StatePlane Texas S Central FIPS 4204 (US Feet)"
field_names = ["PropertyID", "GeoID", "OwnerID", "AccountNumber", "LegalDesc", "LegalArea", "Year", "OwnerName", "OwnerName2", \
               "Address1", "Address2", "Address3", "AddressCity", "AddressState", "AddressZip", "AddressCountry", "SitusNumber", \
               "SitusPrefix", "SitusStreet", "SitusSuffix", "SitusCity", "SitusState", "SitusZip"]
field_types = ["STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", \
               "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING"]
field_lengths = ["50", "50", "50", "50", "255", "50", "50", "70", "70", "60", "60", "60", "50", "50", "16", "5", "15", "10", "50", \
                 "10", "30", "2", "10"]

## Run the Function
create_county_template(template_location, template_name, spatial_ref, field_names, field_types, field_lengths)
    
