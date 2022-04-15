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

<h3><em>- After you run <strong>Get_Solutions.py</strong> you will see the cmd window like this 👇</em></h3>

![scraping](https://user-images.githubusercontent.com/53629881/163650691-4f71edbd-8102-4c7e-9082-4f69894759c6.PNG)

<h4>After finishing it will close by itself and you can see the results in <em>"app.db"</em> you will see for each trainee the number of accepted solutions he had get and when was the last submit!</h4>

<h4>- <em>Note</em> You can edit <em>"Telegram_Bot.py"</em> and put your <em>telegram group id<em> to send some notifications and you can custome it as you want</h4>

 <h3>- <em>Tools and technologies used: Python, Web-Scraping, Beautifulsoup, Selenium, Telegram-API, SQLite</h3>
```diff
- asd in red
```
