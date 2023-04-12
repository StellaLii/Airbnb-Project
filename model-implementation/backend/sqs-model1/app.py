import json
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import pickle
import pandas as pd
from haversine import haversine, Unit
import rtree.index
import numpy as np
import boto3
import uuid


def feature_extrapolation_warning(array):
    if len(array) != 4:
        return
    var = ['accommodates', 'bedrooms', 'beds', 'bathrooms_number']
    inputs = {k: v for k, v in zip(var, array)}
    quantile = {k: v for k, v in zip(var, array)}
    # print(inputs)
    for i in var:
        quantile[i] = len(df_train[df_train[i] < inputs[i]]) / 3685

    warning_message = 'Extrapolation Warning: By comparing with other Airbnb Vancouver listings, the listing you input may have the following aspects that may be a bit unusual.'
    warning_flag = False
    for i in var:
        if quantile[i] > 0.8 or inputs[i] <= 0:
            warning_flag = True
            warning_message += str(' Your ' + i +  ' has a quantile of ' + str(round(quantile[i]*100,2)) + '%.')
    if not warning_flag:
        return ""
    else:
        return warning_message


def price_prediction_warning(price):
    price_q = len(df_train[df_train['price'] < price]) / 3685

    if price >= 310 or price < 59.4:
        warning_message = 'Prediction Confidence Warning: By comparing with existing Airbnb Vancouver listings price, this prediction may not be supported by sufficient available data. '
        # warning_message += str('This prediciton has a quantile of ' + str(price_q*100) + '%')
        return warning_message
    else:
        return ""

def insert_into_index(row):
    coord = (row['longitude'], row['latitude'], row['longitude'], row['latitude'])
    idx.insert(row.name, coord)


def find_average_nearest_price_rental(coords, idx, test = True, k=5):
    lat, lon = coords
    search_radius = 0.001
    nearest = []
    it = 0
    while len(nearest) < k and it < 5:
        bounds = (lon - search_radius, lat - search_radius, lon + search_radius, lat + search_radius)
        nearest = list(idx.intersection(bounds))
        search_radius *= 2
        it+=1
    # print(nearest)

    nearest_distances = [haversine(coords, (df.loc[i]['latitude'], df.loc[i]['longitude'])) for i in nearest]
    nearest_rows = df.loc[nearest].copy()
    nearest_rows['distance'] = nearest_distances
    nearest_rows.sort_values(by='distance', inplace=True)
    nearest_rows = nearest_rows.head(k)
    average_price = nearest_rows['price'].mean()
    return average_price


def find_average_nearest_price(coords, idx, test = True, k=2):
    lat, lon = coords
    search_radius = 0.001
    nearest = []
    it = 0
    while len(nearest) < k and it < 2:
        bounds = (lon - search_radius, lat - search_radius, lon + search_radius, lat + search_radius)
        nearest = list(idx.intersection(bounds))
        search_radius *= 2
        it+=1
    # print(nearest)

    nearest_distances = [haversine(coords, (df.loc[i]['latitude'], df.loc[i]['longitude'])) for i in nearest]
    nearest_rows = df.loc[nearest].copy()
    nearest_rows['distance'] = nearest_distances
    nearest_rows.sort_values(by='distance', inplace=True)
    nearest_rows = nearest_rows.head(k)
    if test:
        std = nearest_rows['price'].std()
        if std < 30:
            average_price = nearest_rows['price'].mean()
        else:
            average_price = np.nan
    else: 
        average_price = nearest_rows['price'].mean()
    return average_price

def handler(mylist, bool_flag):
    # Extract information from the event object
    if not bool_flag:
        with open('rf01.sav', 'rb') as f:
            model = pickle.load(f)
    if bool_flag:
        with open('rf02.sav', 'rb') as f:
            model = pickle.load(f)

    X_test = np.array(mylist)
    X_test = X_test.reshape((1, -1))
    y_predict = model.predict(X_test)
    y_predict = np.array2string(y_predict)
    y_predict = y_predict[1:-1]
    return y_predict


if __name__ == "__main__":
    df_train_x = pd.read_csv('preprocessed_X_train.csv', sep=',')
    df_train_y = pd.read_csv('preprocessed_y_train.csv', sep=',')

    df_train = pd.concat([df_train_x, df_train_y], axis=1)

    df = df_train
    idx = rtree.index.Index()

    df.apply(insert_into_index, axis=1)
    
    rental = pd.read_csv("craiglist.csv",encoding='cp1252')
    rental['price'] = rental['price'].str.replace(',','').astype(float)
    rental = rental.dropna()


    session = boto3.Session(
            aws_access_key_id="your key id",
            aws_secret_access_key="your access key",
            region_name='region'
        )
    sqs = session.client('sqs')
    queue_url = 'fifo sender url'

    response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )
    print(response)
    if 'Messages' in response:
        message = response['Messages'][0]
        message_lst = eval(message['Body'])
        latitude = message_lst[0]
        longitude = message_lst[14]
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )


        avg_price_8 = find_average_nearest_price((latitude, longitude), idx, True, 8)
        df = rental
        idx2 = rtree.index.Index()
        df.apply(insert_into_index, axis=1)
        avg_rental = find_average_nearest_price_rental((latitude, longitude), idx2)


        if avg_price_8 is np.nan:
            mylist = message_lst
            result = handler(mylist, False)
            print("0:")
            print(result)
        else:
            mylist = message_lst
            mylist.append(avg_price_8)
            result = handler(mylist, True)
            print("1:")
            print(result)

        arr = [message_lst[3],message_lst[4],message_lst[5],message_lst[10]]
        prc_warn = price_prediction_warning(float(result))
        ftr_warn = feature_extrapolation_warning(arr)
        res_lst = [result, prc_warn, ftr_warn, avg_rental]
        response = sqs.send_message(
                    QueueUrl='fifo receiver url',
                    MessageBody=str(res_lst),
                    MessageGroupId='message_group_2',
                    MessageDeduplicationId=str(uuid.uuid4())
                )
