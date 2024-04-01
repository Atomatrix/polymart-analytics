import csv
import datetime
import hmac, hashlib
import requests, yaml
from flask import Flask, request

app = Flask(__name__)

# Load Settings
with open('./settings.yml', encoding="utf8") as file:
    settings = yaml.load(file, Loader=yaml.FullLoader)

def get_resource_price(resource_id):

    r = requests.get(f'https://api.polymart.org/v1/getResourceInfo?api_key={settings["polymart_api_key"]}&resource_id={resource_id}')
    data = r.json()

    if r.status_code != 200:
        return None

    return data['response']['resource']['price']


def verify_request(request_data, polymart_signature):

    for webhook_secret in settings['webhook_secrets']:

        # Form the request signature
        hmac_object = hmac.new(bytes(webhook_secret, 'utf-8'), request_data, hashlib.sha256)
        request_signature = hmac_object.hexdigest()

        if polymart_signature == request_signature:
            return True

    return False


@app.route('/webhook', methods=['POST'])
def webhook():

    if not verify_request(request_data=request.data, polymart_signature=request.headers["X-Polymart-Signature"]):
        return 'Unauthorised', 403

    data = request.get_json()

    if data['event'] == 'ping':
        print(f'Received a test ping!')
        return '', 200

    # Return if the event isn't a user purchase.
    if data['event'] != 'product.user.purchase':
        return 'Invalid Event', 400

    product_id = data['payload']['product']['id']
    product_title = data['payload']['product']['title']
    user_id = data['payload']['user']['id']

    # Get the resource price
    product_price = get_resource_price(product_id)

    # Get date and time
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime("%d/%m/%Y")
    formatted_time = current_datetime.strftime("%H:%M")

    new_data = [formatted_date, formatted_time, product_title, product_id, product_price, user_id]

    with open(settings['result_file_name'], mode='a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(new_data)

    print('A new purchase has come through and added to the CSV file.')

    return '', 200


if __name__ == '__main__':

    print('Starting Web Server...')

    if settings['debug_mode']:
        app.run(host='0.0.0.0', port=int(settings['web_port']), debug=settings['debug_mode'])

    else:
        from waitress import serve
        serve(app, port=int(settings['web_port']), host='0.0.0.0')