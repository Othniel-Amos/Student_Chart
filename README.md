# Student Tracker
#### Video Demo:  <URL HERE>
#### Description:
<p>My project is a student tracker. It allows teachers to be able to add any number of students under their portfolio and view them all from a table.</p>  
<p>This project also writes values the user inputted to a sqlite database. Then pulling the values from the database to the website so that the user can see them</p> 
<p>The project also employs a multitude of server side validation techniques such as protection against SQL Injection and
intesive validation of the input the user passes to the program</p>
<p>Enhanced security as the program hashes and encrypts valuable information by using post method and encyrpting passwords 
by generating a hash of them.</p> 
<p>This web application also relies heavily on flask acting as a good backend between connection between the database and html files</p>
<p>Below I'll explain the functionality of the files in my project.</p>
<h2>static</h2>
<h3>images</h3> 
<li>eye.png (A photo of an eye used in the homepage)</li>
<li>favicon.ico (The webpage logo that displays as an icon when viewed from a tab)</li>
<li>green_icon.jpg (A photo of a green plus picture used in the homepage of the app )</li>
<h3>style.css</h3> 
<li>Here are some unique designs that I used for different aspects of the webpage</li>
<li>For example the colour of the name of the webpage is a specific font</li>
<li>The tables are also made in a way that they'll be nice to look at by being rounded</li>
<h2>Templates</h2> 
<h3>add.html</h3> 
<li>Shows the user an interface to be able to add a student to their classroom</li>
<li>It also has added validation to prevent the user from either accidentally or nefariously adding erroneous values  </li>
<li>Flashes messages warning the user of why their values for a student's name aren't accepted (for example the name field could be blank)</li> 
<li>Has a submit button that submits the info to main.py</li>
<hr>
<h3>homepage.html</h3> 
<li>A homepage that the user is redirected to upon logging in to the website</li> 
<li>It has various cards below so that the user can click to be redirected to different parts of the website</li> 
<hr>
<h3>index.html</h3> 
<li>Acts as a layout page for the rest of the pages</li> 
<li>Initializes important features such as the navbar and the icon picture so the look across all sites may be synchronised </li> 
<hr>
<h3>login.html</h3> 
<li>Allows the user to login in with a username and password <strong>if and only if</strong> the user is already registered into the website</li>
<li>If a wrong username or password is given the user is blocked access to the site until a valid one is given</li>
<hr> 
<h3>register.html</h3>
<li>Allows the user to register an account (username and password) <strong>if and only if the username is not already taken</strong></li>
<li>The username and password must meet some already set standards to be registered into the database</li>  
<li><i>Little caveat but you can't register for an account if your already logged in</i></li>
<hr> 
<h3>view.html</h3>
<li>Allows the user to view all of their students in a tabular format</li>
<li>It will not display the information of any students the teacher is not teaching in the database</li>
<br> <hr>
<h2>functions.py</h2> 
<li>A list of functions that I made to help abstract some of the heavy lifting of main.py</li> 
<li>One of the most important functions is that it establishes a connection with the sql database along with doing various things such as
<ol><li>Validating usernames and passwords</li>
    <li>Displaying students to the view.html file</li> 
    <li>Reading from the json file</li> 
    <li>Gets the subjects,grades and classes of the json file</li>
</ol>
</li> <hr>
<h2>school.json</h2> 
<li>A list of attributes such as: grades,subjects and classes</li>
<li>Used for validating the user input from add.html (Checking for tampering with the code from the client side)</li> 
<hr> 

<h2>students.db</h2>
<li>A sql file in which the values of main.py are stored so that they can persist even after the server shuts down</li> 
<li>Also has some already inputted student values to test with</li>
<li>This database also has some prebuilt tables inside it</li>
<li>These tables make sure that things such as usernames and ID's for students and likewise teachers remain completely unique</li>
<li>It also allows for the number of subjects a student has to be able to dynamically increase <i>(One student could have 8 subjects will another has only 2)</i></li> 
<li>Each student is marked under a specific teacherID rendering a one-to-many relationship between teachers and students</li>
<li>One teacher could have many students but one student can only have one teacher</li>

<hr> 
<h2>usernames.txt</h2>
<li>A list of already registered usernames that you can use to log in</li>
<li>I suggest using the username of michael as it already has access to some values of students in the database</li>
<hr> 
<h2>log out</h2>
<li>The web app also allows its users to logout by clicking the button on the navbar</li> 
<hr>
<h2>requirements.txt</h2>
<li>If you download this file and wish to run it locally do the following please</li> 

## Installation 
- Works with python 3.12 +
- Open command terminal in virtual environment and paste the following
```
pip install -r requirements.txt
``` 
<h3>Thanks for reading the README file :D</h3>