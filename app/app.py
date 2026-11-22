
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from flask import Flask

# Load database settings
load_dotenv(Path(__file__).with_name(".env"))

app = Flask(__name__)

@app.route("/viikko4/")
@app.route("/week4/")
def counter():
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE")
    )

    cursor = db.cursor()

    try:

        # Read the updated value
        cursor.execute(
            "SELECT views FROM page_views WHERE id = 1"
        )
        views = cursor.fetchone()[0]
    finally:
        cursor.close()
        db.close()

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Linux Project - Week 2</title>

        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                background: #101827;
                color: #f8fafc;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 45px 20px;
            }}

            .container {{
                max-width: 750px;
                margin: auto;
            }}

            .subtitle {{
                color: #60a5fa;
                font-weight: bold;
                letter-spacing: 2px;
            }}

            h1 {{
                font-size: 36px;
                margin-bottom: 10px;
            }}

            p {{
                color: #cbd5e1;
		font-size: 18px;
                line-height: 1.7;
            }}

            .counter {{
                background: #1c2b44;
                border: 1px solid #334155;
                border-radius: 12px;
                text-align: center;
                padding: 35px;
                margin: 30px 0;
            }}

            .number {{
                color: #60a5fa;
                font-size: 65px;
                font-weight: bold;
                margin: 10px;
            }}

            .tag {{
                display: inline-block;
                background: #283750;
                padding: 9px 14px;
                margin: 4px;
                border-radius: 6px;
                color: #e2e8f0;
            }}

            .info {{
                margin-top: 0px;
                padding-top: 0px;
            }}

            a {{
                color: #60a5fa;
            }}
		.info-box {{
    		background: #1c2b44;
    		border: 1px solid #334155;
    		border-radius: 12px;
    		padding: 25px;
    		margin: 20px 0;
}}
		.copy-icon {{
		font-size: 35px;
		color: #60a5fa;		
}}
		.title-row {{
    		display: flex;
    		align-items: center;
    		gap: 14px;
    		margin-bottom: 15px;
}}

		.title-row img {{
    		width: 60px;
    		height: 60px;
    		object-fit: contain;
    		display: block;
}}

		.title-row h1 {{
    		margin: 0;
}}


		.project-links {{
    		display: flex;
    		flex-wrap: wrap;
    		gap: 12px;
}}

		.project-links p {{
    		margin: 0;
}}

		.project-links a {{
    		display: inline-block;
    		background: #283750;
    		color: #60a5fa;
    		border: 1px solid #334155;
    		padding: 12px 14px;
    		border-radius: 8px;
    		text-decoration: none;
    		font-size: 15px;
    		transition: background 0.2s;
}}

		.project-links a:hover {{
    		background: #334b70;
    		color: #93c5fd;
}}


        </style>
    </head>

<body>
    <div class="container">

<div style="display: flex; align-items: center; gap: 15px;">
         <h1 style="margin: 0;">My Linux Server Replica</h1>
         <img src="/tux.png?v=2"
         alt="Tux Linux mascot"
         style="width: 60px; height: auto;">
</div>

        <p>
            Welcome to my fourth Linux project!
            This time I have two Ubuntu servers working together.
            Server A handles the original visitor counter,
            while Server B displays the replicated data
            without making any changes to it.
        </p>

        <div class="counter">
            <h2>Replicated Page Loads<span style="font-size: 35px; color#60a5fa;">⧉</span></h2>
            <div class="number">{views}</div>
            <p>Read-only replica - Server B</p>
            <p>
                Refreshing this page does not increase the counter.
                The value comes directly from Server A
                through MariaDB replication.
            </p>
        </div>

        <h2>Technologies used</h2>

        <span class="tag">Ubuntu</span>
        <span class="tag">Nginx</span>
        <span class="tag">Python</span>
        <span class="tag">Flask</span>
        <span class="tag">MariaDB</span>
        <span class="tag">SSH</span>
        <span class="tag">rsync</span>
        <span class="tag">cron</span>
        <span class="tag">systemd</span>

        <div class="info">

            <div class="info-box">
                <h2>How does it work?</h2>
                <p>
                    Server A runs the original Flask application
                    and stores the visitor counter in MariaDB.
                    Every new visit updates the database.
                </p>
                <p>
                    MariaDB continuously replicates the changes
                    to Server B. This page reads the counter
                    from B's local database using a dedicated
                    read-only database user.
                </p>
                <p>
                    The application only uses SELECT queries,
                    so visiting this page does not increase
                    the counter.
                </p>
            </div>

            <div class="info-box">
                <h2>About my servers</h2>
                <p>
                    Both servers are running Ubuntu in CSC cPouta.
                    Server B was created from a snapshot of
                    Server A and has its own public IP address.
                </p>
                <p>
                    Server A stores website files in
                    /var/www/html and runs the primary MariaDB
                    database. Server B has its own local MariaDB
                    storage and keeps website backups in
                    /srv/backups/server-a/.
                </p>
            </div>

            <div class="info-box">
                <h2>Backups and security</h2>
                <p>
                    Server A automatically sends website backups
                    to Server B once every hour.
                    I used cron, SSH and rsync for this.
                </p>
                <p>
                    The cron schedule is 0 * * * *.
                    Every backup gets its own timestamped folder,
                    and the results are saved in
                    /home/ubuntu/week4-backup.log.
                </p>
                <p>
                    Backups are stored outside the public website.
                    The dedicated Linux user week4backup owns
                    the backup directory, with permissions 700.
                    SSH keys are used for authentication.
                </p>
                <p>
                    Separate MariaDB users are used for
                    replication and application access.
                    The replica application's database user
                    has SELECT-only permissions.
                </p>
                <p>
                    Replication is not a replacement for backups,
                    because accidental changes or deletions
                    can also be replicated.
                </p>
            </div>

            <div class="info-box">
                <h2>Testing everything</h2>
                <p>
                    I tested both websites and confirmed that
                    Server A increases the visitor counter.
                    The updated value also appears on Server B.
                </p>
                <p>
                    Refreshing Server B does not increase
                    the counter. MariaDB replication was checked
                    and both replication threads were running.
                </p>
                <p>
                    Two automatic backups succeeded on
                    November 22, 2026 at 18:00 and 19:00
                    Finnish time. Four timestamped backup
                    directories were found on Server B.
                </p>
                <p>
                    I also restored a test file to a separate
                    location and compared SHA256 checksums.
                    The restored file matched the original.
                </p>
                <p>
                    After rebooting Server B, the website
                    and database replication were working.
                    The hourly backup cron job remains active
                    on Server A.
                </p>
            </div>

            <div class="info-box">
                <h2>What did I learn?</h2>
                <p>
                    This project helped me understand how
                    two Linux servers can work together.
                    I learned more about MariaDB replication,
                    automated backups and Linux permissions.
                </p>
                <p>
                    One challenge was getting SSH access
                    between the servers working correctly.
                    After fixing the SSH key configuration,
                    the backups started working as expected.
                </p>
            </div>
<div class="info-box">
    <h2>Project links</h2>

    <div class="project-links">
        <p><a href="http://193.166.24.211/viikko2/">
            Server A - Original Counter
        </a></p>

        <p><a href="http://195.148.23.195/viikko4/">
            Server B - Read-Only Replica
        </a></p>

        <p><a href="https://github.com/EmppuLyytinen/LinuxWeek4">
            My GitHub project
        </a></p>
    </div>
</div>
</body>
</html>
	"""
