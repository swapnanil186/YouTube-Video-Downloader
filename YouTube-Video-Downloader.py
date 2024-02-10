import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from pytube import YouTube

def populate_quality_options(event):
    url = url_entry.get()
    if 'youtube.com' in url:
        try:
            yt = YouTube(url)
            video_streams = yt.streams.filter(progressive=True)
            quality_options = [f"{stream.resolution} {stream.subtype}" for stream in video_streams]
            quality_combo['values'] = quality_options
            quality_combo.set(quality_options[0])  # Set default quality
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def browse_download_path():
    path = filedialog.askdirectory()
    if path:
        download_path_entry.delete(0, tk.END)
        download_path_entry.insert(0, path)

def download_video():
    url = url_entry.get()
    try:
        if 'youtube.com' not in url:
            raise ValueError("Invalid YouTube URL")
            
        yt = YouTube(url)
        selected_quality = quality_combo.get().split()[0]  # Extract quality from selected option
        video_stream = yt.streams.filter(res=selected_quality, progressive=True).first()
        
        download_path = download_path_entry.get()
        if not download_path:
            download_path = default_download_path  # Use default path if not specified
        video_stream.download(download_path)
            
        messagebox.showinfo("Success", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Create and pack the URL entry field
url_label = tk.Label(root, text="Paste YouTube Video URL:")
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Bind the <FocusOut> event to populate quality options
url_entry.bind("<FocusOut>", populate_quality_options)

# Quality selection
quality_label = tk.Label(root, text="Select Quality:")
quality_label.pack(pady=5)
quality_combo = ttk.Combobox(root, values=[], width=10)
quality_combo.pack(pady=5)

# Default download path
default_download_path = "C:/Users/Username/Videos"  # Default path
download_path_label = tk.Label(root, text=f"Download Path (Optional, Default: {default_download_path}):")
download_path_label.pack(pady=5)
download_path_entry = tk.Entry(root, width=50)
download_path_entry.pack(pady=5)

# Browse button for selecting download path
browse_button = tk.Button(root, text="Browse", command=browse_download_path)
browse_button.pack(pady=5)

# Create and pack the download button
download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack(pady=5)

# Run the application
root.mainloop()
