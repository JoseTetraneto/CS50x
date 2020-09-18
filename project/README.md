# **Lembrô**

## **Overview**
This Project is the **Final Project** of the Harvard **CS50x** course. It's a **web** based application made possible via **Flask** by coding in **Python**, **HTML** and **CSS**. It's main purpose is to gather in one website all the information of the congresspeople from Brazil, as well as the new legislation being voted, so that the user can follow-up on their candidate after they're elected and check if he or she is acting in accordance with their promisses.

## **Purpose**
A vital part of democracy is the involment of the people in the election process, as well as in the day-to-day political life. Going to the ballots on election day is a vital part of democracy, however it isn't all of it. People should follow their candidates' actions and check if they're putting in action what was preached during the campaign. Through such monitoring we're able to undestand how commited to the progress of the nation our congresspeople are.

It's very common for people in Brazil to go to the ballots on election day and vote for their congresspeople. However, it's quite unsual for them to follow-up on the actions of those who were elected. This happens for a variety of reasons, but mostly because people don't have the knowledge of where to find information about their congress people. 

Aiming to amelliorate this situation, this web application is being created. It's main purpose is to gather in one website all the information of the congresspeople from Brazil, as well as the new legislation being voted, so that the user can follow-up on their candidate after they're elected and check if he or she is acting in accordance with their promisses.

## **Structure**
The backbone of this application is a databased created with the help of several APIs made available by Brazil's Parliament. All the functions that update this database can be found on the helpers.py file.

The website has a topnav bar that is present in all pages, it has a footer that also is present in all pages and its content is divided in the following pages:

### **Inicio (Home)**
In this page the user will find information about **What is Lembrô?**, a brief **History of the Parliament** and its **headquarters**. You`ll also be able fo find some links to external sources.

### **Deputados (Congresspeople)**
In this page the user will find a table containing all the congresspeople in the Parliament. The information in the table is the following:
- Picture
- Name
- Party
- Scholarity
- Button that directs the user to a page containing further details about the congresspeople

Also, in this page the user is able to use one of three filters to filter the table *(it's not possible to combine the filters)* and speed up the search.

### **Deputado (Congressman)**
In this page the user will find detailed information about the congressman. This information is divided in 2 sections:
- Top left corner: Here the user will find the following information
    1. Picture
    2. Name
    3. Party
    4. Scholarity
    5. Date of birth
    6. Place of birth
    7. Cabinet phone
    8. Whereabouts of the cabinet
    9. E-mail
- Bottom portion of the page: Here the user will find a table contaning the results of the all the votes the congressman has participated.

### **Proposições (Proposed Law)**
This page is very similar to the Congresspeople page, with the difference that instead of displaying information about the congresspeople it displays information about the proposed laws that have been passed or that are under evaluation.

The information is also displayed in a table and the user is also able to use one of three filters to filter the table *(again, here it's not possible to combine the filters)*.

### **Meus Deputados (My Congresspeople)**
This page is essentially the same as the Congresspeople page, with the difference that it only displays the congress people that the user has saved as their favorite. It's important to notice that this page is only accessible if you have logged-in.

### **Cadastre-se (Register)**
This page is a registration page in which the user is prompted to provide a unique username and a password and a password confirmation. It's important to notice that there are a few checks to ensure the correct use of the registration feature. Also, the password is hashed so that nobody can access it.

### **Entre (Login)**
This is a login system that performs a few checks and creates a session with which the user can access the *My Congresspeople* page.

### **Saia (Logout)**
This is a simple logout button that finishes the user session.