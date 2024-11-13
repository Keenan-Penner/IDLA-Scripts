import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ctypes import windll
from PIL import Image
from gui_functions import treeplot2d, treeplot3d, multisource2d, multisource3d
import os

windll.shcore.SetProcessDpiAwareness(1)

class MyGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1200x750")
        self.root.title("IDLA simulations")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Notebook setup
        self.label = tk.Label(self.root, text="IDLA simulations", font=("Arial", 20))
        self.label.pack(pady=20, padx=20, expand=False, fill=tk.BOTH, side=tk.TOP)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)

        # Frames setup
        self.frame1 = tk.Frame(self.notebook)
        self.frame2 = tk.Frame(self.notebook)
        self.frame3 = tk.Frame(self.notebook)
        self.frame4 = tk.Frame(self.notebook)

        self.frame1.pack(fill=tk.BOTH, expand=True)
        self.frame2.pack(fill=tk.BOTH, expand=True)
        self.frame3.pack(fill=tk.BOTH, expand=True)
        self.frame4.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.frame1, text="2D Classical IDLA")
        self.notebook.add(self.frame2, text="3D Classical IDLA")
        self.notebook.add(self.frame3, text="2D An[M]")
        self.notebook.add(self.frame4, text="3D An[M]")

        # Label and Inputs
        self.title1 = tk.Label(self.frame1, text="2D Classical IDLA", font=("Arial", 10))
        self.title1.pack(pady=10, padx=20)

        self.title2 = tk.Label(self.frame2, text="3D Classical IDLA", font=("Arial", 10))
        self.title2.pack(pady=10, padx=20)

        self.title3 = tk.Label(self.frame3, text="2D Multi-source IDLA", font=("Arial", 10))
        self.title3.pack(pady=10, padx=20)

        self.title4 = tk.Label(self.frame4, text="3D Multi-source IDLA", font=("Arial", 10))
        self.title4.pack(pady=10, padx=20)
####################################################################################################################
        ### 2D CLASSICAL IDLA ###
        self.frame1_box1 = tk.Label(self.frame1)
        self.frame1_box1.pack(pady=50, padx=20)
        self.frame1_box2 = tk.Label(self.frame1)
        self.frame1_box2.pack(pady=50, padx=20)

        self.frame1_L1 = tk.Label(self.frame1_box1, text="Number of particles:")
        self.frame1_L1.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame1_E1 = tk.Entry(self.frame1_box1, bd=5)
        self.frame1_E1.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame1_check_state = tk.IntVar()
        self.frame1_branch_checkbox = tk.Checkbutton(self.frame1_box1, text="Show highlighted branch", variable=self.frame1_check_state)
        self.frame1_branch_checkbox.pack(pady=10, padx=20, side=tk.LEFT)

        # Radiobuttons
        self.frame1_L2 = tk.Label(self.frame1_box2, text="Do you wish to save the figures? ")
        self.frame1_L2.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame1_info = tk.Label(self.frame1, text="Note: If YES is selected, the figures will be saved inside a folder named 'sim//2D//classical' in the current directory")
        self.frame1_info.pack(pady=10, padx=20, expand=False)
        self.frame1_save_state = tk.IntVar()
        self.frame1_save_state.set(0)  # Default is NO

        self.frame1_YES_checkbox = tk.Radiobutton(self.frame1_box2, text="YES", variable=self.frame1_save_state, value=1, command=self.frame1_savefig)
        self.frame1_NO_checkbox = tk.Radiobutton(self.frame1_box2, text="NO", variable=self.frame1_save_state, value=0, command=self.frame1_savefig)

        self.frame1_YES_checkbox.pack(pady=10, padx=20, side=tk.LEFT)
        self.frame1_NO_checkbox.pack(pady=10, padx=20, side=tk.LEFT)

        # Frame to hold the filename entry and label
        self.frame1_filename_frame = tk.Frame(self.frame1)
        self.frame1_filename_frame.pack(pady=20, padx=20, fill=tk.X)

        # Initialize placeholders for filename entry
        self.frame1_entry_label = None
        self.frame1_filename_entry = None

        # Submit button
        self.frame1_submit_btn = tk.Button(self.frame1, text="Submit", command=self.frame1_submit)
        self.frame1_submit_btn.pack(pady=10, padx=20, expand=False)
