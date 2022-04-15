<h1>Codeforces Data Collector</h1>
<h3><em>- How it is work?</em></h3>
<ol>
    <li>Put your trainees handles <em>(in separate lines)</em> in <strong>"contestants.txt"</strong></li>
    <li>Put groups or sheets URL you want to get information about <em>(in separate lines)</em> in <strong>"sheets.txt"</strong></li>
    <li>Run scripts in order:
        <ol>
            <li>Create Database.py</li>
            <li>Insert_Sheets.py</li>
            <li>Insert_Contestants.py</li>
            <li>Get_Solutions.py</li>
        </ol>
    </li>
</ol>

<h3>After you run <strong>Get_Solutions.py</strong> you will see the cmd window like this 👇</h3>
![scraping](https://user-images.githubusercontent.com/53629881/163649770-738d891d-386e-4f62-a6f7-3a5bc532c9d6.PNG)

<h3>After finishing it will close by itself and you can see the result in <strong>app.db</strong> </h3>
<h3 style="color:green;">It will return to you for each trainee the number of accepted solutions he had get</h3>

<p>You can edit <strong>Telegram_Bot.py</strong> and put your <em>telegram group id<em>to send some notifications and you can custome it as you want</p>
  
 <p><em>Tools and technologies used: <strong>Telegram_Bot.py</strong> Python, Web-Scraping, Selenium, Telegram-API, SQLite.</p>
