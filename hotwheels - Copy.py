import csv
import os
import tkinter as tk
from tkinter import messagebox, colorchooser

FILENAME = 'hotwheels_collection.csv'

# Initialize the listbox as a global variable
listbox = None
displayed_cars = []

def initialize_csv():
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.isfile(FILENAME):
        with open(FILENAME, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HW Number', 'Model Name', 'Year', 'Series', 'Color', 'Condition', 'Value', 'Text Color'])

def add_car(hw_number, model_name, year, series, color, condition, value, text_color):
    """Add a new car to the collection."""
    with open(FILENAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([hw_number, model_name, year, series, color, condition, value, text_color])

def update_car(index, hw_number, model_name, year, series, color, condition, value, text_color):
    """Update an existing car's details in the collection."""
    cars = view_collection()
    if 0 <= index < len(cars):
        cars[index] = [hw_number, model_name, year, series, color, condition, value, text_color]
        with open(FILENAME, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HW Number', 'Model Name', 'Year', 'Series', 'Color', 'Condition', 'Value', 'Text Color'])
            writer.writerows(cars)

def remove_car(index):
    """Remove a car from the collection."""
    cars = view_collection()
    if 0 <= index < len(cars):
        del cars[index]
        with open(FILENAME, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HW Number', 'Model Name', 'Year', 'Series', 'Color', 'Condition', 'Value', 'Text Color'])
            writer.writerows(cars)
        # Update the listbox after removal
        update_car_list()
    else:
        messagebox.showerror("Error", "Invalid car index")

def view_collection():
    """Return the entire collection as a list of lists."""
    cars = []
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        cars = [row for row in reader]
    return cars

def show_categories():
    """Show a list of all categories (unique values in 'Series') in a popup window."""
    cars = view_collection()
    series_list = sorted(set(row[3] for row in cars))
    categories = "\n".join(series_list)
    messagebox.showinfo("Categories", categories)

def show_car_details(car):
    """Show details of the selected car in a popup window."""
    if len(car) >= 7:
        details = (f"HW Number: {car[0]}\nModel: {car[1]}\nYear: {car[2]}\nSeries: {car[3]}\n"
                   f"Color: {car[4]}\nCondition: {car[5]}\nValue: ${car[6]}")
        messagebox.showinfo("Car Details", details)
    else:
        messagebox.showerror("Error", "Incomplete car details")

def update_car_list(filter_text=""):
    """Update the listbox with the current cars in the collection, filtered by search term."""
    global listbox, displayed_cars
    listbox.delete(0, tk.END)
    cars = view_collection()
    filter_text = filter_text.lower()
    displayed_cars = [car for car in cars if filter_text in car[1].lower() or filter_text in car[3].lower()]
    
    for car in displayed_cars:
        listbox.insert(tk.END, f"{car[1]} ({car[2]})")
        # Set the text color based on category, with a fallback if the color is missing
        text_color = car[7] if len(car) > 7 and car[7] else 'black'
        listbox.itemconfig(tk.END, {'fg': text_color})

def main_window():
    """Create the main application window."""
    global listbox
    
    def add_car_gui():
        add_car(entry_hw_number.get(), entry_model_name.get(), entry_year.get(), entry_series.get(), color_var.get(), entry_condition.get(), entry_value.get(), text_color_var.get())
        messagebox.showinfo("Success", "Car added to collection!")
        update_car_list()
        clear_entries()

    def edit_car_gui():
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            update_car(index, entry_hw_number.get(), entry_model_name.get(), entry_year.get(), entry_series.get(), color_var.get(), entry_condition.get(), entry_value.get(), text_color_var.get())
            messagebox.showinfo("Success", "Car details updated!")
            update_car_list()
            clear_entries()

    def remove_car_gui():
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            remove_car(index)
            messagebox.showinfo("Success", "Car removed from collection!")
            clear_entries()
        else:
            messagebox.showerror("Error", "No car selected")

    def save_changes_gui():
        """Save changes to the collection manually."""
        update_car_list()
        messagebox.showinfo("Saved", "Changes saved!")

    def clear_entries():
        entry_hw_number.delete(0, tk.END)
        entry_model_name.delete(0, tk.END)
        entry_year.delete(0, tk.END)
        entry_series.delete(0, tk.END)
        entry_condition.delete(0, tk.END)
        entry_value.delete(0, tk.END)
        color_var.set("")
        text_color_var.set("")

    def on_car_select(event):
        """Event handler for when a car is selected in the listbox."""
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            selected_car = displayed_cars[index]
            if len(selected_car) >= 7:
                # Fill in the entry fields with the selected car's details
                entry_hw_number.delete(0, tk.END)
                entry_hw_number.insert(0, selected_car[0])
                entry_model_name.delete(0, tk.END)
                entry_model_name.insert(0, selected_car[1])
                entry_year.delete(0, tk.END)
                entry_year.insert(0, selected_car[2])
                entry_series.delete(0, tk.END)
                entry_series.insert(0, selected_car[3])
                color_var.set(selected_car[4])
                entry_condition.delete(0, tk.END)
                entry_condition.insert(0, selected_car[5])
                entry_value.delete(0, tk.END)
                entry_value.insert(0, selected_car[6])
                text_color_var.set(selected_car[7] if len(selected_car) > 7 else 'black')
            else:
                messagebox.showerror("Error", "Incomplete car details")

    def search_cars(event=None):
        """Search and update the listbox based on the search entry."""
        search_term = entry_search.get()
        update_car_list(search_term)

    def choose_text_color():
        """Open a color picker and set the selected text color for the category."""
        color_code = colorchooser.askcolor(title="Choose text color for category")[1]
        if color_code:
            text_color_var.set(color_code)

    root = tk.Tk()
    root.title("Hot Wheels Collection Manager")

    # Input fields
    tk.Label(root, text="HW Number").grid(row=0, column=0)
    tk.Label(root, text="Model Name").grid(row=1, column=0)
    tk.Label(root, text="Year").grid(row=2, column=0)
    tk.Label(root, text="Series").grid(row=3, column=0)
    tk.Label(root, text="Color").grid(row=4, column=0)
    tk.Label(root, text="Condition").grid(row=5, column=0)
    tk.Label(root, text="Value ($)").grid(row=6, column=0)

    entry_hw_number = tk.Entry(root)
    entry_model_name = tk.Entry(root)
    entry_year = tk.Entry(root)
    entry_series = tk.Entry(root)
    color_var = tk.StringVar()
    entry_condition = tk.Entry(root)
    entry_value = tk.Entry(root)
    text_color_var = tk.StringVar()

    entry_hw_number.grid(row=0, column=1)
    entry_model_name.grid(row=1, column=1)
    entry_year.grid(row=2, column=1)
    entry_series.grid(row=3, column=1)
    tk.Entry(root, textvariable=color_var).grid(row=4, column=1)
    entry_condition.grid(row=5, column=1)
    entry_value.grid(row=6, column=1)
    tk.Button(root, text="Choose Text Color", command=choose_text_color).grid(row=7, column=1)

    tk.Button(root, text="Add Car", command=add_car_gui).grid(row=8, column=0)
    tk.Button(root, text="Edit Car", command=edit_car_gui).grid(row=8, column=1)
    tk.Button(root, text="Remove Car", command=remove_car_gui).grid(row=8, column=2)
    tk.Button(root, text="Save Changes", command=save_changes_gui).grid(row=8, column=3)

    # Search bar
    tk.Label(root, text="Search").grid(row=9, column=0)
    entry_search = tk.Entry(root)
    entry_search.grid(row=9, column=1)
    entry_search.bind("<KeyRelease>", search_cars)

    # Listbox
    listbox = tk.Listbox(root, width=50, height=15)
    listbox.grid(row=10, column=0, columnspan=4)
    listbox.bind("<<ListboxSelect>>", on_car_select)

    # Categories button
    tk.Button(root, text="Show Categories", command=show_categories).grid(row=11, column=0, columnspan=4)

    # Initialize listbox with car data
    update_car_list()

    root.mainloop()

if __name__ == '__main__':
    initialize_csv()
    main_window()
