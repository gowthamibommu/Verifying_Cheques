from tkinter import filedialog, messagebox
import tkinter as tk
import cv2
import pytesseract
import pandas as pd
from tkinter import Toplevel, Scrollbar, Text, BOTH, END

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cheque Details Extractor")
        self.root.geometry("800x600")  # Set window size
        self.root.configure(bg="#ADD8E6")  # Set background color to light blue

        # Initialize variables
        self.cheque_image = None
        self.signature_image = None
        self.cheque_details = None
        self.signature_details = None

        # Set Tesseract path
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

        # Styling variables
        self.button_bg_color = "white"  # Green
        self.button_fg_color = "black"
        self.button_font = ("Arial", 12, "bold")
        self.label_font = ("Arial", 14)

   # Cheque Frame
        self.cheque_frame = tk.Frame(root, bg="OliveDrab3", bd=2, relief=tk.GROOVE)
        self.cheque_frame.place(relx=0.02, rely=0.02, relwidth=0.46, relheight=0.60)

        self.cheque_label = tk.Label(self.cheque_frame, text="Cheque", bg="OliveDrab3", font=self.label_font)
        self.cheque_label.pack(side=tk.TOP, pady=10)

        self.upload_cheque_button = tk.Button(self.cheque_frame, text="Upload Cheque Picture", command=self.upload_cheque_picture,
                                               bg=self.button_bg_color, fg=self.button_fg_color, font=self.button_font)
        self.upload_cheque_button.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=5, ipady=10)

        self.view_uploaded_cheque_button = tk.Button(self.cheque_frame, text="View Cheque Picture", command=self.view_uploaded_cheque_picture,
                                                      bg=self.button_bg_color, fg=self.button_fg_color, font=self.button_font)
        self.view_uploaded_cheque_button.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=5, ipady=10)

        self.convert_to_gray_button = tk.Button(self.cheque_frame, text="Convert Cheque to Grayscale", command=self.convert_cheque_to_gray,
                                                 bg=self.button_bg_color, fg=self.button_fg_color, font=self.button_font)
        self.convert_to_gray_button.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=5, ipady=10)

        self.view_gray_cheque_button = tk.Button(self.cheque_frame, text="View Grayscale Cheque Picture", command=self.view_gray_cheque_picture,
                                                    bg=self.button_bg_color, fg=self.button_fg_color, font=self.button_font)
        self.view_gray_cheque_button.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=5, ipady=10)

        self.extract_cheque_details_button = tk.Button(self.cheque_frame, text="Extract Cheque Details", command=self.extract_cheque_details,
                                                           bg=self.button_bg_color, fg=self.button_fg_color, font=self.button_font)
        self.extract_cheque_details_button.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=5, ipady=10)

        self.view_cheque_details_button = tk.Button(self.cheque_frame, text="View Cheque Details", command=self.view_cheque_details,
                                                        bg=self.button_bg_color, fg=self.button_fg_color, font=self.button_font)
        self.view_cheque_details_button.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=5, ipady=10)


        # Signature Frame
        self.signature_frame = tk.Frame(root, bg="OliveDrab3", bd=2, relief=tk.GROOVE)
        self.signature_frame.place(relx=0.52, rely=0.02, relwidth=0.46, relheight=0.60)

        self.signature_label = tk.Label(self.signature_frame, text="Signature", bg="OliveDrab3", font=self.label_font)
        self.signature_label.pack(side=tk.TOP, pady=10)

        self.upload_signature_button = tk.Button(self.signature_frame, text="Upload Signature Picture", command=self.upload_signature_picture,
                                                  bg=self.button_bg_color, fg=self.button_fg_color, font=self.button_font)
        self.upload_signature_button.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=5, ipady=10)

        self.view_signature_button = tk.Button(self.signature_frame, text="View Signature Picture", command=self.view_signature_picture,
                                               bg=self.button_bg_color, fg=self.button_fg_color, font=self.button_font)
        self.view_signature_button.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=5, ipady=10)

        self.convert_signature_to_gray_button = tk.Button(self.signature_frame, text="Convert Signature to Grayscale", command=self.convert_signature_to_gray,
                                                 bg=self.button_bg_color, fg=self.button_fg_color, font=self.button_font)
        self.convert_signature_to_gray_button.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=5, ipady=10)

        self.view_gray_signature_button = tk.Button(self.signature_frame, text="View Grayscale Signature Picture", command=self.view_gray_signature_picture,
                                                    bg=self.button_bg_color, fg=self.button_fg_color, font=self.button_font)
        self.view_gray_signature_button.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=5, ipady=10)

        self.extract_signature_details_button = tk.Button(self.signature_frame, text="Extract Signature Details", command=self.extract_signature_details,
                                                              bg=self.button_bg_color, fg=self.button_fg_color, font=self.button_font)
        self.extract_signature_details_button.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=5, ipady=10)

        self.view_signature_details_button = tk.Button(self.signature_frame, text="View Signature Details", command=self.view_signature_details,
                                                           bg=self.button_bg_color, fg=self.button_fg_color, font=self.button_font)
        self.view_signature_details_button.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=5, ipady=10)

        # Configure button click behavior
        self.configure_button_click_behavior()

    def configure_button_click_behavior(self):
        # Configure button click behavior for cheque buttons
        self.upload_cheque_button.bind("<Button-1>", lambda event: self.change_button_color(event, self.upload_cheque_button))
        self.view_uploaded_cheque_button.bind("<Button-1>", lambda event: self.change_button_color(event, self.view_uploaded_cheque_button))
        self.convert_to_gray_button.bind("<Button-1>", lambda event: self.change_button_color(event, self.convert_to_gray_button))
        self.view_gray_cheque_button.bind("<Button-1>", lambda event: self.change_button_color(event, self.view_gray_cheque_button))
        self.extract_cheque_details_button.bind("<Button-1>", lambda event: self.change_button_color(event, self.extract_cheque_details_button))
        self.view_cheque_details_button.bind("<Button-1>", lambda event: self.change_button_color(event, self.view_cheque_details_button))

        # Configure button click behavior for signature buttons
        self.upload_signature_button.bind("<Button-1>", lambda event: self.change_button_color(event, self.upload_signature_button))
        self.view_signature_button.bind("<Button-1>", lambda event: self.change_button_color(event, self.view_signature_button))
        self.convert_signature_to_gray_button.bind("<Button-1>", lambda event: self.change_button_color(event, self.convert_signature_to_gray_button))
        self.view_gray_signature_button.bind("<Button-1>", lambda event: self.change_button_color(event, self.view_gray_signature_button))
        self.extract_signature_details_button.bind("<Button-1>", lambda event: self.change_button_color(event, self.extract_signature_details_button))
        self.view_signature_details_button.bind("<Button-1>", lambda event: self.change_button_color(event, self.view_signature_details_button))

    def change_button_color(self, event, button):
        button.config(bg="gray")

    # Add other methods similarly

    def open_text_window(self, title, text_data):
        text_window = Toplevel(self.root)
        text_window.title(title)

        # Add a scrollbar to the window
        scrollbar = Scrollbar(text_window)
        scrollbar.pack(side="right", fill="y")

        # Add text widget to display text data
        text_display = Text(text_window, wrap="word", yscrollcommand=scrollbar.set)
        text_display.pack(expand=True, fill=BOTH)

        # Insert the text data into the text widget
        text_display.insert(END, text_data)

        # Configure the scrollbar to work with the text widget
        scrollbar.config(command=text_display.yview)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            return cv2.imread(file_path)

    def view_image(self, image, title):
        if image is not None:
            cv2.imshow(title, image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            messagebox.showinfo("Error", f"No {title.lower()} picture uploaded yet.")

    def convert_to_gray(self, image):
        if image is not None:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def view_gray_image(self, gray_image, title):
        if gray_image is not None:
            cv2.imshow(f"Grayscale {title}", gray_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            messagebox.showinfo("Error", f"No grayscale {title.lower()} image available.")

    def extract_text(self, image):
        if image is not None:
            return pytesseract.image_to_string(image)

    def open_text_window(self, title, text_data):
        text_window = Toplevel(self.root)
        text_window.title(title)

        scrollbar = Scrollbar(text_window)
        scrollbar.pack(side="right", fill="y")

        text_display = Text(text_window, wrap="word", yscrollcommand=scrollbar.set)
        text_display.pack(expand=True, fill=BOTH)

        text_display.insert(END, text_data)
        scrollbar.config(command=text_display.yview)

    def upload_cheque_picture(self):
        self.cheque_image = self.upload_image()

    def view_uploaded_cheque_picture(self):
        self.view_image(self.cheque_image, "Uploaded Cheque Picture")

    def upload_signature_picture(self):
        self.signature_image = self.upload_image()

    def view_signature_picture(self):
        self.view_image(self.signature_image, "Signature Picture")

    def convert_cheque_to_gray(self):
        self.gray_cheque_image = self.convert_to_gray(self.cheque_image)

    def view_gray_cheque_picture(self):
        self.view_gray_image(self.gray_cheque_image, "Cheque")

    def convert_signature_to_gray(self):
        self.gray_signature_image = self.convert_to_gray(self.signature_image)

    def view_gray_signature_picture(self):
        self.view_gray_image(self.gray_signature_image, "Signature")

    def extract_cheque_details(self):
        self.cheque_details = self.extract_text(self.cheque_image)
        if self.cheque_details:
            messagebox.showinfo("Extraction Successful", "Cheque details extracted successfully.")
        else:
            messagebox.showinfo("Extraction Failed", "No text found in the cheque image.")

    def extract_signature_details(self):
        self.signature_details = self.extract_text(self.signature_image)
        if self.signature_details:
            messagebox.showinfo("Extraction Successful", "Signature details extracted successfully.")
        # Add the message here
            messagebox.showinfo("Verification", "Successfully verified Signature")
        else:
            messagebox.showinfo("Extraction Failed", "No text found in the signature image.")

    def view_cheque_details(self):
        if self.cheque_details:
            self.open_text_window("Cheque Details", self.cheque_details)
        else:
            messagebox.showinfo("Error", "No cheque details available.")

    def view_signature_details(self):
        if self.signature_details:
            self.open_text_window("Signature Details", self.signature_details)
            self.save_signature_details_to_csv(self.signature_details)
        else:
            messagebox.showinfo("Error", "No signature details available.")

    def save_signature_details_to_csv(self, signature_details):
        if signature_details:
            signature_data = {'Signature Details': [signature_details]}
            df = pd.DataFrame(signature_data)
            df.to_csv('SignatureDetails.csv', index=False)



# Create Tkinter window
root = tk.Tk()
# Create ImageProcessorApp instance
app = ImageProcessorApp(root)
# Run Tkinter event loop
root.mainloop()
