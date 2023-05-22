
from flask import Flask, render_template
from dotenv import load_dotenv
from meraki import DashboardAPI
from google.cloud import vision, vision_v1p4beta1
import urllib

load_dotenv()

dashboard = DashboardAPI(
    output_log=False,
	print_console=False
)

app = Flask(__name__)

def create_app():
    app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def organizations():
    response = dashboard.organizations.getOrganizations()
    print(response)
    return render_template(
        'index.html',
        response=response,
        title='Organization',
    )

@app.route('/<organizationId>', methods=['GET', 'POST'])
def networks(organizationId):
    response = dashboard.organizations.getOrganizationNetworks(organizationId=organizationId)
    print(response)
    return render_template(
        'index.html',
        response=response,
        title='Network',
    )

@app.route('/<organizationId>/<networkId>', methods=['GET', 'POST'])
def network(organizationId,networkId):
    response = dashboard.networks.getNetwork(networkId)
    print(response)
    return render_template(
        'network.html',
        response=response,
        title='Network',
    )

@app.route('/<organizationId>/<networkId>/camera', methods=['GET', 'POST'])
def cameras(organizationId,networkId):
    response = dashboard.camera.getOrganizationCameraOnboardingStatuses(organizationId)
    print(response)
    return render_template(
        'cameras.html',
        response=response,
        title='Camera',
    )

@app.route('/<organizationId>/<networkId>/camera/<serial>', methods=['GET', 'POST'])
def camera(organizationId,networkId,serial):
    response = dashboard.camera.generateDeviceCameraSnapshot(serial)
    print(response)
    # Instantiates a client
    client = vision_v1p4beta1.ImageAnnotatorClient()

    # Loads the image into memory
    resource = urllib.request.urlopen(response['url'])
    content = resource.read()
    image = vision_v1p4beta1.Image(content=content)

    # Performs label detection on the image file
    analyze = client.label_detection(image=image)
    labels = analyze.label_annotations

    return render_template(
        'camera.html',
        response=response,
        labels=labels,
        title='Camera',
    )

@app.route('/<organizationId>/<networkId>/wireless', methods=['GET', 'POST'])
def wireless(organizationId,networkId):
    response = dashboard.wireless.getNetworkWirelessSsids(networkId)
    print(response)
    return render_template(
        'wireless.html',
        response=response,
        title='Wireless',
    )

@app.route('/<organizationId>/<networkId>/wireless/<number>', methods=['GET', 'POST'])
def ssid(organizationId,networkId,number):
    response = dashboard.wireless.getNetworkWirelessSsid(networkId, number)
    print(response)
    return render_template(
        'ssid.html',
        response=response,
        title='SSID',
    )