####################################################################################################################
        ### 3D CLASSICAL IDLA ###
        self.frame2_box1 = tk.Label(self.frame2)
        self.frame2_box1.pack(pady=50, padx=20)
        self.frame2_box2 = tk.Label(self.frame2)
        self.frame2_box2.pack(pady=50, padx=20)

        self.frame2_L1 = tk.Label(self.frame2_box1, text="Number of particles:")
        self.frame2_L1.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame2_E1 = tk.Entry(self.frame2_box1, bd=5)
        self.frame2_E1.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame2_check_state = tk.IntVar()
        self.frame2_branch_checkbox = tk.Checkbutton(self.frame2_box1, text="Show highlighted branch", variable=self.frame2_check_state)
        self.frame2_branch_checkbox.pack(pady=10, padx=20, side=tk.LEFT)

        # Radiobuttons
        self.frame2_L2 = tk.Label(self.frame2_box2, text="Do you wish to save the figures? ")
        self.frame2_L2.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame2_info = tk.Label(self.frame2, text="Note: If YES is selected, the figures will be saved inside a folder named 'sim//2D//classical' in the current directory")
        self.frame2_info.pack(pady=10, padx=20, expand=False)
        self.frame2_save_state = tk.IntVar()
        self.frame2_save_state.set(0)  # Default is NO

        self.frame2_YES_checkbox = tk.Radiobutton(self.frame2_box2, text="YES", variable=self.frame2_save_state, value=1, command=self.frame2_savefig)
        self.frame2_NO_checkbox = tk.Radiobutton(self.frame2_box2, text="NO", variable=self.frame2_save_state, value=0, command=self.frame2_savefig)

        self.frame2_YES_checkbox.pack(pady=10, padx=20, side=tk.LEFT)
        self.frame2_NO_checkbox.pack(pady=10, padx=20, side=tk.LEFT)

        # Frame to hold the filename entry and label
        self.frame2_filename_frame = tk.Frame(self.frame2)
        self.frame2_filename_frame.pack(pady=20, padx=20, fill=tk.X)

        # Initialize placeholders for filename entry
        self.frame2_entry_label = None
        self.frame2_filename_entry = None

        # Submit button
        self.frame2_submit_btn = tk.Button(self.frame2, text="Submit", command=self.frame2_submit)
        self.frame2_submit_btn.pack(pady=10, padx=20, expand=False)
####################################################################################################################
        ### 2D MULTISOURCE IDLA ###
        self.frame3_box1 = tk.Label(self.frame3)
        self.frame3_box1.pack(pady=50, padx=20)
        self.frame3_box2 = tk.Label(self.frame3)
        self.frame3_box2.pack(pady=50, padx=20)

        self.frame3_L1 = tk.Label(self.frame3_box1, text="Number of particles per site n:")
        self.frame3_L1.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame3_E1 = tk.Entry(self.frame3_box1, bd=5)
        self.frame3_E1.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame3_L2 = tk.Label(self.frame3_box1, text="Value of level M:")
        self.frame3_L2.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame3_E2 = tk.Entry(self.frame3_box1, bd=5)
        self.frame3_E2.pack(pady=10, padx=20, expand=False, side=tk.LEFT)

        # Radiobuttons
        self.frame3_L3 = tk.Label(self.frame3_box2, text="Do you wish to save the figures? ")
        self.frame3_L3.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame3_info = tk.Label(self.frame3, text="Note: If YES is selected, the figure will be saved inside a folder named 'sim//2D//multisource' in the current directory")
        self.frame3_info.pack(pady=10, padx=20, expand=False)
        self.frame3_save_state = tk.IntVar()
        self.frame3_save_state.set(0)  # Default is NO

        self.frame3_YES_checkbox = tk.Radiobutton(self.frame3_box2, text="YES", variable=self.frame3_save_state, value=1, command=self.frame3_savefig)
        self.frame3_NO_checkbox = tk.Radiobutton(self.frame3_box2, text="NO", variable=self.frame3_save_state, value=0, command=self.frame3_savefig)

        self.frame3_YES_checkbox.pack(pady=10, padx=20, side=tk.LEFT)
        self.frame3_NO_checkbox.pack(pady=10, padx=20, side=tk.LEFT)

        # Frame to hold the filename entry and label
        self.frame3_filename_frame = tk.Frame(self.frame3)
        self.frame3_filename_frame.pack(pady=20, padx=20, fill=tk.X)

        # Initialize placeholders for filename entry
        self.frame3_entry_label = None
        self.frame3_filename_entry = None

        # Submit button
        self.frame3_submit_btn = tk.Button(self.frame3, text="Submit", command=self.frame3_submit)
        self.frame3_submit_btn.pack(pady=10, padx=20, expand=False)
