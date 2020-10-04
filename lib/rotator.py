import os
import configparser
import logging

def get_aws_config(creds_profile, file):
    config = configparser.RawConfigParser()
    try:
        config.read(file)
        aws_access_key_id = config.get(creds_profile,'aws_access_key_id')
        aws_secret_access_key = config.get(creds_profile,'aws_secret_access_key')
    except Exception as e:
        logging.error("Failing on reading config file with {}".format(e))
        raise e
    return aws_access_key_id,aws_secret_access_key

def set_aws_config(creds_profile, file , aws_access_key_id, aws_secret_access_key):
    config = configparser.RawConfigParser()
    try:
        config.read(file)
        config.set(creds_profile,'aws_access_key_id',aws_access_key_id)
        config.set(creds_profile,'aws_secret_access_key',aws_secret_access_key)
        with open(file,'w') as configfile:
            config.write(configfile)
    except Exception as e:
        logging.error("Falling on setting config file with {}".format(e))
    else:
        logging.info("Updated {} creds in {}".format(aws_access_key_id,file))

def create_key(client,username):
    access_key_metadata = client.create_access_key(UserName= username)['AccessKey']
    access_key = access_key_metadata['AccessKeyId']
    secret_key = access_key_metadata['SecretAccessKey']
    print("Your new access key is {} and Your new secret key is {}".format(access_key,secret_key))
    logging.info("Your new access id and key is create as {} ".format("access_key"))
    return access_key,secret_key

def delete_key(client , access_key, username):
    try:
        client.delete_access_key(UserName=username,AccessKeyId=access_key)
        logging.info("The Access with id "+access_key+" has been deleted")
    except Exception as e:
        logging.error("The access key is ID {} cannot be found/deleted".format(access_key))

def get_username(client , aws_access_key):
    username = None
    try:
        username = client.get_access_key_last_used(AccessKeyId= aws_access_key)['UserName']
        print(username)
    except Exception as e:
        logging.error("Failing on getting username for access key {} with {}".format(aws_access_key,e))
        raise e
    return username

def rotate_keys(client , creds_profile , creds_file):
    try:
        aws_access_key , aws_secret_key = get_aws_config (creds_profile,creds_file)
        print("Old credential getting rotated is : {} {}".format(aws_access_key,aws_secret_key))
        logging.info("Old key getting rotared is : {} ".format(aws_access_key))
        username = get_username(client,aws_access_key)
        keys = client.list_access_keys(UserName=username)
        logging.info("The access key with Id {} is associated with user {}".format(aws_access_key,username))
        inactive_keys = 0
        active_keys = 0
        for key in KeyError['AccessKeyMetadata']:
            if key['Status']=='Inactive': inactive_keys=inactive_keys+1
            elif keys['Status']=='Active': active_keys+1
        logging.info("{} has {} inactive keys and {} active keys".format(username,inactive_keys,active_keys))
        if inactive_keys+active_keys>=2:
            logging.error("{} already has 2 keys. you must delete a key before you can create another key.".format(username))
            exit()
        access_key , secret_key = create_key(client,username)
        print("New keyss", access_key,secret_key)
        delete_key(client,aws_access_key,username)
        set_aws_config(creds_profile,creds_file,access_key,secret_key)
    except Exception as e:
        logging.error("the user access key rotation failed with ".format(e))
        logging.error("the user with the name {} cannot be found ".format(username))


