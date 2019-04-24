#!/usr/bin/env python

# [START storage_upload_file]
import os
import psycopg2
import re
from google.cloud import storage
import threading

#
# Gets list of images that are already in the database
#
def get_images_list(images_database):
    sql = "SELECT * FROM collected_data"
    conn = None
    try:
        # Read database configuration
        conn = psycopg2.connect(dbname='s1764997', user='s1764997', password='password', host='pgteach', port='5432', sslmode='disable')
        # Create a new cursor
        cur = conn.cursor()
        # Execute the INSERT statement
        cur.execute(sql)
        records = cur.fetchall()
        
        # Store data (id, image name) from the database into lists
        for row in records:
            if (row[4]):
                images_database.append("images/object_" + str(row[0]) + ".png")
                ids_database.append(row[0])

        # Close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return images_database

#
# Downloads only new images from the bucket.
# These are stored in the bucket but not on the webserver and in the database 
#
def download_images(blobs, images_database, new_images):
    for blob in blobs:
        if (blob.name not in images_database and blob.name != "images/"):
            res = re.search('_(.+?).', blob.name)
            if res:
                image_id = res.group(1)
            
            filename = "image_" + str(image_id) + ".png"    
            blob.download_to_filename(dl_dir + filename)

            new_images.append(filename)
            images_ids.append(image_id)
            
    return new_images

#
# Inserts new images into database
#
def insert_new_images_to_database(new_images, images_ids):
    try:
        # Read database configuration
        conn = psycopg2.connect(dbname='s1764997', user='s1764997', password='password', host='pgteach', port='5432', sslmode='disable')
        cur = conn.cursor()
        ind = 0
        for image in new_images:
            img_id = images_ids[ind]
            
            sql = """UPDATE collected_data SET image_link= %s WHERE object_id= %s"""
            cur.execute(sql, (image, img_id))
            conn.commit()

            ind = ind+1
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def update_images():
    # Get blobs from the Google Cloud bucket
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name=bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)

    #initialise_variables()
    images_database = []
    ids_database = []
    new_images = []
    images_ids = []

    # Retrieve image IDs and names from the database
    images_database = get_images_list(images_database)
    #print(images_database, ids_database)
    # Download images that are in the bucket but not in the database (only their image link is missing)
    new_images = download_images(blobs, images_database, new_images)
    #print('New images', new_images)
    # Insert downloaded images (only their image link) into database
    insert_new_images_to_database(new_images, images_ids)
    print(new_images, images_ids)

    threading.Timer(10.0, update_images).start()


# Set credentials for using Google Cloud API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/afs/inf.ed.ac.uk/group/teaching/sdp/sdp5/html/credentials.json"

# Set configurations
bucket_name = 'collecteddataset'
prefix = 'images'
dl_dir = '/afs/inf.ed.ac.uk/group/teaching/sdp/sdp5/html/images/'

images_database = []
ids_database = []
new_images = []
images_ids = []

update_images()

