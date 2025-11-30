# CIS216-W01
CIS 216 – Applied Object-Oriented Programming

Student: Amtoj Singh

About This Course

I am taking CIS 216 because I want to strengthen my programming skills beyond the basics and learn how to apply object-oriented programming to real-world problems. This course will also help me prepare for higher-level courses at DePaul University and support my career goals in technology.

Programming Language Selection

For this class, I selected Python 3. I chose Python because it is widely used in many areas of technology such as web development, data analysis, and automation. It has simple syntax, a strong community, and a lot of resources available, which makes it a great language for practicing object-oriented programming concepts.

How I Plan to Use Python

I plan to use Python as my main language for developing applications and solving problems throughout this course. In the future, I intend to use Python for projects involving data analysis, automation, and potentially in my work as a network engineer where scripting and system management are valuable skills.


In Session 2, I learned how to use methods inside a class to organize my code in a cleaner way. I took my original BMI script and rebuilt it into a BMICalculator class that has methods for checking inputs, calculating BMI, and showing the category results. This made the program easier to understand, reuse, and even expand—like adding support for both metric and imperial units. Moving forward, I plan to keep using this approach of breaking code into clear methods so my programs are easier to read, maintain, and build on in both my coursework and future IT work.



Session 3 – Properties
In this session I learned how to use properties to keep class data safe and organized. I added getters and setters with validation for things like name, email, age, GPA, and credits, plus some computed properties like full-time status, class standing, and BMI. This showed me how properties make code easier to manage and more reliable, which I can use in future projects and my career.


Session 4 – Validation: I validated inputs (types, ranges, simple patterns, and cross-references) and used try/except so bad data didn’t crash the app. I also checked date consistency and kept good/bad records separate, which made the program feel more real and reliable.

Session 5 – Unit Testing, I split BMI logic into small functions and wrote unit tests using Python’s built in unittest. Tests cover normal cases, edge cases, and invalid inputs writing tests helped me design cleaner functions and catch mistakes early, which I’ll use in future projects and job tasks.


CIS 216 – Assignment 6 (Employees Inheritance) – ASCII UML
Author: Amtoj Singh

+----------------------+
|       Employee       |
+----------------------+
| - _name: str         |
| - _email: str        |
| - _employee_id: int  |
+----------------------+
| + name: str          |
| + email: str         |
| + employee_id: int   |
| + contact_info():str |
| + compute_pay():float*   (*abstract/overridden) 
| + __str__(): str     |
+----------^-----------+
           |
   +-------+-------------------+--------------------+
   |                           |                    |
+----------+             +-----------+        +-------------+
|  Manager |             | SalesEmp  |        |  HourlyEmp  |
+----------+             +-----------+        +-------------+
| - _annual_salary:float | - _base_pay:float  | - _hourly_rate:float
| - _bonus_percent:float | - _commission:float|                     |
+------------------------+--------------------+---------------------+
| + annual_salary:float  | + base_pay:float   | + hourly_rate:float |
| + bonus_percent:float  | + commission_rate:float                  |
| + give_raise(pct):void | + record_sales($):float                  |
| + compute_pay(n):float | + compute_pay($):float | + compute_pay(h):float
| + __str__():str        | + __str__():str    | + __str__():str     |
+------------------------+--------------------+---------------------+

Notes:
- All subclasses inherit name/email/employee_id, contact_info(), and __str__() from Employee.
- Manager.compute_pay(n) uses annual_salary and bonus_percent, divided by periods (default biweekly 26).
- SalesEmp.compute_pay(sales) = base_pay + sales * commission_rate.
- HourlyEmp.compute_pay(hours) includes overtime ( >40 at 1.5x ).

Session 7 – Polymorphism: I built a Vehicle base class and derived Car, Truck, and Motorcycle, each overriding drive() with their own behavior. By looping over a mixed list of vehicles and calling the same drive() method, I saw how polymorphism lets me write flexible code that’s easy to extend with new types later.

Session 8 – GUI: I built two Tkinter apps: a small “Hello World” to practice widgets and events, and a simple text editor with vertical & horizontal scrollbars, menus, and a status bar. Working with layouts, events, and file dialogs helped me see how GUI apps structure user interactions, and I can reuse this pattern for future tools.

Session 9 – Menus & Events: I extended my text editor by adding a File menu (New, Exit), an Edit menu (Cut/Copy/Paste), and a right-click context menu for the same edit actions. Hooking menu items and keyboard shortcuts into Text widget events made the UI feel more like real software and helped me understand how GUI callbacks and events fit together.

Session 10 – Standard Dialog Boxes: I extended my editor with standard dialogs: file open/save/save-as, a color picker for text color, and a simple font size dialog. This helped me understand how to wire user actions to the right built-in dialogs and update widget state safely. I also kept the code readable and added a few small UX touches (status bar, keyboard shortcuts) that make the app feel more like real software.

Session 11 – Custom Dialog Boxes: I added two custom dialogs to my editor: a modal “About” window built from a Toplevel, and a “Font…” dialog that lists system font families with a size spinner and live preview. Wiring these up taught me how to control modality (transient, grab_set, wait_window), pass state back on OK vs. Cancel, and update a shared tkfont.Font so the editor changes immediately. This made dialogs feel less “magic” and more like normal GUI classes I can reuse.

Session 13 - Inheritance lets you create a new class that reuses and extends an existing one instead of starting from scratch. For example, in my code an Inpatient is a specialized Patient that has extra fields like room number and length of stay, but it still uses all of the basic patient information from the parent class.

The value of inheritance is that it reduces duplicate code and makes programs easier to maintain. If I improve something in the base class, all the child classes benefit automatically. It also lets me override methods in a controlled way, so the subclass can change how something works (like how it prints itself) without breaking other parts of the program. This makes the design more flexible and easier to extend as the system grows.









