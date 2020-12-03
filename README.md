# AIMS_PDF_Python
Code to easily create a pdf integrating all your values, tables and figures in VUB-AIMS format during coding

## Template
The code in `template.py` will offer you all tools you need to create your pdf. 
Running that code will result in the [My_Project.pdf]("https://github.com/Sdniss/AIMS_PDF_Python/My_Project.pdf") that you can find in the repo.

A few small mentions for the code:
1. `pdf = PDF('Author', 'My Project')` will initiate the PDF automatically with a title page
2. Use `.write_text()` instead of the built-in function `.write()` so you do not have to specify the line height every time.
