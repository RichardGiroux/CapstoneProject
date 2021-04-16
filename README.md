# CapstoneProject
This will be for putting my capstone project, which has been named Quagga.

It has been worked on by Richard G, Cyrus R, Gurpreet R, and Rajab M. 

This program was built to be able to take 2 different configuration files from routers and or switches and compare them, showing the differences between them. This includes but is not limited to omissions on 1 file that is not present on the other, or any typo's and/or irregularities between them. It is able to import these configurations file both manually, as well as through our built in FTP plugin that allows you to connect to an FTP server directly through the app.

It also has a built it telnet system. This was designed with the idea in mind that the user could telnet directly into the device they want to, and run the built-in commands(on a cisco device) that allows the user to directly export their configs in a .txt file format to an FTP server, where they could then connect in to and use the files accordingly.

It also has a grading feature that is WIP. It is able to take 2 files, one "master" file which will be used as a reference file in which the other file will be graded against. The other file is the file to be graded. There are also 4 checkboxes on this page, they are grading criteria. The user is able to choose any of these in any amount to mix and match the criteria as desired. When the user is satisfied with his choices, he hits the button to grade the file and a grade is printed out. If the user needs more information the files are also displayed in the "Compare" tab. If the user doesn't select ANY checkboxes and hits grade, the whole file will be graded.

- Currently on the grading tab only the "Telnet" and "Static/Default Routes" checkboxes work, this is a WIP.
