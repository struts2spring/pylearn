# Introduction

Excel is ubiquitous. Many software projects originate from some company or process overgrowing the Excel spreadsheets that were being employed to manage it. As application developers, more than once we’ve had to reverse-engineer Excel files and translate them into a software application.

Excel is also quite common as an export format for data, and sometimes also as an input format. And while Excel is not by any means a domain-specific language, we can sometimes consider it as part of the “notation” that some domain experts use to formalize their problems. Thus, software that can “speak” Excel is often closer to its users. Even when the long-term objective is to convert them to an application or to a domain-specific language (DSL), it’s often a good idea to provide an automated migration path from Excel, as well as borrowing notation from Excel.

For example, an application could consume existing Excel files that people use to exchange among themselves as part of the project, effectively gaining the ability to “speak the same language” as the users. Or, it could produce a spreadsheet as the output of some query or calculation, because some users may want to further expand on it to compile a report with additional charts and formulas.

In this tutorial, we’ll explore working with Excel spreadsheets in Python, using the openpyxl library and other tools. In particular, we’ll learn how to:

    Process Excel files as input, with various methods to access the data in them;
    Evaluate formulas;
    Write Excel files as output.

Note: here, we’re talking about “modern” (2010) XML-based Excel files only, that have a .xlsx extension. Openpyxl does not support legacy binary Excel files (.xls). There are other solutions for that that we won’t explore in this tutorial.

All the sample code shown in this tutorial is available in our GitHub repository.
# Setup

In the following, we assume a UNIX-like environment – Linux, OSX, or WSL, the Windows Substrate for Linux. As the first step, we’ll create a directory to hold our project:
mkdir python-excel
cd python-excel

Alternatively, if we plan to push our code on GitHub, we may create a repository on GitHub first, and clone it on our local machine:
git clone <repo-url> python-excel
cd python-excel

This will give us the option to have GitHub generate a .gitignore file for Python, a README file, and a license file for us.

After we’ve created the project root directory, we can use pip to install openpyxl. We may want to set a virtual environment up so that we don’t pollute our system’s Python installation:
```shell
python -m venv .venv
source .venv/bin/activate
```

Having activated the environment, we should see it reflected in our shell prompt, like this:
(.venv) python-excel (main*) »

We’ll then write a requirements.txt file that lists our dependencies:
echo openpyxl > requirements.txt

Even if we only have a single dependency right now, explicitly listing it in a file that can be interpreted by the machine will make it easier for other developers to work on our project – including a future version of ourselves that has long forgotten about it.

Then, we’ll install the required dependencies with pip:
python -m pip install -r requirements.txt

We can also easily automate these steps in our CI pipeline, such as GitHub actions.
# Loading an Excel File

In Openpyxl, an Excel file is called a “workbook” and is represented by an instance of the class openpyxl.workbook.Workbook. Opening one is super easy:
wb = load_workbook(path)
A glimpse into the results of calling load_workbook

Openpyxl opens workbooks for reading and for writing at the same time unless we specify that we want a read-only workbook with read_only=True as an argument to load_workbook.

When we finish working with an Excel file, we have to close it:
wb.close()

Unfortunately, a Workbook is not a “context manager”, so we cannot use Python’s with statement to automatically close it when we’re done. Instead, we have to manually arrange to close it even in case of exceptions:
wb = load_workbook(path)
try:
    # Use wb...
finally:
    wb.close()
# Processing an Excel File – Common Cases

In general, workbooks may contain multiple sheets, so in order to access the data in an Excel file, we first need to choose a sheet to work on.

Later on, we’ll see how to process multiple worksheets, but for now, we’ll assume that the data that we’re interested in is in the active sheet – the one that the user will see when they open the file in their spreadsheet application:
sheet = wb.active

This is quite often the only sheet in the document, actually.

Now that we have a sheet, we can access the data in its cells in several ways.
Iterating over rows. We can process the data one row at a time, using a Pythonic generator:
for row in sheet.rows():
    # Do something with the row

The rows that rows() yields are themselves generators, and we can iterate through them:
for row in sheet.rows():
    for cell in row:
        # Do something with the cell

Or we can access them by index:
for row in sheet.rows():
    header = row[2]

Actually, the sheet itself is iterable in row order, so we can omit rows altogether:
for row in sheet:
    pass

Iterating over columns. Similarly, we can iterate by column using the cols method:
for col in sheet.cols():
    # Use the column

Columns work the same as rows: they are themselves iterable and addressable by index.

