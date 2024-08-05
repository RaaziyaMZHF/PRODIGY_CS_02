from PIL import Image
import numpy as np
import random
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox


def load_image(image_path):
    return Image.open(image_path)


def save_image(image, path):
    image.save(path)


def swap_pixels(image_array):
    x1, y1 = random.randint(0, image_array.shape[0] - 1), random.randint(0, image_array.shape[1] - 1)
    x2, y2 = random.randint(0, image_array.shape[0] - 1), random.randint(0, image_array.shape[1] - 1)
    image_array[x1, y1], image_array[x2, y2] = image_array[x2, y2], image_array[x1, y1]
    return image_array


def apply_xor(image_array, key):
    return image_array ^ key


def encrypt_image(image_path, output_path, key):
    image = load_image(image_path)
    image_array = np.array(image)
    # Apply pixel manipulation
    image_array = swap_pixels(image_array)
    image_array = apply_xor(image_array, key)
    encrypted_image = Image.fromarray(image_array)
    save_image(encrypted_image, output_path)


def decrypt_image(encrypted_path, output_path, key):
    encrypted_image = load_image(encrypted_path)
    encrypted_array = np.array(encrypted_image)
    # Reverse the XOR operation
    decrypted_array = apply_xor(encrypted_array, key)
    # Assuming you swap pixels in reverse manner (need to implement reverse swapping)
    decrypted_image = Image.fromarray(decrypted_array)
    save_image(decrypted_image, output_path)


def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    operation = simpledialog.askstring("Operation", "Enter 'encrypt' to encrypt or 'decrypt' to decrypt:")
    if operation not in ["encrypt", "decrypt"]:
        messagebox.showerror("Error", "Invalid operation selected.")
        return

    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if not image_path:
        messagebox.showerror("Error", "No image selected.")
        return

    output_path = filedialog.asksaveasfilename(title="Save Image As", defaultextension=".png", filetypes=[("Image files", "*.png")])
    if not output_path:
        messagebox.showerror("Error", "No output path specified.")
        return

    key = simpledialog.askinteger("Key", "Enter encryption/decryption key (integer):")
    if key is None:
        messagebox.showerror("Error", "No key specified.")
        return

    try:
        if operation == "encrypt":
            encrypt_image(image_path, output_path, key)
            messagebox.showinfo("Success", "Image encrypted successfully.")
        elif operation == "decrypt":
            decrypt_image(image_path, output_path, key)
            messagebox.showinfo("Success", "Image decrypted successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    main()
