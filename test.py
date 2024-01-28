import tkinter as tk
from tkinter import messagebox, ttk, simpledialog

class PlantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Savings App")

        self.plant_info = {}  # Store information about each plant

        self.create_widgets()
        self.current_plant = None

    def create_widgets(self):
        # Plant selection drop-down
        self.plant_dropdown_label = tk.Label(self.root, text="Select Plant:")
        self.plant_dropdown_label.pack()

        self.plant_var = tk.StringVar()
        self.plant_dropdown = ttk.Combobox(self.root, textvariable=self.plant_var)
        self.plant_dropdown['values'] = list(self.plant_info.keys())
        self.plant_dropdown.pack()

        # Money saved display
        self.money_label = tk.Label(self.root, text="Amount Saved:")
        self.money_label.pack()

        self.money_entry = tk.Entry(self.root, state='readonly')
        self.money_entry.pack()

        # Plant name entry
        self.name_label = tk.Label(self.root, text="Plant Name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        # Save money button
        self.save_button = tk.Button(self.root, text="Save Money", command=self.save_money)
        self.save_button.pack()

        # Plant image display
        self.plant_image = tk.PhotoImage(file="plant.png")  # Add your plant image file path
        self.plant_label = tk.Label(self.root, image=self.plant_image)
        self.plant_label.pack()

    def save_money(self):
        try:
            amount = int(self.money_entry.get())
            if amount > 0:
                if self.current_plant:
                    self.plant_info[self.current_plant]['savings'] += amount
                    self.update_plant_display()
                    messagebox.showinfo("Success", f"${amount} saved successfully for {self.current_plant}!")
                else:
                    messagebox.showwarning("No Plant Selected", "Please select a plant from the drop-down menu.")
            else:
                messagebox.showwarning("Invalid Amount", "Please enter a positive amount to save.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def update_plant_display(self):
        # Update money saved display
        if self.current_plant:
            savings = self.plant_info[self.current_plant]['savings']
            self.money_entry.config(state='normal')
            self.money_entry.delete(0, tk.END)
            self.money_entry.insert(0, f"${savings}")
            self.money_entry.config(state='readonly')

            # Update plant image (you can customize this part based on your plant growth logic)
            growth_factor = 0.1  # Adjust as needed
            new_height = int(savings * growth_factor)
            self.plant_label.config(height=new_height)

    def plant_selected(self, event):
        # Callback when a plant is selected from the drop-down menu
        self.current_plant = self.plant_var.get()
        self.update_plant_display()

    def add_plant(self):
        # Add a new plant to the drop-down menu using a pop-up window
        plant_name = simpledialog.askstring("Add Plant", "Enter Plant Name:")
        if plant_name:
            try:
                goal = simpledialog.askfloat("Add Plant", "Enter Savings Goal for the Plant:")
                if goal is not None and goal >= 0:
                    self.plant_info[plant_name] = {'savings': 0, 'goal': goal}
                    self.plant_dropdown['values'] = list(self.plant_info.keys())
                    self.plant_var.set(plant_name)
                    self.update_plant_display()
                    messagebox.showinfo("Success", f"{plant_name} added successfully!")
                else:
                    messagebox.showwarning("Invalid Goal", "Please enter a valid non-negative savings goal.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for the savings goal.")
        else:
            messagebox.showwarning("Invalid Name", "Please enter a valid plant name.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PlantApp(root)
    
    # Bind the plant_selected callback to the dropdown selection event
    app.plant_dropdown.bind("<<ComboboxSelected>>", app.plant_selected)
    
    # Add a button to add a new plant
    add_plant_button = tk.Button(root, text="Add Plant", command=app.add_plant)
    add_plant_button.pack()

    root.mainloop()
