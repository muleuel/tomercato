import json
import pymysql

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
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
    
    con = pymysql.connect(host = '127.0.0.1',user = 'root',passwd = 'Muluken!2nega',db = 'tomercato',port =3306)
    cursor = con.cursor()
    for i in range(len(company)):
        #rec = "{" + "company:'" + company[i] + "',sector:'" + sector[i] + "',description:'" + description[i] + "',contact:'" + contact[i] + "',source:'" + source[i]+ "'}"
        #rec = "{" + "company:" + company[i] + ",sector:" + sector[i] + ",description:" + description[i] + ",contact:" + contact[i] + ",source:" + source[i]+ "}"
        #record = eval(rec)
        #row = json.dumps(rec)
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

#names = extract_values(data, 'source')

#print(len(names))
#print(names[0])

all_json = form_new_json(data)
#print(all_json[4741])