####################################################################################################################
        ### 3D MULTISOURCE IDLA ###
        self.frame4_box1 = tk.Label(self.frame4)
        self.frame4_box1.pack(pady=50, padx=20)
        self.frame4_box2 = tk.Label(self.frame4)
        self.frame4_box2.pack(pady=50, padx=20)

        self.frame4_L1 = tk.Label(self.frame4_box1, text="Number of particles per site n:")
        self.frame4_L1.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame4_E1 = tk.Entry(self.frame4_box1, bd=5)
        self.frame4_E1.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame4_L2 = tk.Label(self.frame4_box1, text="Value of level M:")
        self.frame4_L2.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame4_E2 = tk.Entry(self.frame4_box1, bd=5)
        self.frame4_E2.pack(pady=10, padx=20, expand=False, side=tk.LEFT)

        # Radiobuttons
        self.frame4_L3 = tk.Label(self.frame4_box2, text="Do you wish to save the figures? ")
        self.frame4_L3.pack(pady=10, padx=20, expand=False, side=tk.LEFT)
        self.frame4_info = tk.Label(self.frame4, text="Note: If YES is selected, the figure will be saved inside a folder named 'sim//2D//multisource' in the current directory")
        self.frame4_info.pack(pady=10, padx=20, expand=False)
        self.frame4_save_state = tk.IntVar()
        self.frame4_save_state.set(0)  # Default is NO

        self.frame4_YES_checkbox = tk.Radiobutton(self.frame4_box2, text="YES", variable=self.frame4_save_state, value=1, command=self.frame4_savefig)
        self.frame4_NO_checkbox = tk.Radiobutton(self.frame4_box2, text="NO", variable=self.frame4_save_state, value=0, command=self.frame4_savefig)

        self.frame4_YES_checkbox.pack(pady=10, padx=20, side=tk.LEFT)
        self.frame4_NO_checkbox.pack(pady=10, padx=20, side=tk.LEFT)

        # Frame to hold the filename entry and label
        self.frame4_filename_frame = tk.Frame(self.frame4)
        self.frame4_filename_frame.pack(pady=20, padx=20, fill=tk.X)

        # Initialize placeholders for filename entry
        self.frame4_entry_label = None
        self.frame4_filename_entry = None

        # Submit button
        self.frame4_submit_btn = tk.Button(self.frame4, text="Submit", command=self.frame4_submit)
        self.frame4_submit_btn.pack(pady=10, padx=20, expand=False)

        self.root.mainloop()

    def on_close(self):
        """This method is called when the window close button is clicked."""
        print("Closing the application...")
        self.root.quit()  # Ends the mainloop and closes the application
        self.root.destroy()  # Destroys the Tkinter root window
####################################################################################################################
    def frame1_savefig(self):
        """Called when the save_state changes (YES or NO is selected)."""
        choice = self.frame1_save_state.get()  # 1 for YES, 0 for NO
        #print(f"Selected option: {'YES' if choice == 1 else 'NO'}")
        # If "YES" is selected, show the filename entry widget
        if choice == 1:
            if not self.frame1_entry_label:  # Create only once if it doesn't exist
                self.frame1_entry_label = tk.Label(self.frame1_filename_frame, text="Enter a file name: ")
                self.frame1_entry_label.pack(pady=10, padx=20, expand=False)

                self.frame1_filename_entry = tk.Entry(self.frame1_filename_frame, bd=5)
                self.frame1_filename_entry.pack(pady=10, padx=20, expand=False)
        else:
            # If "NO" is selected, hide the filename entry widget
            if self.frame1_entry_label:
                self.frame1_entry_label.pack_forget()
                self.frame1_filename_entry.pack_forget()
                self.frame1_entry_label = None
                self.frame1_filename_entry = None

    def frame1_submit(self):
        self.frame1_filename = self.frame1_filename_entry.get() if self.frame1_filename_entry else None
        #print(self.frame1_filename)
        if self.frame1_save_state.get() == 1 and not self.frame1_filename:
            messagebox.showerror("Error", "Please enter a valid file name!")
            return
        #print(f"Saving file with name: {self.frame1_filename}")
        # Simulate treeplot processing here
        branch_active = self.frame1_check_state.get()
        savepath = f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\GUI\\sim\\2D\\classical\\{self.frame1_filename}"
        self.frame1_particle_num = self.frame1_E1.get() if self.frame1_E1 else None
        if not self.frame1_particle_num:
            messagebox.showerror("Error", "Please enter a valid number of particles")
            return
        self.frame1_particle_num = int(self.frame1_E1.get())
        self.frame1_branch_active = branch_active
        self.frame1_savepath = savepath
        #print(f"Number of particles: {self.frame1_particle_num}")
        #print(f"Show highlighted branch: {self.frame1_branch_active}")
        #print(f"Save path: {self.frame1_savepath}")
        treeplot2d(self.frame1_particle_num, self.frame1_branch_active, self.frame1_savepath)
        agg_img = Image.open(f'{self.frame1_savepath}_agg.png')
        tree_img = Image.open(f'{self.frame1_savepath}_tree.png')
        agg_img.show()
        tree_img.show()
        if self.frame1_save_state.get() == 0:
            os.remove(f'{self.frame1_savepath}_agg.png')
            os.remove(f'{self.frame1_savepath}_tree.png')
