from flask import Flask, render_template, make_response, send_from_directory, Blueprint, jsonify, request, redirect
import os
import boto3

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
region_names ={
    'us-east-1': 'N. Virginia',
    'us-east-2': 'Ohio',
    'us-west-1': 'N. California',
    'us-west-2': 'Oregon',
    'ca-central-1': 'Canada',
    'eu-central-1': 'Frankfurt',
    'eu-west-1': 'Ireland',
    'eu-west-2': 'London',
    'eu-west-3': 'Paris',
    'eu-north-1': 'Stockholm'
}
def get_session(region):
    return boto3.session.Session(region_name=region)


@app.route("/instance/delete/<id>", methods=[ "GET"])
def delete_instance(id):
    if id!='i-0d1407909cad2ee82':
        ec2 = boto3.resource('ec2')
        ec2.instances.filter(InstanceIds=[id]).terminate()
    return redirect("/"), 302

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
        return redirect("/"), 302
    else:
        boto3.setup_default_session(region_name='us-east-2c')
        client = boto3.client('ec2')
        instances = []
        total_billing = 0.0
        total_proxies = 0
        for region in client.describe_regions()['Regions']:
            ec2 = boto3.resource('ec2', region_name=region['RegionName'])
            for instance in ec2.instances.all():
                if instance.public_ip_address:
                    print(instance.id)
                    total_billing += 0.08
                    total_proxies +=1
                    instances.append(
                        {'id':instance.id,'proxy': instance.public_ip_address, 'region': region_names.get(region['RegionName'])})
        return render_template("/dashboard.html", **{'module': 'Dashboard','instances': instances,'total_billing':total_billing,'total_proxies':total_proxies}), 200


if __name__ == "__main__":
    app.run(debug=True, port=8000)
