from flask import Flask, request
import pool
import numpy as np
from sprite import Ball
import json
import cv
app = Flask(__name__)

@app.route("/path", methods=['POST', 'GET'])
def path():
    balls_json = None
    if request.method == 'POST':
        balls_json = request.get_json()
    elif request.method == 'GET':
        balls_json = cv.main()
    
    if type(balls_json) == str:
        balls_json = json.loads(balls_json)
        mball = None
        tballs = []
        for i in balls_json:
            ball_pos = balls_json.get(i)
            if i == "0":
                mball = Ball(np.matrix(ball_pos))
            else:
                tballs.append(Ball(np.matrix(ball_pos)))
        return pool.pool(mball, tballs, 4, 1)
    return "BAD", 400

if __name__ == '__main__':
    app.run('0.0.0.0', 5555)