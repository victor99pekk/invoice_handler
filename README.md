# invoice_handler
invoice handler for "stockholm akut-läkar-grupp" Stockholm emergency physicians. Combines and sort invoices in excel format using python

This is a program used to compile 7 separate files (.xls), from a folder with an arbitrary amount of input files (.xls). 5 of the files are is data associated with 5 different places. one of the files is data associated with kriminalvården, and the last one is invalid data that needs to be corrected manually.

The five places are: (Norrtälje, Södertälje, Syd, City, Nord) 

- Syd includes Flemingsberg, Nacka, flempan, söderort, syd, Stockholm syd and Västberga.

- Nord includes Sollentuna, Solna, norrort, and Tegen.

- City: Södermalm, Östermalm, Norrmalm

The program can be seen as a function (F) that takes in a folder with files and ouputs a folder with 7 output files.

	folder_input = [file_1, file_2, ..., file_N]
	F(folder) = application
	folder_output = [syd, nord, city, södertälje, norrtälje, misnamed, kvv]
	
	folder_input -> F(folder) -> folder_ouput
