
import csv    
import math

'''
==========================================
Point A to Point B continuous path finder
==========================================
'''

'''
step 1 : Import csv
step 2 : find first line (latitude,longitude) and last line (latitude,longitude)
step 3 : find the slope ratio by using calculation (first latitude-last latitud2)/(first latitude - last latitude)
step 4 : slope ratio is used to find straight line path
step 5 : find straight line by using slope ratio
step 6 : Split straight line path and out of line 
step 7 : Join out of line to straight line path by changing latitude of out of line to first latitude
step 8 : find distance of all point (lantitude/Longitude)
step 9 : sort the distance and connect the path of point to generate continuous path
step 10 : export the report to export_latitude_longitude_details.csv

'''

class GeoCoordinate:
    def __init__(self):
        pass
    def import_csv(self,csvfilename):
        data = []
        with open('./latitude_longitude_details.csv') as  scraped:
            reader = csv.reader(scraped, delimiter=',')
            row_index=0
            for row in reader:
                row_index += 1
                if row and row_index !=1:
                    
                    columns = [ row[0], row[1]]
                    data.append(columns)
        return data
    def get_first_and_last_point(self,data):
        first_point = data[0]
        last_point = data[-1]
        return first_point,last_point
    def get_lati_long_data(self,point):
        latitude, longitude = (float(point[0]),float(point[1]))
        return latitude,longitude
    def get_slope_ratio(self,from_latitude=None,from_longitude=None,to_latitude=None,to_longitude=None):
        slope_ratio = (from_latitude-to_latitude)/(from_longitude-to_longitude)
        return slope_ratio
    def find_distance(self,from_point=None, to_point=None):
        import math
        R = 6373.0
        lat1 = math.radians(float(from_point[0]))
        lon1 = math.radians(float(from_point[1]))
        lat2 = math.radians(float(to_point[0]))
        lon2 = math.radians(float(to_point[1]))
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance
    def export_geo_path(self,data=None,first_point=None,slope_ratio=None):

        first_latitude,first_longitude = self.get_lati_long_data(first_point)
        approx_slope_line_list = []
        approx_slope_distance = []
        out_of_line_list =[]
        out_of_line_distance =[]
        total_distance_list =[0]
        join_out_of_line_list =[]
        total_distance_coordinates ={}
        total_distance_coordinates.update({0:first_point})
        row_index=0
        for coordinate in data:
            row_index += 1
            
            if coordinate and row_index !=1:
                current_latitude, current_longitude = self.get_lati_long_data(coordinate)
                current_line_ratio = self.get_slope_ratio(first_latitude,first_longitude,current_latitude,current_longitude)
                distance = self.find_distance(first_point,coordinate)
                
                total_distance_coordinates.update({
                    distance:coordinate
                })
                total_distance_list.append(distance)
                if round(slope_ratio,2) == round(current_line_ratio,2):
                    approx_slope_line_list.append(coordinate)
                else:
                    out_of_line_list.append(coordinate)
                
                    join_out_of_line = [first_latitude,current_longitude]
                    join_out_of_line_list.append(join_out_of_line)
                    distance = self.find_distance(first_point,join_out_of_line)
                    total_distance_list.append(distance)
                    total_distance_coordinates.update({
                        distance:join_out_of_line
                    })
        self.export_csv(total_distance_list,total_distance_coordinates)
    def export_csv(self,total_distance_list,total_distance_coordinates):
        header = ['Latitude', 'Longitude','Distance (km)']
        with open('./export_latitude_longitude_details.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)
            # write the data
            
            for total_distance_lst in sorted(total_distance_list):
                if total_distance_lst in total_distance_coordinates:
                    row  =[total_distance_coordinates[total_distance_lst][0],total_distance_coordinates[total_distance_lst][1],total_distance_lst]
                    writer.writerow(row)
if __name__ == "__main__":
    
    geo_coordinate = GeoCoordinate()

    data = geo_coordinate.import_csv('./latitude_longitude_details.csv')

    first_point,last_point = geo_coordinate.get_first_and_last_point(data)

    first_latitude, first_longitude = geo_coordinate.get_lati_long_data(first_point)

    last_latitude, last_longitude = geo_coordinate.get_lati_long_data(last_point)
    
    slope_ratio = geo_coordinate.get_slope_ratio(first_latitude,first_longitude,last_latitude,last_longitude)
    
    geo_coordinate.export_geo_path(data,first_point,slope_ratio)



    
    
    