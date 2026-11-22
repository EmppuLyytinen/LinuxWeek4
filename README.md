# Linux Week 4 – backups and MariaDB replication

## About the Project

In this assignment, I used two Ubuntu servers in CSC cPouta.

Server A is my original Linux web server, where my earlier assignments are running. Server B was created from a snapshot of server A.

The idea was to make automatic backups from A to B and set up MariaDB replication between the servers.

## MariaDB Replication

I configured MariaDB replication so that changes from Server A are automatically copied to Server B.

I enabled binary logging on Server A and configured Server B as a read-only replica. I also created a separate user for replication.

I tested the replication by refreshing the visitor counter on Server A. The counter value also changed in Server B's database, so the replication was working.

I also checked the replication after rebooting Server B.

Week 4 Flask Application

On server B, I created a separate Flask application that displays the replicated visitor counter.

The application only reads the value from the database. It does not increase the counter when the page is refreshed.

I also created a database user that only has SELECT permission.

The Flask application runs with Gunicorn and systemd, and Nginx passess requests to it.

The page is available at /viikko4/.

## Automatic Backups

I used rsync and SSH to copy files from Server A to Server B.

The backup script copies the contents of /var/www/html to a private backup directory on Server B.

Each backup gets its own folder with a timestamp. This makes it possible to keep older backups instead of replacing them.

I also added a cron job to run the backup script once every hour. The script writes the results to a log file.

Restore Test

I tested restoring a file from one of the backups.

I copied index.html from Server B back to a separate test folder on Server A.

After that, I compared the SHA256 checksums of the original and restored files. The checksums matched, so the restored file was identical.

## Testing

I tested the main parts of the assignment:

MariaDB replication between the servers

Visitor counter updates from A to B

Read-only Flask application on server B

SSH connection and file transfer

Restoring a file from a backup

Services and replication after rebooting server B

I also configured automatic hourly backups with cron. The automatic runs still need to be checked separately from the manual tests.
Hehhllo :)

## Problems and what i learned

I had some problems during the assignment.

One problem was setting up the SSH connection between
the servers. The public key was not copied correctly
at first, so the connection did not work. I fixed the
authorized_keys file and tested the connection again.

I also had to be careful about which server I was using,
because Server A and Server B have different purposes.

I learned more about MariaDB replication, SSH keys,
rsync backups, cron jobs and systemd services.

The most important thing I learned was how to make
two Linux servers work together and how to test that
backups and database replication actually work.
