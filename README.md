# invoice_handler
- Invoice handler for "stockholm akut-läkargrupp" Stockholm emergency physicians. The program combines and sorts invoices in excel format using python, pandas and libraries used to handle excel files.

This is a program used to compile a folder with 7 different output-files (.xlsx), from an input-folder with an arbitrary amount of input files (.xls/xlsx). 

## Input data
the input to the program is a folder with an arbitrary amount of files. The files are in .xls or .xlsx format. Each Doctor sends in their work for the month in an excel file. The data is structured in the following way:

Every row represents a patient visit. It is these patient visits that are to be sorted into the 7 output-files, depending on where in stockholm they have occured. 

### Example of one input-file from the input folder:
![](images/input_example.png)


## Output data


5 of the output-files are associated with 5 different districts in stockholm. Of the 2 remaining output-files, one is data associated with `misnamed rows`, and the last one is filled with `dropped rows`.

### Misnamed rows (output)
`misnamed rows` are rows occurr when the input data is not structured as expected. This could be due to a misspelling of a district/type-of-service name, or a district/type-of-service name that is not recognized. Or invalid date/time formats.
![](images/misnamed_example.png)

### Dropped rows (output)
`dropped rows` are rows that dont contain a district or dont contain a typ-of-service. These rows are not treated by the program, but saved in the output file `dropped rows`, for manual inspection if needed.

### district output-files
The five Districts are: (Norrtälje, Södertälje, Syd, City, Nord) each district contain several places in Stockholm. The places are:

- `Syd`: Flemingsberg, Nacka, flempan, söderort, syd, Stockholm syd and Västberga.

- `Nord`: Sollentuna, Solna, norrort, and Tegen.

- `City`: Södermalm, Östermalm, Norrmalm
- `Södertälje`: Södertälje
- `Norrtälje`: Norrtälje

Different people might have put in the data in different ways, so the program is designed to convert the different ways of writing the input data to one way.
  
### Example of output-file related to City:
![](images/city_example.png)


## How the program works
The program can be seen as a function (F) that takes the input-folder of files (to be sorted) and outputs a folder with 7 output sorted files.

	folder_input = [file_1, file_2, ..., file_N]
	F(input) = application
	folder_output = [syd, nord, city, södertälje, norrtälje, misnamed, kvv]
	
	F(input_folder) = folder_ouput

## User interface
<div style="display: flex; align-items: center; justify-content: space-between;">
    <div style="flex: 1;">
        The program is designed to be used by people with no programming experience. The user interface is a simple GUI that allows the user to select the input-folder and output-folder. The interface contain simple instructions on how to use the program in swedish. The instructions and other features of the gui change along the way to make it possible for a first time user to use the program without any prior knowledge.
    </div>
    <div style="flex: 0 0 auto; margin-left: 20px;">
        <img src="images/gui.png" alt="User Interface" style="width: 200px; height: auto;">
    </div>
</div>


## 2 GUI reactions
(translation in red)

### Failed run
<div style="display: flex; align-items: flex-start; justify-content: space-between;">
    <div style="flex: 1;">
        chosen input folder correctly, but forgotten to name the output folder. The program will give an error message and ask the user to name the output-folder.
    </div>
    <div style="flex: 0 0 auto; margin-left: 20px;">
        <img src="images/failed_run.png" alt="Failed Run" style="width: 200px; height: auto;">
    </div>
</div>

### Successful run
<div style="display: flex; align-items: flex-start; justify-content: space-between;">
    <div style="flex: 1;">
        The program has successfully sorted the input files and saved the output files in the output folder. The user is given a message that the program has finished and where it is possible to find the output files.
    </div>
    <div style="flex: 0 0 auto; margin-left: 20px;">
        <img src="images/success_run.png" alt="Successful Run" style="width: 200px; height: auto;">
    </div>
</div>

the gui does also let you know if you've put in files that have to incorrect format (not .xls/.xlsx) and more.