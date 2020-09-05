import json
import pymysql

def extract_values(obj, key):
    """find all the keys in the json."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search the JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results
   
#form new json list


def form_new_json(data):
    new_json = []
    company = extract_values(data, 'company')
    sector = extract_values(data, 'sector')
    description = extract_values(data, 'description')
    contact = extract_values(data, 'contact')
    source = extract_values(data, 'source')
    
    con = pymysql.connect(host = '127.0.0.1',user = 'root',passwd = '',db = 'tomercato',port =3306)
    cursor = con.cursor()
    cursor.execute("DROP TABLE IF EXISTS b_info;")
    cursor.execute("CREATE TABLE IF NOT EXISTS b_info (company varchar(2000) , sector varchar(2000) ,description longtext, contact text, source text);")
    for i in range(len(company)):
        
       comp=company[i]
       sect=sector[i]
       desc=description[i]
       cont=contact[i] 
       src =source[i] 
       cursor.execute("INSERT INTO b_info (company,  sector,   description, contact, source) VALUES (%s, %s, %s, %s, %s)", (comp, sect, desc, cont,src))
       rec =  { "company" : company[i] ,
                            "sector" : sector[i] ,
                            "description" : description[i] ,
                            "contact" : contact[i] ,
                            "source" : source[i] }
       row = json.dumps(rec)
       #print(i)                     
       new_json.append( row)
    con.commit()
    con.close()    
    return new_json
   
f = open('TwoMercato.json',)
data = json.load(f)
all_json = form_new_json(data)
#print(all_json[4741])