import csv 
import enquiries
import os
def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


def import_csv(csvfilename=""):
    data = []
    with open('./export_latitude_longitude_details.csv') as  scraped:
        reader = csv.reader(scraped, delimiter=',')
        row_index=0
        for row in reader:
            row_index += 1
            if row and row_index !=1:
                
                columns = [ row[0], row[1],row[2]]
                data.append(columns)
    return data
def get_tarrain():
   data ={
       'boundary wall,road': 0,
       'road':0.5,
      'river side': 1.5,
       'civil station, road': 3

   } 
   return data        
if __name__ == "__main__":
    from dotenv import load_dotenv
    from pathlib import Path
    dotenv_path = Path('./.env')
    load_dotenv(dotenv_path=dotenv_path)

    lat1 = 10.0069921 
    lon1 = 76.3735699
    R = 6378.1 #Radius of the Earth
    brng = 1.57 #Bearing is 90 degrees converted to radians.

    

    import mysql.connector

    mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
    )
    mycursor = mydb.cursor()
    mycursor.execute(

        '''
        DROP TABLE IF EXISTS `geo_locations`;
        '''
    )
    print('<================Drop geo locations=======================> \n\n')
    mycursor.execute(

        '''
        CREATE TABLE `geo_locations` (
        `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
        `latitude` FLOAT( 10, 6 ) NOT NULL ,
        `longitude` FLOAT( 10, 6 ) NOT NULL,
        `distance` FLOAT( 10, 6 ) NOT NULL
        ) ENGINE = MYISAM ;
        '''
    )
    print('<================Create Table geo_locations=======================> \n\n')
    data = import_csv()
    for dat in progressBar(data, prefix = 'Insert Progress:', suffix = 'Insert Complete', length = 50):
        mycursor.execute(

            f'''
            INSERT INTO `geo_locations` (`latitude`, `longitude`, `distance`) 
            VALUES 
            ({dat[0]},{dat[1]},{dat[2]});
            '''
        )
    
    print('<================insert table complete=======================> \n\n')

    data = get_tarrain()

    options = list(data.keys())

    choice = enquiries.choose(f'Choose one of these finding terrain by starting point latitude {lat1} and longitude {lon1} : ', options)
    d = data[choice]

    query = f'''


    SELECT latitude,longitude FROM `geo_locations` WHERE `distance` = 0 

    '''

    mycursor.execute(query)

    myresult = mycursor.fetchone()
    lat1 = myresult[0] 
    lon1 = myresult[1]

    
    query = f'''


    SELECT 

        DEGREES(ASIN(
            SIN(RADIANS({lat1}))*COS({d}/{R})+COS(RADIANS({lat1}))*SIN({d}/{R})*COS({brng})
        )) as lat2,
        DEGREES(RADIANS({lon1}) + ATAN2(
            SIN({brng})*SIN({d}/{R})*COS({lat1}),
            COS({d}/{R})-SIN(RADIANS({lat1}))*SIN(RADIANS(
                DEGREES(ASIN(
                    SIN(RADIANS({lat1}))*COS({d}/{R})+COS(RADIANS({lat1}))*SIN({d}/{R})*COS({brng})
                ))



            ))
        )) as lon2
        FROM  geo_locations 

    '''

    mycursor.execute(query)

    myresult = mycursor.fetchone()
    if myresult:
        latitude = myresult[0]
        longitude = myresult[1]
        print(
        f''' 
        
        Start from latitude {lat1} and longitude {lon1} \n
        Bearing is 90 degrees converted to radians \n
        distance {d} KM \n
        To latitude {latitude} \n
        To longitude {longitude}
        ''')
    mydb.close()



    
    
    