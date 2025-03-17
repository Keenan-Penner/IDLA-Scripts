import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ctypes import windll
from PIL import Image 
from gui_functions import branch, idla, idla3, A2, A3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

windll.shcore.SetProcessDpiAwareness(1)


class MyGUI:
    def __init__(self, root):
        self.root = root
        self.stop_event = threading.Event()
        self.root.geometry("1200x750")
        self.root.title("IDLA simulations")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.task_running = False

        # Notebook setup
        self.label = tk.Label(self.root, text="IDLA simulations", font=("Arial", 20))
        self.label.pack(pady=20, padx=20, expand=False, fill=tk.BOTH, side=tk.TOP)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)

        # Create two frames to hold the plots
        self.canvas_frame_1 = tk.Frame(root)
        self.canvas_frame_1.pack(side=tk.LEFT, padx=10)

        self.canvas_frame_2 = tk.Frame(root)
        self.canvas_frame_2.pack(side=tk.LEFT, padx=10)

        self.popup1 = None #tracks whether the popup window is open
        self.popup2 = None
        self.fullscreen = False # Fullscreen mode flag
        
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
        self.frame2_info = tk.Label(self.frame2, text="Note: If YES is selected, the figures will be saved inside a folder named 'sim//3D//classical' in the current directory")
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
        self.frame4_info = tk.Label(self.frame4, text="Note: If YES is selected, the figure will be saved inside a folder named 'sim//3D//multisource' in the current directory")
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

    def on_close(self):
        """This method is called when the window close button is clicked."""
        print("Closing the application...")
        self.root.quit()  # Ends the mainloop and closes the application
        self.root.destroy()  # Destroys the Tkinter root window

    def update_label(self, message):
        """Update the Tkinter label."""
        self.label.config(text=message)
        self.root.update_idletasks()  # Force the GUI to update

    def run(self):
        self.root.mainloop()
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

    def task1(self):
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
            self.frame1_submit_btn.config(state=tk.NORMAL)  # Disable all submit buttons while task is running
            self.frame2_submit_btn.config(state=tk.NORMAL) 
            self.frame3_submit_btn.config(state=tk.NORMAL)
            self.frame4_submit_btn.config(state=tk.NORMAL)
            self.update_label("IDLA Simulations")  # Update status label
            return
        else:
            try:
                self.frame1_particle_num = int(self.frame1_particle_num)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of particles")
                self.frame1_submit_btn.config(state=tk.NORMAL)  # Disable all submit buttons while task is running
                self.frame2_submit_btn.config(state=tk.NORMAL) 
                self.frame3_submit_btn.config(state=tk.NORMAL)
                self.frame4_submit_btn.config(state=tk.NORMAL)
                self.update_label("IDLA Simulations")  # Update status label
                return
        self.frame1_particle_num = int(self.frame1_E1.get())
        self.frame1_branch_active = branch_active
        self.frame1_savepath = savepath
        if self.stop_event.is_set():
                print("Task was stopped.")
                return
        #print(f"Number of particles: {self.frame1_particle_num}")
        #print(f"Show highlighted branch: {self.frame1_branch_active}")
        #print(f"Save path: {self.frame1_savepath}")
        agg = idla(self.frame1_particle_num)
        self.root.after(0, self.update_label, 'Your simulation is ready!')
        self.root.after(0, self.frame1_submit_btn.config, {'state': tk.NORMAL}) #re-enable submit buttons
        self.root.after(0, self.frame2_submit_btn.config, {'state': tk.NORMAL})
        self.root.after(0, self.frame3_submit_btn.config, {'state': tk.NORMAL})
        self.root.after(0, self.frame4_submit_btn.config, {'state': tk.NORMAL})
        #self.frame1_submit_btn.config(state=tk.NORMAL)  # Re-enable the button
        self.root.after(0, self.plot_classical_2d, agg, self.frame1_particle_num, self.frame1_branch_active, self.frame1_savepath)

    def plot_classical_2d(self, A, n, branch_arg, save_path):
        """Plot the data in the main thread."""
        #clears previously existing widgets
        for widget in self.canvas_frame_1.winfo_children():
            widget.destroy()
        for widget in self.canvas_frame_2.winfo_children():
            widget.destroy()
        # Create a figure and plot the data
        fig1, ax1 = plt.subplots()
        fig2, ax2 = plt.subplots()
        points = A[0]
        edges=A[1]

        ##AGGREGATE
        xpoints=[points[i][0] for i in range(len(points))]
        ypoints=[points[i][1] for i in range(len(points))]
        ax1.axis('square')
        max_x = max(abs(min(xpoints)), max(xpoints))
        max_y = max(abs(min(ypoints)), max(ypoints))
        extremum = max(max_x, max_y)
        ax1.set_xlim([-extremum - 1, extremum + 1])
        ax1.set_ylim([-extremum - 1, extremum + 1])
        ax1.set_title(f"2D IDLA with {n} particles")
        ax1.scatter(xpoints, ypoints, s=10, color = 'C0')

        ##TREE
        point=A[0][-1]
        Branch=branch(edges,point)
        ax2.axis('square')
        ax2.set_xlim([-extremum - 1, extremum + 1])
        ax2.set_ylim([-extremum - 1, extremum + 1])
        ax2.set_title(f"2D IDLA tree with {n} particles")
        for i in range(len(edges)):
            ax2.plot([edges[i][0][0],edges[i][1][0]],[edges[i][0][1],edges[i][1][1]],linewidth=0.5,color='blue')
        if branch_arg:
            for i in range(len(Branch)):
                ax2.plot([Branch[i][0][0],Branch[i][1][0]],[Branch[i][0][1],Branch[i][1][1]],linewidth=0.5,color='red')

        if save_path != None:
            fig1.savefig(f'{save_path}_agg.png', dpi=500)
            fig2.savefig(f'{save_path}_tree.png', dpi=500)

        #close any existing widgets
        if self.popup1:
            self.popup1.destroy()
        if self.popup2:
            self.popup2.destroy()


        # Embed the plot into the Tkinter window using FigureCanvasTkAgg
        self.popup1 = tk.Toplevel(self.root)
        self.popup1.title("Aggregate")

        self.popup2 = tk.Toplevel(self.root)
        self.popup2.title("Tree")

        # Add a label to the pop-up window
        canvas1 = FigureCanvasTkAgg(fig1, master=self.popup1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas2 = FigureCanvasTkAgg(fig2, master=self.popup2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def frame1_submit(self):
        if self.task_running:
            return  # Don't start a new task if one is already running
        self.stop_event.clear()
        self.frame1_submit_btn.config(state=tk.DISABLED)  # Disable all submit buttons while task is running
        self.frame2_submit_btn.config(state=tk.DISABLED) 
        self.frame3_submit_btn.config(state=tk.DISABLED)
        self.frame4_submit_btn.config(state=tk.DISABLED)
        self.update_label("Your simulation is running...")  # Update status label
        thread = threading.Thread(target=self.task1)
        thread.start()  # Start the background thread

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

    def task2(self):
        self.frame2_filename = self.frame2_filename_entry.get() if self.frame2_filename_entry else None
        #print(self.frame2_filename)
        if self.frame2_save_state.get() == 1 and not self.frame2_filename:
            messagebox.showerror("Error", "Please enter a valid file name!")
            return
        #print(f"Saving file with name: {self.frame2_filename}")
        # Simulate treeplot processing here
        branch_active = self.frame2_check_state.get()
        savepath = f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\GUI\\sim\\3D\\classical\\{self.frame2_filename}"
        self.frame2_particle_num = self.frame2_E1.get() if self.frame2_E1 else None
        if not self.frame2_particle_num:
            messagebox.showerror("Error", "Please enter a valid number of particles")
            self.frame1_submit_btn.config(state=tk.NORMAL)  # Disable all submit buttons while task is running
            self.frame2_submit_btn.config(state=tk.NORMAL) 
            self.frame3_submit_btn.config(state=tk.NORMAL)
            self.frame4_submit_btn.config(state=tk.NORMAL)
            self.update_label("IDLA Simulations")  # Update status label
            return
        else:
            try:
                self.frame2_particle_num = int(self.frame2_particle_num)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of particles")
                self.frame1_submit_btn.config(state=tk.NORMAL)  # Disable all submit buttons while task is running
                self.frame2_submit_btn.config(state=tk.NORMAL) 
                self.frame3_submit_btn.config(state=tk.NORMAL)
                self.frame4_submit_btn.config(state=tk.NORMAL)
                self.update_label("IDLA Simulations")  # Update status label
                return
        self.frame2_particle_num = int(self.frame2_E1.get())
        self.frame2_branch_active = branch_active
        self.frame2_savepath = savepath
        if self.stop_event.is_set():
                print("Task was stopped.")
                return
        #print(f"Number of particles: {self.frame2_particle_num}")
        #print(f"Show highlighted branch: {self.frame2_branch_active}")
        #print(f"Save path: {self.frame2_savepath}")
        agg = idla3(self.frame2_particle_num)
        self.root.after(0, self.update_label, 'Your simulation is ready!')
        self.root.after(0, self.frame1_submit_btn.config, {'state': tk.NORMAL}) #re-enable submit buttons
        self.root.after(0, self.frame2_submit_btn.config, {'state': tk.NORMAL})
        self.root.after(0, self.frame3_submit_btn.config, {'state': tk.NORMAL})
        self.root.after(0, self.frame4_submit_btn.config, {'state': tk.NORMAL})
        #self.frame2_submit_btn.config(state=tk.NORMAL)  # Re-enable the button
        self.root.after(0, self.plot_classical_3d, agg, self.frame2_particle_num, self.frame2_branch_active, self.frame2_savepath)

    def plot_classical_3d(self, A, n, branch_arg, save_path):
        """Plot the data in the main thread."""
        #clears previously existing widgets
        for widget in self.canvas_frame_1.winfo_children():
            widget.destroy()
        for widget in self.canvas_frame_2.winfo_children():
            widget.destroy()
        # Create a figure and plot the data
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111, projection='3d')
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111, projection='3d')

        ##AGGREGATE
        points = A[0]
        xpoints = [points[i][0] for i in range(len(points))]
        ypoints = [points[i][1] for i in range(len(points))]
        zpoints = [points[i][2] for i in range(len(points))]
        ax1.axis('square')
        max_x = max(abs(min(xpoints)), max(xpoints))
        max_y = max(abs(min(ypoints)), max(ypoints))
        max_z = max(abs(min(zpoints)), max(zpoints))
        extremum = max(max_x, max_y, max_z)
        ax1.set_xlim([-extremum - 1, extremum + 1])
        ax1.set_ylim([-extremum - 1, extremum + 1])
        ax1.set_zlim([-extremum - 1, extremum + 1])
        ax1.set_title(f"3D IDLA with {n} particles")
        
        ax1.scatter(xpoints, ypoints, zpoints, s=2, color = 'C0')

        ##TREE
        edges=A[1]
        point=A[0][-1]
        Branch=branch(edges,point)
        ax2.axis('square')
        ax2.set_xlim([-extremum - 1, extremum + 1])
        ax2.set_ylim([-extremum - 1, extremum + 1])
        ax2.set_zlim([-extremum - 1, extremum + 1])
        ax2.set_title(f"3D IDLA tree with {n} particles")
        for i in range(len(edges)):
            xline=[edges[i][0][0], edges[i][1][0]]
            yline=[edges[i][0][1], edges[i][1][1]]
            zline=[edges[i][0][2], edges[i][1][2]]
            ax2.plot(xline,yline,zline,linewidth=0.5, color = 'C0')
        if branch_arg:
            for i in range(len(Branch)):
                xline=[Branch[i][0][0],Branch[i][1][0]]
                yline=[Branch[i][0][1],Branch[i][1][1]]
                zline=[Branch[i][0][2],Branch[i][1][2]]
                ax2.plot(xline,yline,zline,linewidth=2, color = 'red')

        if save_path != None:
            fig1.savefig(f'{save_path}_agg.png', dpi=500)
            fig2.savefig(f'{save_path}_tree.png', dpi=500)

        #close any existing widgets
        if self.popup1:
            self.popup1.destroy()
        if self.popup2:
            self.popup2.destroy()


        # Embed the plot into the Tkinter window using FigureCanvasTkAgg
        self.popup1 = tk.Toplevel(self.root)
        self.popup1.title("Aggregate")

        self.popup2 = tk.Toplevel(self.root)
        self.popup2.title("Tree")

        # Add a label to the pop-up window
        canvas1 = FigureCanvasTkAgg(fig1, master=self.popup1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas2 = FigureCanvasTkAgg(fig2, master=self.popup2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def frame2_submit(self):
        if self.task_running:
            return  # Don't start a new task if one is already running
        self.stop_event.clear()
        self.frame1_submit_btn.config(state=tk.DISABLED)  # Disable all submit buttons while task is running
        self.frame2_submit_btn.config(state=tk.DISABLED) 
        self.frame3_submit_btn.config(state=tk.DISABLED)
        self.frame4_submit_btn.config(state=tk.DISABLED)
        self.update_label("Your simulation is running...")  # Update status label
        thread = threading.Thread(target=self.task2)
        thread.start()  # Start the background thread

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
        
    def task3(self):
        self.frame3_filename = self.frame3_filename_entry.get() if self.frame3_filename_entry else None
        #print(self.frame3_filename)
        if self.frame3_save_state.get() == 1 and not self.frame3_filename:
            messagebox.showerror("Error", "Please enter a valid file name!")
            return
        #print(f"Saving file with name: {self.frame3_filename}")
        # Simulate treeplot processing here
        savepath = f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\GUI\\sim\\2D\\multisource\\{self.frame3_filename}"
        self.frame3_particle_num = self.frame3_E1.get() if self.frame3_E1 else None
        if not self.frame3_particle_num:
            messagebox.showerror("Error", "Please enter a valid number of particles")
            self.frame1_submit_btn.config(state=tk.NORMAL)  # reenable all submit buttons while task is running
            self.frame2_submit_btn.config(state=tk.NORMAL)
            self.frame3_submit_btn.config(state=tk.NORMAL)
            self.frame4_submit_btn.config(state=tk.NORMAL)
            self.update_label("IDLA Simulations")
            return
        else:
            try:
                self.frame3_particle_num = int(self.frame3_particle_num)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of particles")
                self.frame1_submit_btn.config(state=tk.NORMAL)  # Disable all submit buttons while task is running
                self.frame2_submit_btn.config(state=tk.NORMAL) 
                self.frame3_submit_btn.config(state=tk.NORMAL)
                self.frame4_submit_btn.config(state=tk.NORMAL)
                self.update_label("IDLA Simulations")  # Update status label
                return
        self.frame3_particle_num = int(self.frame3_E1.get())
        self.frame3_level = self.frame3_E2.get() if self.frame3_E2 else None
        # Check if the level is valid and not empty
        if not self.frame3_level:
            messagebox.showerror("Error", "Please enter a valid level")
            self.frame1_submit_btn.config(state=tk.NORMAL)
            self.frame2_submit_btn.config(state=tk.NORMAL)
            self.frame3_submit_btn.config(state=tk.NORMAL)
            self.frame4_submit_btn.config(state=tk.NORMAL)
            return
        else:
            try:
                self.frame3_level = int(self.frame3_level)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of particles")
                self.frame1_submit_btn.config(state=tk.NORMAL)  # Reenable all submit buttons if an error occurs
                self.frame2_submit_btn.config(state=tk.NORMAL) 
                self.frame3_submit_btn.config(state=tk.NORMAL)
                self.frame4_submit_btn.config(state=tk.NORMAL)
                self.update_label("IDLA Simulations")  # Update status label
                return
        self.frame3_level = int(self.frame3_E2.get())
        self.frame3_savepath = savepath
        if self.stop_event.is_set():
                print("Task was stopped.")
                return
        #print(f"Number of particles: {self.frame3_particle_num}")
        #print(f"Show highlighted branch: {self.frame3_branch_active}")
        #print(f"Save path: {self.frame3_savepath}")
        agg = A2(self.frame3_particle_num, self.frame3_level)
        self.root.after(0, self.update_label, 'Your simulation is ready!')
        self.root.after(0, self.frame1_submit_btn.config, {'state': tk.NORMAL}) #re-enable submit buttons
        self.root.after(0, self.frame2_submit_btn.config, {'state': tk.NORMAL})
        self.root.after(0, self.frame3_submit_btn.config, {'state': tk.NORMAL})
        self.root.after(0, self.frame4_submit_btn.config, {'state': tk.NORMAL})
        #self.frame3_submit_btn.config(state=tk.NORMAL)  # Re-enable the button
        self.root.after(0, self.plot_multi_2d, agg, self.frame3_particle_num, self.frame3_level, self.frame3_savepath)
    
    def plot_multi_2d(self, A, n, M, save_path):
        """Plot the data in the main thread."""
        #clears previously existing widgets
        for widget in self.canvas_frame_1.winfo_children():
            widget.destroy()
        for widget in self.canvas_frame_2.winfo_children():
            widget.destroy()
        # Create a figure and plot the data
        fig1, ax1 = plt.subplots()
        
        xpoints = [A[i][0] for i in range(len(A))]
        ypoints = [A[i][1] for i in range(len(A))]
        
        max_x = max(abs(min(xpoints)), max(xpoints))
        max_y = max(abs(min(ypoints)), max(ypoints))
        extremum = max(max_x, max_y)
        
        ax1.scatter(xpoints, ypoints, s=2, color = 'C0')
        ax1.axis('square')
        ax1.set_title(f"2D Multi-source IDLA : A_{n}[{M}]")
        
        ax1.set_xlim([-extremum - 1, extremum + 1])
        ax1.set_ylim([-extremum - 1, extremum + 1])
        ax1.set_xlabel('X axis')
        ax1.set_ylabel('Y axis')

        if save_path != None:
            fig1.savefig(f'{save_path}_agg.png', dpi=500)

        #close any existing widgets
        if self.popup1:
            self.popup1.destroy()
        if self.popup2:
            self.popup2.destroy()

        # Embed the plot into the Tkinter window using FigureCanvasTkAgg
        self.popup1 = tk.Toplevel(self.root)
        self.popup1.title("Aggregate")

        # Add a label to the pop-up window
        canvas1 = FigureCanvasTkAgg(fig1, master=self.popup1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def frame3_submit(self):
        if self.task_running:
            return  # Don't start a new task if one is already running
        self.stop_event.clear()
        self.frame1_submit_btn.config(state=tk.DISABLED)  # Disable all submit buttons while task is running
        self.frame2_submit_btn.config(state=tk.DISABLED) 
        self.frame3_submit_btn.config(state=tk.DISABLED)
        self.frame4_submit_btn.config(state=tk.DISABLED)
        self.update_label("Your simulation is running...")  # Update status label
        thread = threading.Thread(target=self.task3)
        thread.start()  # Start the background thread

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

    def task4(self):
        self.frame4_filename = self.frame4_filename_entry.get() if self.frame4_filename_entry else None
        #print(self.frame4_filename)
        if self.frame4_save_state.get() == 1 and not self.frame4_filename:
            messagebox.showerror("Error", "Please enter a valid file name!")
            return
        #print(f"Saving file with name: {self.frame4_filename}")
        # Simulate treeplot processing here
        savepath = f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\GUI\\sim\\2D\\multisource\\{self.frame4_filename}"
        self.frame4_particle_num = self.frame4_E1.get() if self.frame4_E1 else None
        #Ensure that the entry is not empty, and is an integer
        if not self.frame4_particle_num or not isinstance(self.frame4_particle_num, int):
            messagebox.showerror("Error", "Please enter a valid number of particles")
            self.frame1_submit_btn.config(state=tk.NORMAL)
            self.frame2_submit_btn.config(state=tk.NORMAL)
            self.frame3_submit_btn.config(state=tk.NORMAL)
            self.frame4_submit_btn.config(state=tk.NORMAL)
            self.update_label("IDLA Simulations")
            return
        else:
            try:
                self.frame4_particle_num = int(self.frame4_particle_num)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of particles")
                self.frame1_submit_btn.config(state=tk.NORMAL)  # Reenable all submit buttons if an error occurs
                self.frame2_submit_btn.config(state=tk.NORMAL) 
                self.frame3_submit_btn.config(state=tk.NORMAL)
                self.frame4_submit_btn.config(state=tk.NORMAL)
                self.update_label("IDLA Simulations")  # Update status label
                return
        self.frame4_particle_num = int(self.frame4_E1.get())
        self.frame4_level = self.frame4_E2.get() if self.frame4_E2 else None
        if not self.frame4_level:
            messagebox.showerror("Error", "Please enter a valid level")
            self.frame1_submit_btn.config(state=tk.NORMAL)
            self.frame2_submit_btn.config(state=tk.NORMAL)
            self.frame3_submit_btn.config(state=tk.NORMAL)
            self.frame4_submit_btn.config(state=tk.NORMAL)
            self.update_label("IDLA Simulations")
            return
        else:
            try:
                self.frame4_level = int(self.frame4_level)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of particles")
                self.frame1_submit_btn.config(state=tk.NORMAL)  # Disable all submit buttons while task is running
                self.frame2_submit_btn.config(state=tk.NORMAL) 
                self.frame3_submit_btn.config(state=tk.NORMAL)
                self.frame4_submit_btn.config(state=tk.NORMAL)
                self.update_label("IDLA Simulations")  # Update status label
                return
        self.frame4_level = int(self.frame4_E2.get())
        self.frame4_savepath = savepath
        if self.stop_event.is_set():
                print("Task was stopped.")
                return
        #print(f"Number of particles: {self.frame4_particle_num}")
        #print(f"Show highlighted branch: {self.frame4_branch_active}")
        #print(f"Save path: {self.frame4_savepath}")
        agg = A3(self.frame4_particle_num, self.frame4_level)
        self.root.after(0, self.update_label, 'Your simulation is ready!')
        self.root.after(0, self.frame1_submit_btn.config, {'state': tk.NORMAL}) #re-enable submit buttons
        self.root.after(0, self.frame2_submit_btn.config, {'state': tk.NORMAL})
        self.root.after(0, self.frame3_submit_btn.config, {'state': tk.NORMAL})
        self.root.after(0, self.frame4_submit_btn.config, {'state': tk.NORMAL})
        #self.frame4_submit_btn.config(state=tk.NORMAL)  # Re-enable the button
        self.root.after(0, self.plot_multi_3d, agg, self.frame4_particle_num, self.frame4_level, self.frame4_savepath)

    def plot_multi_3d(self, A, n, M, save_path):
        """Plot the data in the main thread."""
        #clears previously existing widgets
        for widget in self.canvas_frame_1.winfo_children():
            widget.destroy()
        for widget in self.canvas_frame_2.winfo_children():
            widget.destroy()
        
        A = np.array(A)
        #get maximum and minimum x value
        global_maxi_x = np.max(A[:, 0])
        global_mini_x = np.min(A[:, 0])

        #get maximum and minimum y value
        global_maxi_y = np.max(A[:, 1])
        global_mini_y = np.min(A[:, 1])

        #get maximum and minimum z value
        global_maxi_z = np.max(A[:, 2])
        global_mini_z = np.min(A[:, 2])

        #create a voxel grid containing the aggregate
        voxel_grid = np.zeros((global_maxi_x - global_mini_x +1, 
                                global_maxi_y - global_mini_y +1, 
                                global_maxi_z - global_mini_z +1))
        
        #loop over points in the array
        print('Preparing voxels...')
        for point in tqdm(A):
            point_x = point[0]
            point_y = point[1]
            point_z = point[2]
        #translation of all the coordinates by value of their global minimum
            voxel_x = point_x + abs(global_mini_x)
            voxel_y = point_y + abs(global_mini_y)
            voxel_z = point_z + abs(global_mini_z)

            voxel_grid[voxel_x, voxel_y, voxel_z] = 1
        
        #plot 
        
        # Create a figure and plot the data
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        x, y, z = np.indices((voxel_grid.shape[0] + 1, voxel_grid.shape[1] + 1, voxel_grid.shape[2] + 1))

        x+= global_mini_x
        y+= global_mini_y
        z+= global_mini_z 

        ax.voxels(x, y, z, voxel_grid, edgecolor='k', shade = False)

        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        ax.set_box_aspect([1, 1, 1])
        ax.set_aspect('equal')
        ax.set_title(f"3D Multi-source IDLA : A_{n}[{M}]")

        if save_path != None:
            fig.savefig(f'{save_path}_agg.png', dpi=500)

        #close any existing widgets
        if self.popup1:
            self.popup1.destroy()
        if self.popup2:
            self.popup2.destroy() 

        # Embed the plot into the Tkinter window using FigureCanvasTkAgg
        self.popup1 = tk.Toplevel(self.root)
        self.popup1.title("Aggregate")
        

        # Add a label to the pop-up window
        canvas1 = FigureCanvasTkAgg(fig, master=self.popup1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def frame4_submit(self):
        if self.task_running:
            return  # Don't start a new task if one is already running
        self.stop_event.clear()
        self.frame1_submit_btn.config(state=tk.DISABLED)  # Disable all submit buttons while task is running
        self.frame2_submit_btn.config(state=tk.DISABLED) 
        self.frame3_submit_btn.config(state=tk.DISABLED)
        self.frame4_submit_btn.config(state=tk.DISABLED)
        self.update_label("Your simulation is running...")  # Update status label
        thread = threading.Thread(target=self.task4)
        thread.start()  # Start the background thread
####################################################################################################################