####################################################################################################################
    def frame2_savefig(self):
        """Called when the save_state changes (YES or NO is selected)."""
        choice = self.frame2_save_state.get()  # 1 for YES, 0 for NO
        #print(f"Selected option: {'YES' if choice == 1 else 'NO'}")
        # If "YES" is selected, show the filename entry widget
        if choice == 1:
            if not self.frame2_entry_label:  # Create only once if it doesn't exist
                self.frame2_entry_label = tk.Label(self.frame2_filename_frame, text="Enter a file name: ")
                self.frame2_entry_label.pack(pady=10, padx=20, expand=False)

                self.frame2_filename_entry = tk.Entry(self.frame2_filename_frame, bd=5)
                self.frame2_filename_entry.pack(pady=10, padx=20, expand=False)
        else:
            # If "NO" is selected, hide the filename entry widget
            if self.frame2_entry_label:
                self.frame2_entry_label.pack_forget()
                self.frame2_filename_entry.pack_forget()
                self.frame2_entry_label = None
                self.frame2_filename_entry = None

    def frame2_submit(self):
        self.frame2_filename = self.frame2_filename_entry.get() if self.frame2_filename_entry else None
        #print(self.frame2_filename)
        if self.frame2_save_state.get() == 1 and not self.frame2_filename:
            messagebox.showerror("Error", "Please enter a valid file name!")
            return
        #print(f"Saving file with name: {self.frame2_filename}_agg.png")
        # Simulate treeplot processing here
        branch_active = self.frame2_check_state.get()
        savepath = f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\GUI\\sim\\2D\\classical\\{self.frame2_filename}"
        self.frame2_particle_num = self.frame2_E1.get() if self.frame2_E1 else None
        if not self.frame2_particle_num:
            messagebox.showerror("Error", "Please enter a valid number of particles")
            return
        self.frame2_particle_num = int(self.frame2_E1.get())
        self.frame2_branch_active = branch_active
        self.frame2_savepath = savepath
        #print(f"Number of particles: {self.frame2_particle_num}")
        #print(f"Show highlighted branch: {self.frame2_branch_active}")
        #print(f"Save path: {self.frame2_savepath}")
        treeplot3d(self.frame2_particle_num, self.frame2_branch_active, self.frame2_savepath)
        agg_img = Image.open(f'{self.frame2_savepath}_agg.png')
        tree_img = Image.open(f'{self.frame2_savepath}_tree.png')
        agg_img.show()
        tree_img.show()
        if self.frame2_save_state.get() == 0:
            os.remove(f'{self.frame2_savepath}_agg.png')
            os.remove(f'{self.frame2_savepath}_tree.png')
