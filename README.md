# cybersec_project_1
Return repository for course final project

Report:
LINK: https://github.com/savalre/cybersec_project_1

Installation:
1. Install django version used in project with: python -m pip install Django==4.1.4
2. Clone/extract project and navigate to mysite directory
3. Get database configured with commands: python manage.py makemigrations AND python manage.py migrate
4. Start server with: python manage.py runserver
5. App starts in url http://localhost:8000/polls/

Admin username: admin
Admin pw: kukukissa

I used OWASP 2017 list in this report.

FLAW 1: A1:2017-Injection
Link to flaw: https://github.com/savalre/cybersec_project_1/blob/4870e002057c452e45fcfaa682ae3bfd862fab26/mysite/polls/views.py#L64

Inserting new messages into database is done in this app using python f-string and raw sql. This way user input is directly inserted into SQL query and enables injecting SQL statements into apps SQL query. This makes the SQL injection possible.

Fix: https://github.com/savalre/cybersec_project_1/blob/4870e002057c452e45fcfaa682ae3bfd862fab26/mysite/polls/views.py#L67-L70

Flaw can be fixed by deleting the flawed line and using the outcommented fix line that uses parameterized query. In this method, the data user gives is not directly part of SQL query and SQL injection is not possible.

FLAW 2: A5:2017-Broken Access Control
Link to flaw: https://github.com/savalre/cybersec_project_1/blob/4870e002057c452e45fcfaa682ae3bfd862fab26/mysite/polls/views.py#L82-L85

In this app only admin-lever users can see the delete button and remove messages from the messageboard. Delete button is hidden from normal level users.
But the "message_delete" method is flawed, because it doesn't check if the user that is making the POST request is admin-level or not. This lets normal users delete messages.
You can produce this flaw by logging in with non-admin user and editing this code bit into html template in browsers console:

<form action="http://localhost:8000/polls/<pk>/delete/" method="POST" style="display:inline;">
<button type="submit">Delete</button>
</form>

Replace <pk> with a primary number of the message you want to delete and click delete button. This deletes the message from database. Because the pk numbers are simple integers starting from 1, they are easy to guess, which makes it very possible to guess correct pk-numbers.

Fix: https://github.com/savalre/cybersec_project_1/blob/4870e002057c452e45fcfaa682ae3bfd862fab26/mysite/polls/views.py#L89-L95

Flaw can be fixed by using the outcommented method. This method checks if the user trying to send the POST request is superuser or not.
Because superuser is configured when the app is created, normal users can't create an account with same username that the superused has (in this case 'admin'). This way, non-superuser user can't delete messages from the app.

FLAW 3: A7:2017-Cross-Site Scripting (XSS)
Link to flaw: https://github.com/savalre/cybersec_project_1/blob/4870e002057c452e45fcfaa682ae3bfd862fab26/mysite/polls/views.py#L20-L24

You can produce this flaw by creating new message with message content: <script>alert(document.cookie);</script>

Django has an automatic escaping mechanism in every template. When template is rendered, every template escapes output of every variable tag, turning certain
characters into others, for example "<" is turned into "&lt".
In the app, the message is saved into database in its unescaped form.
I bypassed djangos automatic escaping by making a method "get_context_data" that iterates through every message shown and marks it safe using djangos "mark_safe" method.
Django then sees that the content of message that are marked safe, really are safe and can be shown in their raw form when IndexView is rendered. This enables the XSS-attack.

Fix: To fix this, simply remove the method "get_context_data". Then the messages are shown in escaped form when indexView is rendered and XSS attack is not possible.

FLAW 4: A9:2017-Using Components with Known Vulnerabilities
This is a design fault, so there is no direct link to flaw. I used outdated version of Django framework to build this app.

If you run command "pip-audit" on your command line (pip-audit can be downloaded with command "python -m pip install pip-audit")...:
Name Version ID Fix Versions
---------- --------- ------------------- -------------------
django 4.1.4 PYSEC-2023-13 3.2.18,4.0.10,4.1.7
django 4.1.4 PYSEC-2023-12 3.2.17,4.0.9,4.1.6
django 4.1.4 PYSEC-2023-61 3.2.19,4.1.9,4.2.1
django 4.1.4 PYSEC-2023-100 3.2.20,4.1.10,4.2.3
django 4.1.4 PYSEC-2023-222 3.2.23,4.1.13,4.2.7
django 4.1.4 PYSEC-2023-225 3.2.21,4.1.11,4.2.5
django 4.1.4 PYSEC-2023-226 3.2.22,4.1.12,4.2.6

...you can see that the version of django used in the project has several security vulnerabilities. This version is vulnerable for example to ReDOS and DOS attacks.
This is very poor application designing, and leaves app open to serious breach opportunities.

Fix: In order to fix the flaw, the Django framework used in this project should be updated to a safer, more secure, up-to-date version.

FLAW 5: CSRF Token
Link to flaw: https://github.com/savalre/cybersec_project_1/blob/4870e002057c452e45fcfaa682ae3bfd862fab26/mysite/mysite/settings.py#L49

Django has inbuild middleware token, that protects the app against CSRF attacks. All html-forms should also have csrf-tokens, but they don't work if the middleware is turned off.
I turned off djangos middleware token by commenting the line that contains it, so that csrf attack is possible.

You can produce this flaw by first logging in the messaging application as a normal level user. Then open a 3rd party website (for example StackOverflow) and open the console in your browse. Inserting code bit below into 3rd party website, and pushing 'Submit' button makes it so that the message is posted to the app.

<form action="http://localhost:8000/polls/create/" method="POST" name="CSRF">
<input type="text" name="message_text" value="Hacked">
<input type="datetime-local" name="pub_date">
<input type="submit" value="Submit">
</form>

Fix: Uncomment the line given in flaw link. This turns the middleware token on again and csrf attack is not possible because the middleware token verifies each form submission.