Accessing cells by address. If we need a piece of data that is in one specific cell, we don’t need to iterate through the whole sheet until we encounter it; we can use Excel-style coordinates to access the cell:
cell = sheet['C5']

We can also obtain a generator for a row, column, or a range of cells; we’ll show that in a later section.
# Processing Cells

In any case, to process the data in a spreadsheet we have to deal with individual cells. In Openpyxl, a cell has a value and a bunch of other information that is mostly interesting only for writing, such as style information.

Conveniently, we work with cell values as Python objects (numbers, dates, strings, and so on) as Openpyxl will translate them to Excel types and back appropriately. So, cell contents are not restricted to be strings. Here, for example, we read the contents of a cell as a number:
tax_percentage = sheet['H16'].value
tax_amount = taxable_amount * tax_percentage

However, we have no guarantee that the user actually put a number in that cell; if it contains the string “bug”, in the lucky case, we’ll get a runtime error when we run the code above:
TypeError: can't multiply sequence by non-int of type 'float'

However, in the not-so-lucky case, i.e. when taxable_amount is an integer – as it should be, since we’re dealing with money in the example – we’ll get a long string of “bug” repeated taxable_amount times. That’s because Python overloads the * operator for strings and integers to mean “repeat the string n times”. This will potentially result in further type errors down the line, or in a memory error when Python cannot allocate such a big string.
Therefore, we should always validate the input to our program, including Excel files. In this particular case, we can check the type of the value of a cell with Python’s isinstance function:
if isinstance(cell.value, numbers.Number):
    # Use the value

Or we can ask the cell for which type of data it contains:
if cell.data_type == TYPE_NUMERIC:
    # Use the numeric value
# Advanced Addressing of Cells

So far, we’ve explored the simplest, most straightforward ways of accessing cells. However, that doesn’t cover all the use cases that we may encounter; let’s have a look at more complex access schemes.

Sheets other than the active one. We can obtain sheets by access them by name from the workbook:
sheet = wb['2020 Report']

Then we can access cells in the sheet as we’ve seen earlier.

Ranges of cells. We’re not limited to addressing cells one by one – we can also obtain cell ranges:

    sheet['D']
    is a whole row (D in this case)
    sheet[7]
    is a whole column (7 in this case)
    sheet['B:F']
    represents a range of rows
    sheet['4:10']
    represents a range of columns
    sheet['C3:H5']
    is the most versatile option, representing an arbitrary range of cells.

In any of the above cases, the result is an iterable of all the cells, in row order (except when the range represents one or more columns, in which case, cells are arranged in column order):
for cell in sheet['B2:F10']:
    # B2, B3, ..., F1, F2, ..., F10
for cell in sheet['4:10']:
    # A4, B4, ..., A10, B10, ... 
for cell in sheet['B2:F10']
for cell in sheet['4:10']
# Cell Iterators

If the above addressing schemes don’t suit our problem, we can resort to the lower-level methods iter_rows and iter_columns, that return generators – respectively by row and by column – over a range of cells.

In particular, both methods take 5 named parameters:

    min_row – the number of the starting row (1 is A, 2 is B, etc.)
    min_col – the starting column
    max_row – the number of the last row
    max_col – the last column
    values_only – if true, the generator will yield only the value of each cell, rather than the entire cell object. So, we won’t have to spell cell.value
    , just value
    . On the other hand, we won’t have access to the other properties of the cell, such as its data_type.

So, for example, if we want to iterate over the range B2:F10 by column we’ll write:
for cell in sheet.iter_columns(min_row=2, min_col=2, max_row=6, max_col=10):
    # Use the cell
# Writing an Excel File

To write an Excel file, we just call the save method on our workbook:
wb.save('someFile.xlsx')

There’s not much to say about that. It’s more interesting to know how to modify a workbook before saving it. This can be a workbook that has been loaded from a file or a brand new workbook created in Python with the new operator.
# Modifying Individual Cells

We can alter the value of a cell simply by assigning to it:
cell.value = 42

Note that this will automatically update the cell’s data type to reflect the new value. Besides the obvious primitive types (integer, float, string), the available types include various classes in the datetime module, as well as NumPy numeric types if NumPy is installed.

Not just values and types, we can set other properties of cells, notably style information (font, color, …), which is useful if we’re set on producing a good-looking report. The documentation of Openpyxl contains a thorough explanation of working with styles so we’ll just refer to that.
# Adding and Removing Sheets

