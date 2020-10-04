import os

url=""
os.environ["HTTP_PROXY"]=url
os.environ["HTTPS_PROXY"]=url
os.environ["OUTPUT_DIR"]="logs/"
os.environ["creds_file"]="C:\\Users\\HP\\Documents\\home\\test\\cred.txt"
os.environ["creds_profile"]="default"