# **<span style="color: #28a745;">Med</span><span style="color: #007bff;">Connect</span>**

#### Video Demo:  https://youtu.be/D0LOrPFh-SI

#### Description: 
**<span style="color: #28a745;">Med</span><span style="color: #007bff;">Connect</span>** is an Electronic Health Records (EHR) System integrated with an Appointment Management System to keep track of appointments and access your medical records all in one place. Whether you're a patient or a healthcare provider, **<span style="color: #28a745;">Med</span><span style="color: #007bff;">Connect</span>** offers a user-friendly platform to manage your medical information and appointments with ease.

> [!WARNING]
> Since this is a small project I did not implement any encryption to the medical data.
> 
> PS : I know encryption is a requirement for an EHR system

<br>

<details>

<summary>Want to test MedConnect ?</summary>

<br>

### Clone MedConnect Repository

```shell
# Install virtualenv (assuming you have installed python3-pip)
pip install virtualenv

# Make a new directory (Choose any name for the directory) and go inside it
mkdir Test
cd Test

# Create python virtual environment
virtualenv venv

# Activate venv
source venv/bin/activate

# Clone Medconnect repository
git clone https://github.com/dumij58/medconnect.git

```

### From here you can continue in 2 ways (Choose one):

Installing Medconnect

```shell
# cd into medconnect repository
cd medconnect

# Install MedConnect using pip (using -e will make medconnect package editable)
pip install -e .

# Run flask development server
flask --app medconnect run
```

Without installing MedConnect

```shell
# cd into medconnect package inside the medconnect repository
cd medconnect/medconnect

# Run flask development server
flask --app medconnect run
```

</details>

<br>

<details>

<summary>See what each Python file does</summary>

## \_\_init.py\_\_

Flask application factory is initialized in this file and it tells Python to treat the current directory as a package. 

It creates the medconnect application factory, sets the default config values, loads the configuration file if it exists and overwrites the existing config values, creates the instance folder if it doesn't exist, initializes all the extensions (eg: SQLAlchemy, Flask_Migrate, Flask_Mail, etc.), imports and registers the blueprints, configure url rules and set up jinja enironment filters.

## models.py

This file sets up SQLAlchemy and Flask Migrate. It contains all the models for all tables in the database and it sets up the relationships between the models.

## forms.py

This file contains all the WTForms's forms used in the project and custom validators to validate the form data.

## email.py

This file sets up Flask Mail. It defines a function which is used to send emails.

## helpers.py

This file contains flask decorators to ensure a user has logged in to access a certain page or only admins can access the "admin only" pages. It is used to define custom functions and define functions for jinja environment variables.

## auth.py

This file handles everything related to user authentication.

It handles the validation of registration form data of both doctor and patient registration, validation of login data of all 3 user types and while doing that plug the sqlalchemy user object into the flask's g namespace object and create a "user_type" variable inside flask session to show the type of the current logged in user, use flask's app_context_processor() function to make the "user_type" accessible throughout the application, user logout commands and lastly add an admin into the database manually.

<!-- Include add admin instructions -->
<details>

<summary>How to add an admin?</summary>

There is a flask route defined in order to add an admin. You can find the route inside the auth.py file. Type that route into your browser and you will see a form. Give a username, password and a identification no. (any number would work) and submit the form. Admin will be added to the database instantly, now admin can log in using the login page.

</details>

## doc.py

This file contains all the flask routes related to doctors

It handles display doctor dashboard, adding sessions, removing sessions, show all appointments in each session (session panel), start appointment, mark appointment as "no show", store medical records (appointment panel), handle AJAX requests for different sections in appointment panel, handle AJAX requests when changing account details and handle AJAX requests to get doctor and patient names lists.

## pt.py

This file contains all the flask routes related to patients

It handles display patient dashboard, search for appointments with Doctor and/or Hospital and/or Date (can't use just the date to search), add patient medical details, handle AJAX requests when removing items in medical details (it also handles the remove requests for appointment panel mentioned in doc.py), book appointments, cancel appointments (it should be done at least 7 days before the appointment date or you can't cancel), handle AJAX requests when changing account details and handle AJAX requests to get doctor and hospital names lists.

## admin.py

This file contains all the flask routes related to admins

It handles display admin dashboard, validate doctor registration, reject doctor registration, sends email to doctor, add/remove hospitals, show/mark as read messages sent through the contact page, show all the log entries.

## main.py

This file contains everyhting else that I couldn't specify as either doctor or patient or admin related

It handles displaying medconnect homepage, displays profiles for doctors and patients, search medical records for both patients and doctors, show medical records (only the respective patient and doctor have access to it), display contact page and store messages sent through the contact page.

</details>

<br>

## Register

There are two register forms, one for doctors and one for patients. 

When a patient submits their form, they instantly get added into the patient table in the database and a "Welcome to MedConnect!" email is sent to the email provided by the patient. 

When a doctor submit their form, they get added to a temporary table in the database until an admin checks the data and validates the registration, then the doctor is added to the doctor table in the database and a "Registration Pending" email is sent to the email provided by the doctor.

