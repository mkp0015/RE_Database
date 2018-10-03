#####################################################################
#FILE: download_files_from_ftp.py
#AUTHOR: Melinda Pullman
#EMAIL: Melinda.K.Pullman@usace.army.mil
#ORGANIZATION: USACE|SWG
#CREATION DATE: 10/03/2018
#LAST MOD DATE: N/A
#PURPOSE: This script will batch download files from an ftp. An example
#         is provided where all texas county tigerline shapefiles
#         containing all county lines are downloaded from the tigerline's
#         FTP site.
#DEPENDENCIES: urllib, os
#####################################################################

def download_from_ftp(url_path, filenames, outfile_path):

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
    import urllib
    import os

    for f in range(0, len(filenames)):
        filename = os.path.join(url_path, filenames[f])
        local_filename = os.path.join(outfile_path, filenames[f])
        urllib.urlretreive(filename, local_filename)
        ## Fix bug for urllib python 2.7
        urlib.urlcleanup()



## Define Local Varaiables
outfile_path = r'C:\Users\m3rexmkp\Desktop\AddGeocoderFinal'
## Texas State FIPS = 48 - download all files from 48001 -> 48507
year = '2017'
state_county_id = range(48013, 48509,2)
filenames  = ['tl_' + year + '_' + str(state_county_id[i]) + '_edges.zip' for i in range(0, len(state_county_id))]
urlpath = 'ftp://ftp2.census.gov/geo/tiger/TIGER2017/EDGES/'

## Run Function
download_from_FTP(url_path, filenames, outfile_path)


