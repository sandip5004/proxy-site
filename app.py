from flask import Flask, render_template, make_response, send_from_directory, Blueprint, jsonify, request
import os
import boto3
import pprint


# import awsutils

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), 'templates'),
        static_url_path=os.path.join(os.getcwd(), 'static'),
    )
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
    app.secret_key = 'd5c2ba7f-4926-4bc1-883a-9d74c8c246ea '
    app.config['SESSION_TYPE'] = 'redis'
    return app


app = create_app()

site_static_blueprint = Blueprint('static_files', __name__, static_url_path='/static', static_folder='static/')
app.register_blueprint(site_static_blueprint)


regions = {
    'us-east-1':'ami-00639dda9aa592f98',
    'us-east-2':'ami-01494aa943347280a',
    'us-west-1':'ami-06fdeca3c7ed916dc',
    'us-west-2':'ami-0303636ed16a45543',
    'ca-central-1':'ami-0f260257895cebccd',
    'eu-central-1':'ami-022590452567c90af',
    'eu-west-1':'ami-0e8234a3160901309',
    'eu-west-2':'ami-06b2fa87250a5ddd7',
    'eu-west-3':'ami-0d02d1f42e41770c4',
    'eu-north-1':'ami-04b38e0bbea7a5167'
}

def get_session(region):
    return boto3.session.Session(region_name=region)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        boto3.setup_default_session(region_name=request.form['zone'])
        ec2 = boto3.resource('ec2')
        ec2.create_instances(ImageId=regions.get(request.form['zone']), MinCount=int(request.form['proxy_count']),
                             MaxCount=int(request.form['proxy_count']),
                             InstanceType='t2.micro',
                             # KeyName='sandip.dev'
                             )
        client = boto3.client('ec2')
        instances = []
        for region in client.describe_regions()['Regions']:
            ec2 = boto3.resource('ec2', region_name=region['RegionName'])
            for instance in ec2.instances.all():
                if instance.public_ip_address:
                    pprint.pprint(instance)
                    instances.append(instance.public_ip_address)
        return render_template("/dashboard.html", **{'instances': instances}), 200
    else:
        return render_template("/dashboard.html", **{'module': 'Dashboard'}), 200


if __name__ == "__main__":
    app.run(debug=True, port=8000)