####################################################################################################################
    def frame3_savefig(self):
        """Called when the save_state changes (YES or NO is selected)."""
        choice = self.frame3_save_state.get()  # 1 for YES, 0 for NO
        #print(f"Selected option: {'YES' if choice == 1 else 'NO'}")
        # If "YES" is selected, show the filename entry widget
        if choice == 1:
            if not self.frame3_entry_label:  # Create only once if it doesn't exist
                self.frame3_entry_label = tk.Label(self.frame3_filename_frame, text="Enter a file name: ")
                self.frame3_entry_label.pack(pady=10, padx=20, expand=False)

                self.frame3_filename_entry = tk.Entry(self.frame3_filename_frame, bd=5)
                self.frame3_filename_entry.pack(pady=10, padx=20, expand=False)
        else:
            # If "NO" is selected, hide the filename entry widget
            if self.frame3_entry_label:
                self.frame3_entry_label.pack_forget()
                self.frame3_filename_entry.pack_forget()
                self.frame3_entry_label = None
                self.frame3_filename_entry = None

    def frame3_submit(self):
        self.frame3_filename = self.frame3_filename_entry.get() if self.frame3_filename_entry else None
        #print(self.frame3_filename)
        if self.frame3_save_state.get() == 1 and not self.frame3_filename:
            messagebox.showerror("Error", "Please enter a valid file name!")
            return
        #print(f"Saving file with name: {self.frame3_filename}_agg.png")
        # Simulate treeplot processing here
        savepath = f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\GUI\\sim\\2D\\multisource\\{self.frame3_filename}"
        self.frame3_particle_num = self.frame3_E1.get() if self.frame3_E1 else None
        if not self.frame3_particle_num:
            messagebox.showerror("Error", "Please enter a valid number of particles")
            return
        self.frame3_particle_num = int(self.frame3_E1.get())
        self.frame3_level = self.frame3_E2.get() if self.frame3_E2 else None
        if not self.frame3_level:
            messagebox.showerror("Error", "Please enter a valid level")
            return
        self.frame3_level = int(self.frame3_E1.get())
        self.frame3_savepath = savepath
        #print(f"Number of particles: {self.frame3_particle_num}")
        #print(f"Level : {self.frame3_level}")
        #print(f"Save path: {self.frame3_savepath}")
        multisource2d(self.frame3_particle_num, self.frame3_level, self.frame3_savepath)
        agg_img = Image.open(f'{self.frame3_savepath}_agg.png')
        agg_img.show()
        if self.frame3_save_state.get() == 0:
            os.remove(f'{self.frame3_savepath}_agg.png')
####################################################################################################################
    def frame4_savefig(self):
        """Called when the save_state changes (YES or NO is selected)."""
        choice = self.frame4_save_state.get()  # 1 for YES, 0 for NO
        #print(f"Selected option: {'YES' if choice == 1 else 'NO'}")
        # If "YES" is selected, show the filename entry widget
        if choice == 1:
            if not self.frame4_entry_label:  # Create only once if it doesn't exist
                self.frame4_entry_label = tk.Label(self.frame4_filename_frame, text="Enter a file name: ")
                self.frame4_entry_label.pack(pady=10, padx=20, expand=False)

                self.frame4_filename_entry = tk.Entry(self.frame4_filename_frame, bd=5)
                self.frame4_filename_entry.pack(pady=10, padx=20, expand=False)
        else:
            # If "NO" is selected, hide the filename entry widget
            if self.frame4_entry_label:
                self.frame4_entry_label.pack_forget()
                self.frame4_filename_entry.pack_forget()
                self.frame4_entry_label = None
                self.frame4_filename_entry = None

    def frame4_submit(self):
        self.frame4_filename = self.frame4_filename_entry.get() if self.frame4_filename_entry else None
        #print(self.frame4_filename)
        if self.frame4_save_state.get() == 1 and not self.frame4_filename:
            messagebox.showerror("Error", "Please enter a valid file name!")
            return
        #print(f"Saving file with name: {self.frame4_filename}_agg.png")
        # Simulate treeplot processing here
        savepath = f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\GUI\\sim\\2D\\multisource\\{self.frame4_filename}"
        self.frame4_particle_num = self.frame4_E1.get() if self.frame4_E1 else None
        if not self.frame4_particle_num:
            messagebox.showerror("Error", "Please enter a valid number of particles")
            return
        self.frame4_particle_num = int(self.frame4_E1.get())
        self.frame4_level = self.frame4_E2.get() if self.frame4_E2 else None
        if not self.frame4_level:
            messagebox.showerror("Error", "Please enter a valid level")
            return
        self.frame4_level = int(self.frame4_E1.get())
        self.frame4_savepath = savepath
        #print(f"Number of particles: {self.frame4_particle_num}")
        #print(f"Level : {self.frame4_level}")
        #print(f"Save path: {self.frame4_savepath}")
        multisource3d(self.frame4_particle_num, self.frame4_level, self.frame4_savepath)
        agg_img = Image.open(f'{self.frame4_savepath}_agg.png')
        agg_img.show()
        if self.frame4_save_state.get() == 0:
            os.remove(f'{self.frame4_savepath}_agg.png')
####################################################################################################################