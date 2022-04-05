from flask import Flask, request
import pool
import numpy as np
from sprite import Ball
app = Flask(__name__)

@app.route("/path", methods=['POST'])
def path():
    if request.method == 'POST':
        balls_json = request.get_json()
        mball = None
        tballs = []
        for i in balls_json:
            ball_pos = balls_json[i]
            if i == "0":
                mball = Ball(np.matrix(ball_pos))
            else:
                tballs.append(Ball(np.matrix(ball_pos)))
        return pool.pool(mball, tballs, 4, 3)
if __name__ == '__main__':
    app.run()