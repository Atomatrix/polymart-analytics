# Polymart Analytics
Create your own Polymart Analytics using their webhooks without needing a Plus or Pro upgrade.

# How to set up
- Clone the files to a place where you can run a web server.
- Change the port in `settings.yml` to the port you wish to use on your server.
- Create a webhook on your product page(s).
  - The format of your webhook should be: `http://IP.ADDRESS:PORT/webhook`.
- Copy the webhook secret and add it to the list of them in the `settings.yml` file.
- Add your Polymart API key (found on [this page](https://polymart.org/account)) to `settings.yml`.
- Install the Python packages from `requirements.txt`.
- Run `main.py`.
- Send a test webhook from a Polymart resource and see if it comes up in the console.
- Any purchases from users will be added to the `data.csv` file.
