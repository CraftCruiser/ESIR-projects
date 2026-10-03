import csv
import json

class File():

    """
    Class permettant de gérer les maps (sauvegarder, créer, modifier ...)
    """    
    #___/ IMPORT/EXPORT, fichier json/csv\____

    #-/JSON\-
    def import_json(path):
        """
        Permet d'importer des données d'un fichier json
        """
        with open(path, 'r') as file:
            data = json.load(file)
        return data

    def export_json(path,data):
        """
        Permet d'exporter des données vers un fichier json
        """
        with open(path, 'w') as file:
            json.dump(data,file,indent=4)


    def change_json(path,key,value):
        """
        Permet de changer des valeurs d'un fichier json
        """
        data = File.import_json(path)
        data[key] = value
        File.export_json(path,data)
    
    #-/CSV\-
    def import_csv(path):
        """
        Permet de convertir un csv en liste de liste
        """
        with open(path, 'r', newline='') as file:
            reader = csv.reader(file)
            data = [list(row) for row in reader]
        return data
    
    def export_csv(path,data):
        """
        Permet d'exporter une liste de liste en csv
        """
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)