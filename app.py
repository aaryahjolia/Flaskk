from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    df = pd.read_csv(file)
    device_efficiency = df.groupby('Device_id')['On_time'].sum() / df.groupby('Device_id')['Total_rotations'].sum()
    average_rpm = df.groupby('Device_id')['RPM'].mean()

    # Plot device efficiency
    plt.figure(figsize=(10, 6))
    device_efficiency.plot(kind='bar')
    plt.xlabel('Device ID')
    plt.ylabel('Efficiency')
    plt.title('Device-wise Efficiency')
    plt.tight_layout()

    # Save the plot to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the image as base64
    image_base64 = base64.b64encode(buffer.read()).decode()

    plt.close()

    return render_template('result.html', image=image_base64, average_rpm=average_rpm)

if __name__ == '__main__':
    app.run(debug=False)
