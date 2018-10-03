#####################################################################
#FILE: append_parcels_to_template_3.py
#AUTHOR: Melinda Pullman
#EMAIL: Melinda.K.Pullman@usace.army.mil
#ORGANIZATION: USACE|SWG
#CREATION DATE: 09/28/2018
#LAST MOD DATE: N/A
#PURPOSE: This script will copy attributes from the county parcel
#         shapefiles to the template shapefile for standardizing
#         attribute fields
#DEPENDENCIES: arcpy, os, numpy
#####################################################################

def append_parcels_to_template(fc, template, fc_field_names, template_field_names, output_fc):

    """
    PARAMETERS
    fc - the string containing the path where the county feature class is stored
    template - the string containing the path where the template feature class is stored
    fc_field_names - a string containing the county feature class names that will be 
    appened to the template feature class 
    template_field_names - a string containing the template field names that the county
    feature class fields will be appened to 
    output_fc - the resulting county feature class with the template field names 
    USE
    >>> fc = r'C:\Users\...\county_feature_class'
    >>> template = r'C:\Users\...\template_feature_class'
    >>> fc_field_names = ['Field1', 'Field2', 'Field3',...]
    >>> template_field_names = ['Field1', 'Field2', 'Field3',...]
    >>> output_fc = r'C:\Users\...\output_feature_class'
    >>> append_parcels_to_template(fc, template, fc_field_names, template_field_names, output_fc)
    """
    
    ## Import Dependencies
    import arcpy
    import os
    import numpy as np

    ## Environmental Variables
    arcpy.env.overwriteOutput = True 
    
    ## Create a copy of the template into the corresponding county feature dataset
    arcpy.CopyFeatures_management(template, output_fc)

    ## Define the append and target layers for the arcpy append tool
    append_layer = fc
    target_layer = output_fc

    ## Create a field mapping object (This object looks like the empty grid of fields
    ## you see when you first open the append tool in the toolbox)
    fieldmappings = arcpy.FieldMappings()

    ## Add fields of each layer to the empty grid of fields 
    fieldmappings.addTable(target_layer)
    fieldmappings.addTable(append_layer)

    ## Map the fiels with different names; first creat an empty list that will hold the corresponding names
    list_of_fields_we_will_map = []
    
    ## Create tuples of corresponding field names to be stored in the list 
    ## Get indices of county parcel shapefile that are non null b/c null feild names will throw an error
    ## in the append tool
    x = np.flatnonzero(fc_field_names != "")
    
    ## Append non null field names into the tuples
    for i in range(0, len(x)):
        list_of_fields_we_will_map.append((template_field_names[x[i]], fc_field_names[x[i]]))

    ## Now map the field names 
    for field_map in list_of_fields_we_will_map:
        
        ## Find the fields index by name
        field_to_map_index = fieldmappings.findFieldMapIndex(field_map[0])
        
        ## Grab "A copy" of the current field map object for this particular field
        field_to_map = fieldmappings.getFieldMap(field_to_map_index)
        
        ## Update its data source to add the input from the the append layer
        field_to_map.addInputField(append_layer, field_map[1])
        
        ## We edited a copy, update our data grid object with it
        fieldmappings.replaceFieldMap(field_to_map_index, field_to_map)

    ## Create a list of append datasets and run the the tool
    inData = [append_layer]
    arcpy.Append_management(inData, target_layer, "NO_TEST", field_mapping=fieldmappings)


## Run the Function for a Single County
kenedy_field_names = np.array(("Prop_ID", "GeoID", "OwnerID", "", "Parcel_Legal", "Area_Legal", \
                               "", "Owner", "", "", "", "", \
                               "", "", "","", "Situs_Addr", \
                               "Situs_PreDir", "Situs_Street", "Situs_Type", "", "", ""))

template_field_names = np.array(("PropertyID", "GeoID", "OwnerID", "AccountNumber", "LegalDesc", "LegalArea", \
                        "Year", "OwnerName", "OwnerName2", "Address1", "Address2", "Address3", \
                        "AddressCity", "AddressState", "AddressZip", "AddressCountry", "SitusNumber", \
                        "SitusPrefix", "SitusStreet", "SitusSuffix", "SitusCity", "SitusState", "SitusZip"))

fc = r'C:\Users\m3rexmkp\Desktop\Database\coastal_tx_parcels.gdb\kenedy_parcels_072018_project'

template = r'C:\Users\m3rexmkp\Desktop\Database\re_database_1.gdb\template_county\county_parcels_template2'

output_fc = r'C:\Users\m3rexmkp\Desktop\Database\re_database_1.gdb\kenedy_county\kenedy_county_072018'

#append_parcels_to_template(fc, template, kenedy_field_names, template_field_names, output_fc)



## Automate the Function for Every County
import arcpy

workspace = r'C:\Users\m3rexmkp\Desktop\Database\coastal_tx_parcels.gdb'

fc_list = arcpy.ListFeatureClasses(workspace)

template = r'C:\Users\m3rexmkp\Desktop\Database\re_database_1.gdb\template_county\county_parcels_template2'

aransas_field_names = np.array(("PROP_ID", "geo_id", "", "acct_pid", "legal_desc", "legal_acre",\
                                "tax_yr", "file_as_na", "", "addr_line1", "addr_line2", "addr_line3", \
                                "addr_city", "addr_state", "zip", "", "situs_num", \
                                "situs_stre", "situs_st_1", "situs_st_2", "situs_city", "situs_stat", "situs_zip"))