Every input field in both registration forms are validated using WTForms validators and custom validators.

## Login

All three user types have one centralized login page. Entering their username and password will take them to their respective dashboard.

> [!IMPORTANT]
> Because the login page is centralized, doctor/patient/admin can't have the same username.

## Admin

Admin __dashboard__ shows any pending doctor validations and the last 5 log entries. Admins can check the data and decide whether to validate or reject the registration.
When it is validated, doctor is added to the doctor table in the database and a "Welcome to MedConnect" email is sent to the provided email. When it is rejected the temporary doctor data is deleted from the database and a "Registration Rejected" email is sent to the provided email.

Admins can __add/remove hospitals__ into the database using the hospitals page. Hospitals page shows all the hospitals currently in the database.

In the __Messages__ page admins can see the messages sent through the contact page. It includes the type of the user sent the message if the sender is in the database, if not it shows "Not in DB". Admins can mark messages as read for them to dismiss them.

__Log__ page shows all the log entries.

## Doctor

Doctor __dahsboard__ shows their full name, username and registration no. at the top. And it shows appointments that are scheduled for today and upcoming sessions in the next 7 days. Clicking on "Go to Profile" button will take you to the profile page, in there you can change your username, password and other details (except for the registration no.).

Doctors can add/remove sessions using the __Sessions__ page. Session time is validated using a custom validator to check if the time overlaps with an existing session of the same doctor. It shows all the sessions with the count of total available appointments and the number of booked appointments.

> [!IMPORTANT]
> When at least 1 appointment is booked, that session can't be removed.

Clicking on the "View" button on a session takes you to the __Session Panel__, which shows all the appointments currently booked in that session. In the session panel, if an appointment is not started it shows two buttons, one is "Start Appointment" the other is "Mark as No-Show" and if it is currently in session it shows that too. If an appointment is ended, the appointment is not shown in the session panel.

Clicking on "Start Appointment" takes you to the __Appointment Panel__, where you can enter all the medical details of the patient, including follow up and referral details. Ending the appointment will store all the data in different tables in the database.

<details>
<summary>See how medical records get stored in the database</summary>

### Patient Information Tab
When starting an appointment in the appointmnet panel, 1st tab has all the patient details including the patient medical history (if the patient has entered those details in their profile). 

### Examination Tab
On top of the Examination tab there is a button that shows another set of tabbed sections when clicked. It is there for the doctor to add to the patient medical history if needed. Next you can see an input field for the chief complaint. Next there are 2 sections for adding vital signs and examination notes. In these 2 sections you can add/remove items as needed (multiple items can be added)

### Tests Tab
There is a section that you can add tests into the database.

> [!NOTE]
> Test Tab is not fully implemented. Since I started this as a small project adding a full-fledged tests tab (including sending test requests to the relevent labs, get the test results back from the lab, etc.) is out of the scope of this project.

### Diagnosis & Treatment Tab
At the top you can type the diagnosis. Then the Treatment section is devided to 2 parts, medication and other. In medication section you can add all the medication you prescribe for the patient. In other section you can add everything else that you recommend the patient to do. (You can add/remove multiple items from these sections)

### End Tab
In the End tab you can add follow up details (follow up date, etc.) and/or referral details (referral date, doctor's name and specialization, referral reason, etc.) You can select a doctor that is in the database or you can type in a doctor's name that is not in the database by selecting "Other Doctor" from the doctors list.

### But, how is all the data stored?
Every section that has adding/removing multiple items functionality and the referral section have dedicated tables in the database. Everything else (cheif complaint, diagnosis and follow up details) are in a different table called medical record.

Once you start the appointment an entry in medical record table is created. After you end the appointment, medical record data (chief complaint, diagnosis and follow up details) will be updated. The tables dedicated to the sections you can add/remove multiple items get updated as you add/remove them.

> [!WARNING]
> Because of the way this is implemented, you cannot cancel an appointment and delete its data, once it is started.

</details>

In the __Records__ page, doctors can search for medical records by patient and/or hospital and/or date. Then, clicking on the "View" button shows you the whole medical record with all the details you entered in the appointment panel including patient details and hospital details.

## Patient

Patient __dahsboard__ shows their full name and username at the top. And it shows upcoming appointments and recent medical records. Clicking on "Go to Profile" button will take you to the profile page, in there you can change your username, password and other details (except for the registration no.). Clicking on "Make an Appointment" will redirect you to the Appoitments page.

In the __Appointments__ page you can search for appointments by doctor and/or hospital and/or date (can't search by just a date). It also shows the available number of appoointments in the session. Once you've found the right appointment clicking on "Book Appointment" will take you to booking page, which contains all the details related to the appointment. Clicking on "Confirm Booking" will show an alert, if you "Confirm" that your booking will be added to the  appointment table in database.

In the __Records__ page, patients can search for medical records by doctor and/or hospital and/or date. Then, clicking on the "View" button shows you the whole medical record (all the details the doctor entered during the appointment) including doctor details and hospital details.