So far we’ve seen that we can address some objects – particularly workbooks and worksheets – as if they were dictionaries, to access their components: worksheets, rows, columns, individual cells, cell ranges. We’ll now see how we can add new information to the dictionaries and how to replace existing information. We’ll start with sheets.

To create a worksheet, we use the create_sheet method on a workbook:
new_sheet = wb.create_sheet()

This will add a new sheet to the workbook, after the other sheets, and will return it. We can also give it a title:
new_sheet = wb.create_sheet(title = 'My new sheet')

If we want to place the sheet at another position in the list, we can specify its index (which is zero-based, zero being the first):
# The new sheet will be inserted as the third sheet
new_sheet = wb.create_sheet(index = 2)

To delete a sheet, instead, we have two options. We can delete it by name in accordance with the dictionary abstraction:
del wb['My sheet']

We can check if a sheet with a given name is present in the workbook using the in operator:
name = 'My sheet'
if name in workbook:
    del workbook[name]

Alternatively, we can call the remove method with the sheet as the argument:
wb.remove(sheet)
# Adding and Removing Rows, Columns, and Cells

Similarly, we have methods for adding or removing rows, columns, or individual cells in a worksheet. Let’s see some examples.

First and foremost, by simply accessing a cell, we cause the creation of all rows and columns needed to make room for it:
wb = Workbook()
# Initially, an empty worksheet has a single row and column, A and 1
self.assertEqual(wb.active.max_row, 1)
self.assertEqual(wb.active.max_column, 1)
# We set the value of the cell at C3; 
# openpyxl creates rows B, C and columns 2, 3 automatically
wb.active['C3'].value = 12
# Now the sheet has 3 rows and columns
self.assertEqual(wb.active.max_row, 3)
self.assertEqual(wb.active.max_column, 3)
wb.close()

Additionally, we can use the insert_rows and insert_cols methods to add rows or columns in the middle of the sheet. Existing cells are automatically moved after the newly inserted rows/columns:
wb = Workbook()
self.assertEqual(wb.active.max_row, 1)
wb.active['A1'].value = 11
# Insert 3 rows, starting at index 0 (i.e. row 1)
wb.active.insert_rows(0, 3)
self.assertEqual(wb.active.max_row, 4)
# Note how the cell, A1, has automatically moved by 3 rows to A4
self.assertEqual(wb.active['A4'].value, 11)

We have the corresponding delete_rows and delete_cols to remove rows/columns instead:
# Delete 2 columns, starting from index 1, i.e. column B
sheet.delete_columns(1, 2)
# Working With Formulas

Spreadsheets are powerful because they support formulas to compute cell values. Calculated cells automatically update their value when other cells change. Let’s see how we can work with formulas in Openpyxl.

First of all, we can ignore formulas altogether if we just want to read an Excel file. In that case, opening it in “data only” mode will hide formulas, presenting all cells with a concrete value – as computed the last time Excel opened the file:
wb = load_workbook(filename, data_only=True)

Only when modifying an Excel file we may want to recalculate formulas. While openpyxl has some support for parsing formulas, that we could use to analyze them (e.g., to check if they’re only calling known functions), it doesn’t know how to evaluate formulas by itself. So, we have to resort to a third-party library if we want to compute formulas.

Enter the library called, well, “formulas”. Let’s add it to our requirements.txt file and install it:
$ cat requirements.txt
openpyxl
formulas
pip install -r requirements.txt

With the formulas library, we have two options:

    calculating the values of all the formulas in a workbook, recursively following dependencies, the way Excel does it;
    compiling individual formulas to Python functions that we can then invoke with different arguments.

# Calculating the Values of All Formulas

The first use case is not the most interesting in the context of this tutorial because it overlaps with the data_only approach we’ve seen earlier. In fact, in that mode, we cannot load a workbook, modify it, and then recompute the formulas in it. We’d have to:

    save the modified workbook to a file;
    have formulas load the file again;
    calculate formula values with an API call;
    save the file with the calculated values;
    open the file with openpyxl in data_only mode and finally see the computed values.

Not really efficient use of developer and computer time!

That said, this feature of the formulas library does have its value, because it supports some advanced use cases:

    Calculating formulas across multiple workbooks. In Excel, it’s possible to have a formula refer to another file. formulas can load multiple workbooks as part of the same set so as to resolve these cross-file references, which is a pretty rarely used feature of Excel that, e.g., Apple’s Numbers doesn’t support.
    Compiling an entire Excel workbook into a Python function. We can define certain cells as input cells, others as output cells, and obtain a function that, given the inputs, computes the formulas in the workbook and returns the values it finds in the output cells after the calculation.

