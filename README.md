# CONTRAST
### Video Demo:  <URL https://youtu.be/HafZyUTpcQM>
### Description:-

#### Introduction:
My final project, "Contrast" is an inventory and database management app designed to provide a bespoke solution to a medium sized printing company. The requirements of the company are unique in, that they do not own their own warehouses or offices. The business is built on relationships with suppliers. At every step of the process, the suppliers hold the stock intermediately as it is prepared for the next step. For example, once the plates are printed, they are held by the plate supplier until the printing press (a separate contractor) is ready. Delivery drivers from the press then come and collect the plates when the press is ready and so on.

Due to this structure, a supply chain management solution was needed to keep track of where the raw materials and stocks of each finished product are kept as well as keeping accounts with each supplier (and the clients). The biggest challenge for the project was modelling the complex relationships between the company and its suppliers, contractors and clients. This involved quite a large learning curve in database design. The design was completed using a freely available database visualisation tool. The implementation of the database and subsequently, the app itself, was relatively quick from that point on.

#### Choice of implementation:

The main decision in the early part was whether to implement the solution as a standalonde desktop app, a mobile app or a web app which could be accessed via a browser. Ultimately the decision to implement a web app was based on the choice of the client who wanted employees to be able to access the required information quickly and easily without having to go through installation steps.

#### Choice of language and framework:

I arrived at the choice of using Python as a programming logic due to its ease of implementation. I am aware that C and javascript offer certain performance advantages. However for the relatively small scale of the project and after conversations about future expansion plans for the company, it was decided that python would be able to meet the demands of the scale.

Having made the choice to work with Python for a web app, the main choice was between using Django which provides a number of features out of the box including an extensive security suite, and Flask which is more minimalist but quicker to get operational. Once again, due to the relatively small scale of the company and with no plans to expand further, Flask won as a simple, working solution.

#### Structure:

The project consists of the app folder which contains all the files required for Flask i.e., the main python file, "app.py" which implements the app; the "static" folder harbouring the icon and the "styles.css" file containing styling information; the "templates" folder containing the html files for specific routes within the app as well as a "layout.html" file which serves as a basis for all other templates. Additionally, the "flask_sessions" folder stores session information on the server.

Apart from the "app.py", a number of other project files are stored here. The structure below provides a brief overview of what each file does.

**contrast.db**: The main database stored on the server. The app interacts with the database using the Sqlite3 library context manager.

**helpers.py**: Contains auxiliary functions, decorator functions and formatting functions used in the main program.

**queries.sql**: Queries used to test the python database api were stored here.

**requirements.txt**: A Flask prerequisite text file to enable others to understand what files are needed for app.py to function.

**schema.sql**: The database was implemented using this sql file. It contains information about the design and structure for each file.

**testing.py**: Used to break down snippets of code and test for functionality on a smaller scale before implementing in the main program.

#### Summary:

At this stage, the app, while not complete has all required functionality. The steps to come include the implementation of forms for data entry into each table and functionality required to edit existing data. The structure for data entry from forms into the network of tables itself has been blueprinted in "queries.sql" but requires implementing in the main program. I enjoyed seeking a project on my own and deciding on a spec in collaboration with a client. The process of designing a database, while at times overwhelming, was an excellent learning process. I am looking forward to continuing to improve the **"Contrast"** app and deploying it in production.