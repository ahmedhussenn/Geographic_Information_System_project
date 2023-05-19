import binascii
from PIL import Image,ExifTags
import os
import arcpy

countries=r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\files\ne_10m_admin_0_countries.shp'
points=r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\files\ne_10m_populated_places.shp'
airports=r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\files\ne_10m_airports.shp'
ports=r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\files\ne_10m_ports.shp'
roads=r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\files\ne_10m_roads.shp'
outpath=r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\Output'
arcpy.env.workspace = r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\files'
arcpy.env.overwriteOutput=True


#print data
#Task1
print("Task1: ")
fl=arcpy.ListFeatureClasses()
print("Data sets: ",fl)

#Task2
# countries with military airports
arcpy.MakeFeatureLayer_management(airports,'points_layer',""" "type"='military'""")
arcpy.MakeFeatureLayer_management(countries,'countries_layer')
arcpy.SelectLayerByLocation_management('points_layer','WITHIN','countries_layer',)
arcpy.env.overwriteOutput=True
arcpy.FeatureClassToFeatureClass_conversion('points_layer', outpath, 'countries_with_airport_military')

# Spatially join military airports with countries
output_fc = "C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\Output\military_countries.shp"
# Print shapefile in Pycharm
arcpy.SpatialJoin_analysis('points_layer','countries_layer', output_fc)
print("Task 2: military airports in countries")
with arcpy.da.SearchCursor(output_fc, ["*"]) as cursor:
    for row in cursor:
        print(row)

#Task3
#roads in Asia
arcpy.MakeFeatureLayer_management(roads,'roads_layer',""" "continent"='Asia'""")
arcpy.MakeFeatureLayer_management(countries,'countries_layer')
arcpy.SelectLayerByLocation_management('roads_layer','WITHIN','countries_layer',)
arcpy.env.overwriteOutput=True
arcpy.FeatureClassToFeatureClass_conversion('roads_layer', outpath, '_roads')

# Print Number of roads in Asia
asia_roads = "C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\Output\_roads.shp"
num_Asia_roads = arcpy.GetCount_management(asia_roads)
print("Task 3 :Number of roads in Asia: ", num_Asia_roads)

#Task4
#ports in Italy, Spain, France
arcpy.MakeFeatureLayer_management(ports,'ports_layer')
arcpy.MakeFeatureLayer_management(countries,'countries_layer')
sql_query = "name IN ('Italy', 'Spain', 'France')"
arcpy.SelectLayerByAttribute_management("countries_layer", "NEW_SELECTION", sql_query)

arcpy.SelectLayerByLocation_management('ports_layer','WITHIN','countries_layer',)
arcpy.FeatureClassToFeatureClass_conversion('ports_layer', outpath, 'ports_in_italy_span_france')
arcpy.env.overwriteOutput=True
# Print Number of ports in France,italy and spain
ports_in_countries = "C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\Output\ports_in_italy_span_france.shp"
num_ports_in_countries = arcpy.GetCount_management(ports_in_countries).getOutput(0)
print("Task4: ports in countries France,italy and spain: ", num_ports_in_countries)

#Task6
fields = ['name','location','wikipedia','type']
delimfield = arcpy.AddFieldDelimiters(airports, fields[3])
print ("Task6:the name, location, and Wikipedia page for all airports which are major")
cur = arcpy.da.SearchCursor(airports, fields,delimfield+"='major'" )
# Print the name, location, and Wikipedia page for all airports which are major
for row in cur:
 print ("Name",row[0])
 print ("Location", row[1])
 print ("Wikipedia", row[2])
 print ("type", row[3])

#Task7
print("Task7: ")
arcpy.MakeFeatureLayer_management(roads,'roads_layer')
with arcpy.da.SearchCursor(countries,['FID','INCOME_GRP','SOVEREIGNT','POP_EST','REGION_UN']) as cc:
    for x in cc:
        if x[3] > 25000000 and x[4] == "Africa":
            print x[1]
            print x[2]
            arcpy.MakeFeatureLayer_management(countries, 'countries_layer',""" "FID"={} """.format(x[0]))
            arcpy.SelectLayerByLocation_management('roads_layer', 'WITHIN', 'countries_layer')
            formattedOutputIncome = ' '.join(x[1] .split()[1:])
            formattedOutputname = x[2].replace('(','').replace(')','')
            arcpy.FeatureClassToFeatureClass_conversion('roads_layer', outpath,'Roads_in_{0}_{1}'.format(formattedOutputname,formattedOutputIncome))
            print 'output name {} \n'.format(formattedOutputname)
            print 'output income {} \n'.format(formattedOutputIncome)
