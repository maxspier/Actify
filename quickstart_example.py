import os
from openai import OpenAI
import json
import mysql.connector
#from flask import Flask, render_template, request




client = OpenAI(api_key="Your API Key Here")

connection = mysql.connector.connect(
    host="Your DB Host Here",
    user="Your DB User Here",
    password="Your DB Password Here",
    database="Your Database Here",
    port=Your Port Here
)

db_cursor = connection.cursor()

def calculateCalories(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": "You are a fitness helper. The user will give you something they ate. Provide the macros for the meal. Ensure that all data provided to the user is in a JSON format without any formatiing (```). Units should be standard (grams) for everything not calories. Do not include units in the JSON. The fields should be calories, protien, carbohydrates, and fat. Sometimes, a user may give more than one food at a time or a meal. Combine these into one response in the exact same way, totaling the macros from each item."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    x = json.loads(completion.choices[0].message.content)
    return x
    
def updateCalories(user, json):
    db_cursor.execute("SELECT * FROM fitness_users WHERE username like '" + str(user) + "'")
    user_info = db_cursor.fetchall()

    print(str(json))

    caloriesEnding = float(user_info[0][2]) + float(json["calories"])
    proteinEnding = float(user_info[0][3]) + float(json["protein"])
    carbohydratesEnding = float(user_info[0][4]) + float(json["carbohydrates"])
    fatEnding = float(user_info[0][5]) + float(json["fat"])

    db_cursor.execute(
        "UPDATE fitness_users SET calories = %s, protein = %s, carbohydrates = %s, fat = %s WHERE username = %s AND passkey = %s",
        (caloriesEnding, proteinEnding, carbohydratesEnding, fatEnding, user, user)
    )


    connection.commit()

def createUser(name, password):
    db_cursor.execute(
        "INSERT INTO fitness_users (username, passkey) VALUES (%s, %s)",
        (name, password)
    )
    connection.commit()

#@app.route("/")
#def index():
#    return render_template("index.html")

updateCalories("user", calculateCalories("Thomases bagel with cream cheese and onion, and chipotle bowl with white rice, black beans, chicken, hot salsa, mild salsa, corn, lettuce, and side tortilla, and iced matcha latte medium sized with matcha ice cream on top."))


