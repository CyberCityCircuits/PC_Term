PC_Term (Product Code Terminator)
V0_06_01F - Release: 02-12-2017

All software is original and does not infringe on any copyrights or licenses held by Verifone or any Verifone Authorize Service Company.

Note:  If found inside a .zip file, the .zip file will need to be decompressed in order for the tools  to operate properly.

New to Version 0_06_01:
Built a Graphical User Interface Framework.

New to Version 0_06_00:
Added functions to reset and change ID Checks and Food Stamp Checks on PLUs.

Instructions for use:
	Place the entire 'export' from your POS in the folder called 'Put_XMLs_Here'.  If the folder doesn't exist, running the tool will automatically create it.  Once running the tool, it will import your dataset.  A list of departments will show on the main window.

The 'Edit PLUs' menu has several menu options in it.
	* Remove Product Codes - This will reset all product codes in the 'PLUs.xml' file to '0'.
	* Remove Food Stamps Checks - This will remove all checks in all PLUs for food stamps.  This may not always be desirable.  If you want to keep the food stamp checks you have now, but you want to add to other items then use the 'Set Food Stamp Checks by Department' option.
	* Reset ID Checks by Department - This will remove all ID checks for tobacco and alcohol.  Then it will let you add ID checks by departments.  When you are done entering department indexes enter '0' to be finished.  If you need to remove a department from the list just enter the number with a '-' in front of it.  For example, if you need to remove department '20' from your list then you can type in '-20' and that will remove it.
	* Set Food Stamp Checks by Department - This willadd food stamp checks by department. It adds the value to every PLU assigned to that department.


All processes add a log entry in a file called '!PC_Term Report.txt'

Please share and distribute as needed.  Any questions, problems, or concerns can be sent to David Ray.

Thank you.
