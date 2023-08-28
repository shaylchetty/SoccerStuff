from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import shutil

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    video_file = request.files['video']

    if video_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded video to a temporary location
    video_path = os.path.join('uploads', video_file.filename)
    video_file.save(video_path)

    # Process the video (replace this with your processing logic)
    processed_video_path = process_video(video_path)

    return jsonify({'processedVideoUrl': processed_video_path})


def process_video(video_path):
    # Replace this with your video processing logic
    # You can use libraries like OpenCV to manipulate videos
    # For demonstration purposes, let's assume we are just copying the video
    processed_video_path = 'processed_videos/processed.mp4'
    os.makedirs(os.path.dirname(processed_video_path), exist_ok=True)
    shutil.copy(video_path, processed_video_path)
    return processed_video_path


if __name__ == '__main__':
    app.run(debug=True)