brazoria_field_names = np.array(("PID", "simple_geo", "", "", "LegalDescr", "ACREAGE",\
                                 "", "file_as_na", "", "addr_line1", "addr_line2", "addr_line3", \
                                 "addr_city", "addr_state", "addr_zip", "", "situs_di_1", \
                                 "", "", "", "", "", ""))

calhoun_field_names = np.array(("PROP_ID", "geo_id", "", "", "legal_desc", "legal_acre", \
                                "tax_yr", "file_as_na", "", "addr_line1", "addr_line2", "addr_line3",\
                                "addr_city", "addr_state", "zip", "", "situs_num", \
                                "situs_stre", "situs_st_1", "situs_st_2", "situs_city", "situs_stat", "situs_zip"))

cameron_field_names = np.array(("PROP_ID", "GEO_ID","owner_id", "", "legal1", "acres", \
                       "appr_yr", "owner", "adtn_nam", "addr1", "addr2", "",  \
                       "adr_city", "adr_str", "adr_zip", "country", "situs_no", \
                       "sit_pfx", "sit_str", "sit_sfx", "sit_cty", "sit_st", "sit_zip"))

chambers_field_names = np.array(("Property_ID", "", "", "Account", "legal_description", "Total_Tract_Acres", \
                                 "", "Owner_Name", "", "Owner_Address_1", "Owner_Address_2", "", \
                                 "Owner_City", "Owner_State", "Owner_Zip", "", "Site_Description", \
                                 "", "", "", "", "", ""))

fort_bend_field_names = np.array(("PROPNOSRCH", "", "OwnerID", "", "LEGAL_1", "GISCALCULA", \
                                  "", "OWNERNAME", "", "OADDR1", "OADDR2", "OADDR3", \
                                  "OWNERCITY", "OWNERSTATE", "OWNERZIP", "", "SITUSSNO", \
                                  "SITUSPRDIR", "SITUSSNM", "situs_suffix", "", "", ""))

galveston_field_names = np.array(("ID", "GEOID", "", "", "LEGAL", "ACRES", \
                                  "", "NAME", "", "ADDRESS", "ADDRESS2", "ADDRESS3", \
                                  "CITY", "ST", "ZIP", "", "SITUS_NO", \
                                  "SITUS", "", "", "", "", "")) 

harris_field_names = np.array(("", "", "", "HCAD_NUM", "", "", \
                               "", "CurrOwner", "", "", "", "", \
                               "", "", "", "", "LocNum", \
                               "LocAddr", "", "", "city", "", "zip"))

jefferson_field_names = np.array(("Prop_ID", "geo_id", "owner_id", "", "legal_desc", "legal_acre", \
                                  "owner_tax_", "file_as_na", "", "addr_line1", "addr_line2", "addr_line3", \
                                  "addr_city", "addr_state", "zip", "", "situs", \
                                  "situs_stre", "situs_st_1", "situs_st_2", "situs_city", "situs_stat", "situs_zip"))

kenedy_field_names = np.array(("Prop_ID", "GeoID", "OwnerID", "", "Parcel_Legal", "Area_Legal", \
                               "", "Owner", "", "", "", "", \
                               "", "", "","", "Situs_Addr", \
                               "Situs_PreDir", "Situs_Street", "Situs_Type", "", "", ""))

matagorda_field_names = np.array(("PROP_ID", "geo_id", "", "acct_pid", "legal_desc", "legal_acre", \
                                  "tax_yr", "file_as_na", "", "addr_line1", "addr_line2", "addr_line3", \
                                  "addr_city", "addr_state", "zip", "", "situs_num", \
                                  "situs_stre", "situs_st_1", "situs_st_2", "situs_city", "situs_stat", "situs_zip"))

nueces_field_names = np.array(("PROP_ID", "SIMPLE_GEO", "", "TAXID", "LEGAL", "ACREAGE", \
                               "APPRYEAR", "NAME", "", "ADDRESS", "ADDRESS2", "", \
                               "CITY", "STATE", "ZIP", "", "SITE_NUM", \
                               "", "SITE_STR", "", "", "", "ZIP_CODE"))

template_field_names = np.array(("PropertyID", "GeoID", "OwnerID", "AccountNumber", "LegalDesc", "LegalArea", \
                        "Year", "OwnerName", "OwnerName2", "Address1", "Address2", "Address3", \
                        "AddressCity", "AddressState", "AddressZip", "AddressCountry", "SitusNumber", \
                        "SitusPrefix", "SitusStreet", "SitusSuffix", "SitusCity", "SitusState", "SitusZip"))

county_field_names = [aransas_field_names, brazoria_field_names, calhoun_field_names, cameron_field_names, \
                      chambers_field_names, fort_bend_field_names, galveston_field_names, harris_field_names, \
                      jefferson_field_names, kenedy_field_names, matagorda_field_names, nueces_field_names]

county_names = ['aransas_county', 'brazoria_county', 'calhoun_county', 'cameron_county', 'chambers_county', \
                'fort_bend_county', 'galveston_county', 'harris_county', 'jefferson_county', 'kenedy_county', \
                'matagorda_county', 'nueces_county']

#for i in range(0,len(fc_list)):
#    output_fc = os.path.join(r'C:\Users\m3rexmkp\Desktop\Database\re_database_1.gdb', county_names[i], fc_list[i])
#    append_parcels_to_template(fc_list[i], template, county_field_names[i], template_field_names, output_fc)



