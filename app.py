import streamlit as st
import pandas as pd
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Initialize logs
mouse_log = []
keyboard_log = []
app_log = []
screenshot_log = []
stop_flag = False

# Function to take a screenshot using Selenium with Headless Chrome
def capture_screenshot_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280x1024")

    driver = webdriver.Chrome(options=chrome_options)

    # Open a webpage or any URL you want to capture
    driver.get("https://www.example.com")

    # Take screenshot
    timestamp = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
    screenshot_path = f"screenshot_{timestamp}.png"
    driver.save_screenshot(screenshot_path)

    # Add to log
    screenshot_log.append((timestamp, screenshot_path))

    driver.quit()

# Function to log active application (mocked for demo purposes)
def log_active_app():
    global stop_flag
    while not stop_flag:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        app_log.append((timestamp, "Mocked Active Window"))  # Mocked example
        time.sleep(5)

# Function to generate a summary
def generate_task_summary():
    with open('task_summary.md', 'w') as f:
        f.write("# Task Capture Summary\n\n")
        f.write("## Application Usage\n")
        for entry in app_log:
            f.write(f"{entry[0]} - Active Window: {entry[1]}\n")

        f.write("\n## Screenshots\n")
        for entry in screenshot_log:
            f.write(f"{entry[0]} - Screenshot Path: {entry[1]}\n")

# Streamlit visualization
def visualize_logs():
    # Convert logs to DataFrames
    app_df = pd.DataFrame(app_log, columns=['Timestamp', 'Active Window'])
    screenshot_df = pd.DataFrame(screenshot_log, columns=['Timestamp', 'Screenshot Path'])

    # Streamlit app
    st.title("Task Capture Visualization")

    st.subheader("Active Applications")
    st.write(app_df)

    st.subheader("Screenshots")
    st.write(screenshot_df)
    for path in screenshot_df['Screenshot Path']:
        st.image(path)

# Main function to start capturing tasks
def main():
    global stop_flag
    capture_duration = 60  # Run for 60 seconds

    st.write("Starting task capture for 60 seconds...")

    # Start logging active applications in a separate thread
    app_thread = threading.Thread(target=log_active_app)
    app_thread.start()

    # Start capturing screenshots
    screenshot_thread = threading.Thread(target=capture_screenshot_selenium)
    screenshot_thread.start()

    # Run for the specified duration and then stop
    time.sleep(capture_duration)
    stop_flag = True  # Set the flag to stop the thread

    # Wait for threads to complete
    app_thread.join()
    screenshot_thread.join()

    st.write("Task capture completed. Generating summary and visualization...")

    # Generate a task summary
    generate_task_summary()

    # Visualize logs using Streamlit
    visualize_logs()

if __name__ == "__main__":
    main()
