import arcpy, os,pandas as pd
from arcpy import env  
from arcpy.sa import *
import datetime

directory = "C:/Ocean-2019/variables/14rainfall/"
lon="long"
lat="lat"
var="var"
teste = "teste"
arcpy.env.overwriteOutput = True
barrios="D:/data/aoi/shapes/Barrios.shp"
barrios_diss="D:/data/aoi/shapes/barrios_diss.shp"
concat_df_B = pd.DataFrame()
concat_df_P = pd.DataFrame()

for filename in os.listdir(directory+"raw_data/"):
  if filename.endswith("tif"):
    try:
        arquivo = filename[23:31]
        print arquivo
        ExtractValuesToPoints("D:/aoi/Points_ID.shp", directory+"raw_data/"+filename,"C:/Ocean-2019/variables/14rainfall/shape/"+arquivo+"_points.shp")
  
        arcpy.Clip_management(directory+"raw_data/"+filename,"-75,192131 -46,382992 -72,235513 -41,352593","C:/Ocean-2019/variables/14rainfall/raster/"+arquivo+".tif", "#", "#", "NONE", "NO_MAINTAIN_EXTENT")

        arcpy.RasterToPoint_conversion("C:/Ocean-2019/variables/14rainfall/raster/"+arquivo+".tif","C:/Ocean-2019/variables/14rainfall/shape/"+arquivo+"_P" , "VALUE")
#_____________________________________________________            
        slopes = "C:/Ocean-2019/variables/14rainfall/shape/"+arquivo+"_P.shp"
        barrioX = r'D:\aoi\shapes\Barrios.shp'
        outfc = "C:/Ocean-2019/variables/14rainfall/barrios/"+arquivo+"_S"
        #create the field map
        myMap = arcpy.FieldMappings()
        myMap.addTable(barrioX)
        myMap.addTable(slopes)
        fIndex = myMap.findFieldMapIndex("grid_code")

        #create new field map with the "GRID_CODE" field
        NewFieldMap = myMap.getFieldMap(fIndex)

        #set the merge rule
        NewFieldMap.mergeRule = 'Mean'

        myMap.replaceFieldMap(fIndex,NewFieldMap)

        arcpy.SpatialJoin_analysis(barrioX, slopes, outfc, "JOIN_ONE_TO_ONE", "", myMap, "CONTAINS")
#_____________________________________________________
        arcpy.TableToTable_conversion( "C:/Ocean-2019/variables/14rainfall/barrios/"+filename[23:31]+"_S.dbf", "C:/Ocean-2019/variables/14rainfall/semi-final/", "B"+filename[23:31]+".csv")
        arcpy.TableToTable_conversion("C:/Ocean-2019/variables/14rainfall/shape/"+arquivo+"_P.dbf", "C:/Ocean-2019/variables/14rainfall/semi-final/", "P"+filename[23:31]+".csv")
        data = filename[23:31]
        d2= datetime.datetime.strptime(str(data), "%Y%m%d").strftime("%d/%m/%Y")
        csv_B = "C:/Ocean-2019/variables/14rainfall/semi-final/B"+filename[23:31]+".csv"
        
        df_B = pd.read_csv(csv_B,sep=";")
        
        #df_B.drop
        df_B.drop(['Join_Count'],axis=1,inplace=True)
        df_B.drop(['TARGET_FID'],axis=1,inplace=True)
        df_B.drop(['OID'],axis=1,inplace=True)
        df_B.drop(['pointid'],axis=1,inplace=True)
        #df_B.drop(['Code'],axis=1,inplace=True)
        #df_B.drop(['Des'],axis=1,inplace=True)
        #df_B.drop(['Long'],axis=1,inplace=True)
        #df_B.drop(['Lat'],axis=1,inplace=True)
        #df_B.drop(['Raster'],axis=1,inplace=True)
        df_B['data'] = d2
       # df_B2 = df_B.loc[df_B['RASTERVALU'] !=  0]
        #print df_B2
        concat_df_B = pd.concat([concat_df_B, df_B])

        csv_P = "C:/Ocean-2019/variables/14rainfall/semi-final/P"+filename[23:31]+".csv"
        df_P = pd.read_csv(csv_P,sep=";")
        
        df_P['data']=d2
        #df_P.drop(['Des'],axis=1,inplace=True)
        #df_P.drop(['Code'],axis=1,inplace=True)
        df_P.drop(['OID'],axis=1,inplace=True)
       # df_P.drop(['Long'],axis=1,inplace=True)
       # df_P.drop(['Lat'],axis=1,inplace=True)
       # df_P.drop(['Raster'],axis=1,inplace=True)
       # print df_P
        concat_df_P = pd.concat([concat_df_P, df_P])
       
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print "file "+arquivo +" processed at "+st    
    except:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print "file "+arquivo +"not processed at "+st
        continue
concat_df_B.to_csv("C:/Ocean-2019/variables/14rainfall/Barrios_1718.csv")
concat_df_P.to_csv("C:/Ocean-2019/variables/14rainfall/Points_1718.csv")
