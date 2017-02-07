PC_Term (Product Code Terminator)
V0_06_00H - Release: 02-05-2017

All software is original and does not infringe on any copyrights or licenses held by Verifone or any Verifone Authorize Service Company.

Note:  If found inside a .zip file, the .zip file will need to be decompressed in order for the tools  to operate properly.

New to Version 0_06_00:
Added functions to reset and change ID Checks and Food Stamp Checks on PLUs.

Instructions for use:
Place the entire 'export' from your POS in the folder called 'Put_XMLs_Here'.  If the folder doesn't exist, running the tool will automatically create it.  Once running the tool use option 1 to import the dataset into PC_Term.  Once imported, use option 5 to remove all product codes from the PLUs.  Use option 6 to reset ID Checks by department.  Use option 7 to remove all Food Stamp Checks (if needed).  Use option 8 to add Food Stamp Checks to the PLUs by department.  Once inside option 6 and option 8 you can enter 'dept' to check the department list that is inside your dataset to make sure you are using the right department.  Once you are finished use option 2 to export your dataset for use with your POS.

When you import the dataset into PC_Term, it also creates a backup of the original dataset in a folder called 'Backup_XMLs'.  When you export the dataset it places your export into a folder called 'Processed_XMLs'.  The dataset in the 'Processed_XML' folder is what you will use in your POS.

All processes add a log entry in a file called '!PC_Term Report.txt'

Please share and distribute as needed.  Any questions, problems, or concerns can be sent to David Ray.

Thank you.
