# Pbit Dataset Finder!

## Table of contents:

## Description:
The goal of this project was to find in which PowerBi reports (with the extension **Pbit**), certain words would appear. The words correspond to the Dataset that is desired to be found simbolizing that a certain dataset is being used by the report in question. This could have been much simplified, but the goal was to use implementing something and learn in the process :stuck_out_tongue:, with something that was originally tasked to do, in this case using docker and mongodb.

**Note:** The conversion from Pbix to Pbit needs to be done manually unfortunately.

---

### How it works:

The python main.py file, follows the following logic:

- Extraction from the "Reports" folder, the file called "DataModel" that is present in any report and stores it in the "Extract" folder
- It then converts that same file into a valid json and stores it in the "JsonConverted" Folder 
- After that, it tries to insert into a collection on MongoDB, in case the connection is live, otherwise it will store the results in the "Output" folder.

The last step was to be able to run the python code without the need of MongoDB since it's not really a requirement. Nonetheless, the pymongo would still need to be ran from the command line, in order to make it work.

---

### Requirements:
1. Copy the .pbit files to the Reports folders.

2. Change the elements.txt file with the words you want to be found. The text file is displayed inside the following folder structure:
```
.
│    
└───app
    └───Scripts
        │   elements.txt
```

#### Without Docker

From the root directory of the project:

```
pip install -r ./app/requirements.txt 
```
And then
 ```
 python ./app/Scripts/main.py
```

#### With Docker Installed

After performing the two steps listed in the Requirements section, just run the following command to build the image and run the containers.
```
docker-compose -f ./docker.yaml up -d 
```
To check on the results, access the url: [MongoDB](http://localhost:8080).  
When prompted for credentials, use the following: 
 - User: admin
 - Pass: pass

This can be changed in the yaml file of the project.

---

### Conclusion
This project allowed to automate the tedious task of checking the data source of the PowerBI reports by making the process of extraction of the metadata, conversion into JSON file, checking the data source and saving the results more efficient and effective.