However, to keep it simple, we’ll leave those out of this tutorial.
# Compiling Individual Formulas as Python Functions

Let’s concentrate on individual formulas, that we can better integrate with our work based on openpyxl. As per formulas’ documentation, the incantation for compiling an Excel formula into a Python function is the following:
func = formulas.Parser().ast(value)[1].compile()

Note the [1]
there – for some reason, the ast method returns a tuple of two objects of which the second, the builder, is the most useful. Even though this is documented, apparently it’s a piece of internal API that would need to be wrapped in a more user-friendly interface.

Anyway, when we evaluate the code above, the resulting func will be a function with as many arguments as the inputs of the formula:
func = formulas.Parser().ast('=A1+B1')[1].compile()
func(1, 2) == 3 # True
# Handling Dependencies of Formulas

So, we can compile the formula of a single cell into a function. However, what happens when the formula depends on other cells that contain formulas themselves? The formulas library doesn’t help us in that regard; we have to compute all the inputs recursively if they are themselves formulas. Let’s see how we might do that.

First of all, how do we distinguish between a cell with a formula and a cell with a regular value? Openpyxl doesn’t offer a method to do that, so we have to check if the value of the cell starts with an equal character:
def has_formula(cell: Cell)
   return isinstance(cell.value, str) and cell.value.startswith('=')

Therefore, we know how to compute the values of cells that don’t contain formulas:
def compute_cell_value(cell: Cell):
   if not has_formula(cell):
       return cell.value

Now, the interesting thing is how to compute the value when the cell does contain a formula:
func = formulas.Parser().ast(cell.value)[1].compile()
args = []
# TODO: compute function arguments
return func(*args)

We compile the formula into a Python function and then we invoke it on its inputs. Since the inputs are references to cells, we recursively invoke compute_cell_value in order to get their values:
sheet = cell.parent
for key in func.inputs.keys():
   args.append(compute_cell_value(sheet[key]))

We leverage the fact that every cell keeps a reference to its parent, i.e., the sheet that contains it. We also make use of introspection information retained by formulas, that allows us to inspect the inputs of a function – a dictionary of cell references.

Note that this doesn’t support references across sheets or, for that matter, files.
# Computing Formulas Over Cell Ranges

So far, our compute_cell_value function successfully computes the values of cells without formulas and with formulas that may depend on other cells. However, what about formulas that depend, not on individual cells, but on cell ranges?

Well, in that case, the input of a function is a range expression, such as A1:Z1 in =SUM(A1:Z1)
. When we call compute_cell_value recursively, we pass it the following:
sheet[key]

When the key is the address of a single cell, we obtain a cell object; but when it refers to a range of cells, we obtain a tuple with one entry per cell. Our compute_cell_value doesn’t know how to deal with such input, so we have to modify it to handle that case:
if isinstance(input, Tuple):
   return tuple(map(compute_cell_value, input))

Then, the complete version of the function becomes:
def compute_cell_value(input: Union[Cell, Tuple]):
   if isinstance(input, Tuple):
       return tuple(map(compute_cell_value, input))
   if not has_formula(input):
       return input.value
   func = formulas.Parser().ast(input.value)[1].compile()
   args = []
   sheet = input.parent
   for key in func.inputs.keys():
       args.append(compute_cell_value(sheet[key]))
   return func(*args)
 Adding New Formula Functions

formulas supports many built-in Excel functions, but not all of them. And of course it doesn’t know about user-defined functions in VBA. However, we can register new Python functions with it so that they can be called in formulas:
def is_number(number):
   ... # This is actually defined in formulas, but strangely not exposed as the Excel function
FUNCTIONS = formulas.get_functions()
FUNCTIONS['ISNUMBER'] = is_number

Simple as that. The inputs to the function are its actual arguments as native Python values, so strings, numbers, dates, etc. – not instances of the Cell class.

Also, compared to a regular Python function, we have to guard against XlError, which represents errors in calculations such as #DIV/0! or #REF! (we typically see those in Excel when we’ve made some mistake in writing a formula):
def is_number(number):
    if isinstance(number, XlError):
        return False
    ...
Conclusions

We can work productively with Excel in Python with the aid of two mature open-source libraries, openpyxl and formulas. Consuming and producing complex Excel files is a valuable capability in applications whose users routinely work with Excel.

In this tutorial, we’ve learned how to read and write Excel files that may contain formulas. We didn’t talk about styling, charts, merging cells, and other possibilities you may want to read about.

All the sample code shown in this tutorial is available in our GitHub repository.
