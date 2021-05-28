#-*- coding:utf-8 -*-
from flask import Flask, render_template, request, jsonify
import yaml
import logging
import git
import os

app = Flask(__name__)
config = yaml.safe_load( open("config.yml") )

def get_project_name( git_path ):
    return git_path.split('/')[-1].split('.')[0]

@app.route( '/', methods=['GET'] )
def index():
    return render_template('index.html')

@app.route( '/git/clone', methods=['POST'] )
def git_clone():
    result = {"code":"0", "message":"success"}
    if request.method == 'POST':
        git_path = request.form.get( "git_path")
        project_name = get_project_name( git_path )
        to_path = os.path.join(config.get("project_path"), project_name)
        logging.info( "项目名称: %s"%(project_name) )
        logging.info( "项目路径: %s"%(to_path) )
        try:
            git.Repo.clone_from( git_path, to_path )
        except Exception as e:
            result["code"]="1"
            result["message"]=str(e)
    return jsonify(result)

if __name__ == '__main__':
    logging.basicConfig( level=logging.INFO, filename="console.log" )
    app.run(host='localhost', port=9999)
