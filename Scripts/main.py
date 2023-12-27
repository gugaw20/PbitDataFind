# Package Imports
import subprocess, sys
import os
from os import listdir
from os.path import isfile, join
from zipfile import ZipFile
import json

# Files Imports
import InOut


def extracts(targetDirectory):

    reportsDirectory = os.path.join(targetDirectory, "Reports")
    extractDirectory = os.path.join(targetDirectory, "Extract")
    failed_reports = []

    files = InOut.allFiles(reportsDirectory)

    for file in files:
        filename = file.split('.')[0]

        try:
            with ZipFile(os.path.join(reportsDirectory, file), 'r') as zObject:  
                zObject.extract("DataModelSchema", path=f"{extractDirectory}") 
            zObject.close()

            os.rename(os.path.join(extractDirectory, "DataModelSchema"), os.path.join(extractDirectory, f"{filename}"))

        except KeyError:
            failed_reports.append(file)
    
    if len(failed_reports) > 0:
        fileFullPath = os.path.join(targetDirectory, "Output", "results_bad.txt")

        # Clear Text File
        InOut.clearTextFile(fileFullPath)

        # Save to Text File
        InOut.saveResults(fileFullPath, failed_reports)

    return


def JsonConverted(targetDirectory):

    extractDirectory = os.path.join(targetDirectory, "Extract")
    jsonDirectory = os.path.join(targetDirectory, "JsonConverted/")
    powershell_script = './Scripts/JsonConvert.ps1'

    files = InOut.allFiles(extractDirectory)

    for file in files:
        # PowerShell
        subprocess.run(["powershell.exe", "-File", powershell_script, 
                        extractDirectory + file, jsonDirectory + file + ".json"], 
                        stdout=sys.stdout)

    return


def finder(targetDirectory, elementToFind):

    # Read Json
    results = []

    jsonDirectory = os.path.join(targetDirectory, "JsonConverted")
    files = InOut.allFiles(jsonDirectory)

    for file in files:
        with open(f"{jsonDirectory + file}", "rb") as f:
            data = json.load(f)
    
        for dataset in data.get("model").get("tables"):
        
            filtered_data = dataset.get("partitions")[0].get("source").get("expression")[1]
            res = [ele for ele in elementToFind if(ele in filtered_data)]
            
            if res:
                results.append([f"Element: {res}", f"Report: {file}"])
                break
    
    if len(results) > 0:
        fileFullPath = os.path.join(targetDirectory, "Output", "results.txt")

        # Clear Text File
        InOut.clearTextFile(fileFullPath)

        # Save to Text File
        InOut.saveResults(fileFullPath, results)

    return


if __name__ == "__main__":

    # Working Directory
    targetDirectory = os.getcwd()

    # Step 1: Verify Folders
    InOut.existsFolder(targetDirectory, "data")

    folders = ['Extract', 'JsonConverted', 'Output']
    for folder in folders:
        targetDirectory = os.path.join(targetDirectory, "data")
        InOut.existsFolder(targetDirectory, folder)

    # Step 2: Unzip Report
    extracts(targetDirectory)
    
    # Step 3: Convert to Json
    JsonConverted(targetDirectory)
    
    # Step 4: Report find Dataset
    elements = ["Sprint", "Issues", "Dog"]
    finder(targetDirectory, elements)
    