print 'Done'


#task 5
countries_file = r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\files\ne_10m_admin_0_countries.shp'
countries_list = ['Algeria', 'Bahrain', 'Comoros', 'Djibouti', 'Egypt', 'Iraq', 'Jordan', 'Kuwait', 'Lebanon', 'Libya', 'Mauritania', 'Morocco', 'Oman', 'Palestine', 'Qatar', 'Saudi Arabia', 'Somalia', 'Sudan', 'Syria', 'Tunisia','Western Sahara', 'United Arab Emirates', 'Yemen']
output_dir = r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\Output';
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
arcpy.env.overwriteOutput = True
output_shapefile = r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\Output\arabic_cites.shp'

if os.path.exists(output_shapefile):
    print("file already exitsts")
else :
    output_shapefile = os.path.join(output_dir, 'arabic_cites.shp')
    arcpy.CreateFeatureclass_management(output_dir, 'arabic_cites.shp', 'POINT')

    for country in countries_list:
     arcpy.MakeFeatureLayer_management(points,"points_layer")
     arcpy.MakeFeatureLayer_management(countries_file, 'countrieslayer', """ "NAME"='{}'""".format(country))
     arcpy.SelectLayerByLocation_management('points_layer', 'WITHIN', 'countrieslayer')
     arcpy.Append_management('points_layer', output_shapefile, 'NO_TEST')

countries_arab =['Algeria', 'Bahrain', 'Comoros', 'Djibouti', 'Egypt', 'Iraq', 'Jordan', 'Kuwait', 'Lebanon', 'Libya', 'Mauritania', 'Morocco', 'Oman', 'Palestine', 'Qatar', 'Saudi Arabia', 'Somalia', 'Sudan', 'Syria', 'Tunisia','Western Sahara', 'United Arab Emirates', 'Yemen']
arcpy.MakeFeatureLayer_management(r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\files\ne_10m_populated_places.shp', 'cities')
selected_fids = []
with arcpy.da.SearchCursor('cities', ['FID', 'SOV0NAME']) as cursor:
    for row in cursor:
        if row[1] in countries_arab:
            selected_fids.append(int(row[0]))

query = """ "FID" IN {} """.format(tuple(selected_fids))
arcpy.MakeFeatureLayer_management(r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\files\ne_10m_populated_places.shp', 'cities', query)
arcpy.FeatureClassToFeatureClass_conversion('cities', r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\Output', 'arabic_cities_if')
#task 5

print("task 11 ")
field_list=arcpy.ListFields(points)
for x in field_list:
    print (x.name+"  "+x.type)


#task 12
field_list = arcpy.ListFields(points)
list_fields = []
for x in field_list:
    list_fields.append(x.name)
for field in list_fields:
    with arcpy.da.UpdateCursor(points, [field]) as city_cursor:
        for x in city_cursor:

            if isinstance(x[0], float) and x[0] == 0.0:

                x[0]=3.3333
                city_cursor.updateRow(x)
            if  x[0] == 0.0:

                x[0] = 3.3333
                city_cursor.updateRow(x)
            if x[0] == ' ':
                x[0] = 'Updated'
                city_cursor.updateRow(x)

#task 12


#task 13 to 16
imagefilepath=r'C:\Users\Ahmed Hussien\PycharmProjects\pythonProject4\Gis_images'
images=os.listdir(imagefilepath)
for image in images:
    print("______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________")
   # print (image)
    path=os.path.join(imagefilepath,image)
    print("Path of image is : "+path)
    print("")
    img=Image.open(path)
    exif={ExifTags.TAGS[k]:v for k,v in img.getexif().items()if k in ExifTags.TAGS}
    print("Exif Tags are :"+str(exif))
    print("")

    image_gps_holder={}

    if(len(exif.keys())>0):
     print ("GPS Info are :")
     for key in exif['GPSInfo'].keys():
      # print (key)
       keytype=ExifTags.GPSTAGS.get(key)
       if(keytype=="GPSVersionID"):
         print(keytype + " code is {}".format(key) + " and have value " + binascii.hexlify(keytype).decode('ascii'))
       else:
          print(keytype+" code is {}".format(key)+" and have value "+str(exif['GPSInfo'][key]))
          image_gps_holder[keytype]=exif['GPSInfo'][key]

     print("")
     latidude = image_gps_holder.get('GPSLatitude')
     longtudide = image_gps_holder.get('GPSLongitude')
     print ("Latitude of image is " + str(latidude))
     print ("Longitude of image is  " + str(longtudide))
     print("")

    else:
     print(path +" is not geotagged")
#task 13 to 16






