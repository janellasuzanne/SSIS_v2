import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import askyesno, askquestion
from tkinter.messagebox import showerror, showwarning, showinfo

import mysql.connector
from mysql.connector import Error

from init_queries_version2 import *

class SSIS_ver2(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Simple Student Information System v2')
        self.geometry('720x480')
        self.bind('<Control-KeyPress-w>', lambda event: self.quit())

        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='version2'
        )
        self.cursor = self.db.cursor()

        # create database
        self.execute_query(self.db, create_database_query)

        # create tables
        self.execute_query(self.db, create_course_ver2_table_query)
        self.execute_query(self.db, create_student_ver2_table_query)

        # populate tables
        self.execute_query(self.db, populate_coursesv2)
        self.execute_query(self.db, populate_studentsv2)

        self.db.commit()

        # entities
        self.student = 'STUDENT'
        self.course = 'COURSE'

        self.code_var = tk.StringVar(value='Enter Course Code')
        self.desc_var = tk.StringVar(value='Enter Course Description')
        self.id_var = tk.StringVar(value='Enter ID Number')
        self.first_var = tk.StringVar(value='Enter First Name')
        self.last_var = tk.StringVar(value='Enter Last Name')
        self.year_var = tk.StringVar(value='Select Year Level')
        self.gender_var = tk.StringVar(value='Select Gender')
        self.search_var = tk.StringVar(value='Search by')
        self.search_entry_var = tk.StringVar(value='Search here...')

    # WIDGETS
        # frames
        self.entities_frame = tk.LabelFrame(self, relief='sunken')
        self.search_frame = tk.Frame(self, relief='sunken')

        self.entity = ''

        # entities elements
        self.student_button = tk.Button(self.entities_frame, text=self.student, width=25, command=lambda: self.refresh_list(self.student)
        )
        self.course_button = tk.Button(self.entities_frame, text=self.course, width=25, command=lambda: self.refresh_list(self.course)
        )

        # search elements
        self.search_combobox = ttk.Combobox(
            self.search_frame,
            textvariable=self.search_var,
            width=20,
            state='readonly')
        self.search_entry = tk.Entry(
            self.search_frame,
            textvariable=self.search_entry_var,
            width=80)

        # show_list button
        self.show_list = tk.Button(self, text='Show List', command=lambda: self.refresh_list(self.entity)
        )

        self.treeview = ttk.Treeview(self, show='headings')
        self.treeview.bind('<Double-Button-1>', self.get_info)

        # add button
        self.add = tk.Button(self, text='Add', relief='raised', command=lambda: self.create(self.entity)
        )

    # LAYOUT
        # frames
        self.entities_frame.pack(fill='x', padx=5, pady=10)
        self.search_frame.pack(fill='x', padx=5, pady=5)

        # entities elements
        self.student_button.pack(side='left', expand=True, pady=5)
        self.course_button.pack(side='left', expand=True, pady=5)

        # search elements
        self.search_combobox.pack(side='left', expand=True)
        self.search_entry.pack(side='left', expand=True)

        # show_list button
        self.show_list.pack(fill='x')

        # treeview
        self.treeview.pack(fill='x', expand=True, padx=30, pady=10)

        # add button
        self.add.pack(fill='x', padx=10, pady=10)

        self.mainloop()
    
    def execute_query(self, connection, query):
        self.cursor = connection.cursor()
        try:
            self.cursor.execute(query)
            connection.commit()
            print('Query Successful')
        except Error as err:
            return

# L - LIST
    def refresh_list(self, entity):
        self.entity = entity
        # Removes the previous data in the treeview
        if len(self.treeview.get_children()) > 0:
            self.treeview.delete(*self.treeview.get_children())

        if self.entity == self.student:
            self.treeview['columns'] = ('ID', 'Name', 'Course', 'Year Level')
            self.treeview.column("ID", width=5)
            self.treeview.column("Name", width=30)
            self.treeview.column("Course", width=10)
            self.treeview.column("Year Level", width=10)

            self.treeview.heading("ID", text="Student ID")
            self.treeview.heading("Name", text="Student Name")
            self.treeview.heading("Course", text="Course")
            self.treeview.heading("Year Level", text="Year Level")

            if self.search_var.get() == 'All':
                self.cursor.execute('SELECT * FROM student_ver2 ORDER BY year_level, course_key')
            elif self.search_var.get() == 'ID':
                self.cursor.execute('SELECT * FROM student_ver2 WHERE id = %s', (self.search_entry_var.get(),))
            elif self.search_var.get() == 'Last Name':
                self.cursor.execute('SELECT * FROM student_ver2 WHERE  last_name= %s', (self.search_entry_var.get(),))
            elif self.search_var.get() == 'Course':
                self.cursor.execute('SELECT * FROM student_ver2 WHERE  course_key= %s ORDER BY year_level, course_key', (self.search_entry_var.get(),))
            else:
                self.cursor.execute('SELECT * FROM student_ver2 ORDER BY year_level, course_key')
            
            students = self.cursor.fetchall()
            for student in students:
                self.treeview.insert('', tk.END, values=(student[0], f'{student[1]} {student[2]}', student[5], student[3]))
        else:
            self.treeview['columns'] = ('Code', 'Desc')
            self.treeview.column("Code", width=5)
            self.treeview.column("Desc", width=30)

            self.treeview.heading("Code", text="Course Code")
            self.treeview.heading("Desc", text="Course Description")

            if self.search_var.get() == 'All':
                self.cursor.execute('SELECT * FROM course_ver2 ORDER BY code')
            elif self.search_var.get() == 'Course Code':
                self.cursor.execute('SELECT * FROM course_ver2 WHERE  code= %s', (self.search_entry_var.get(),))
            else:
                self.cursor.execute('SELECT * FROM course_ver2 ORDER BY code')

            courses = self.cursor.fetchall()
            for course in courses:
                self.treeview.insert('', tk.END, values=(course[0], course[1]))
        # Updates the available search filters
        self.search_combo_update()

    # Function to update the search filters
    def search_combo_update(self):
        if self.entity == self.student:
            self.search_combobox['values'] = ('All', 'ID', 'Last Name', 'Course')
        elif self.entity == self.course:
            self.search_combobox['values'] = ('All', 'Course Code')

# C - CREATE
    def create(self, entity):
         # toplevel
        self.create_toplevel = tk.Toplevel(self)
        self.create_toplevel.title('Information')
        self.create_toplevel.geometry('500x350')
        self.create_toplevel.resizable(False, False)
        self.create_toplevel.bind('<Control-KeyPress-w>', lambda event: self.create_toplevel.destroy())
        
    # WIDGETS
        # frames 
        self.info_field = tk.LabelFrame(self.create_toplevel, relief='sunken')
        self.labels_frame = tk.Frame(self.info_field)
        self.entries_frame = tk.Frame(self.info_field)
        self.actions_frame = tk.Frame(self.create_toplevel)

        # actions elements
        self.submit = tk.Button(self.actions_frame, text='Submit', command=self.submit_item)
        self.cancel = tk.Button(self.actions_frame, text='Cancel', command=lambda: self.create_toplevel.destroy())

        # LAYOUT
        # frames
        self.info_field.pack(fill='x', pady=20)
        self.actions_frame.pack(fill='x', side='bottom', pady=10)
        
        # info frame sub-frames
        self.labels_frame.pack(side='left', expand=True, pady=10)
        self.entries_frame.pack(side='left', expand=True, pady=10)

        # actions element
        self.submit.pack(fill='x', padx=10, pady=5)
        self.cancel.pack(fill='x', padx=10, pady=5)

        if entity == self.course:
        # WIDGETS
            # labels
            self.code_label = tk.Label(self.labels_frame, text='COURSE CODE:')
            self.desc_label = tk.Label(self.labels_frame, text='COURSE DESCRIPTION:')

            # entries
            self.code_entry = tk.Entry(
                self.entries_frame,
                textvariable=self.code_var,
                width=45)
            self.desc_entry = tk.Entry(
                self.entries_frame,
                textvariable=self.desc_var,
                width=45)

        # LAYOUT
            # labels
            self.code_label.pack(anchor='w', pady=2)
            self.desc_label.pack(anchor='w', pady=2)
            
            # entries
            self.code_entry.pack(pady=2)
            self.desc_entry.pack(pady=2)
                
        if entity == self.student:
        # WIDGETS
            # labels
            self.student_id_label = tk.Label(self.labels_frame, text='STUDENT ID:')
            self.first_name_label = tk.Label(self.labels_frame, text='FIRST NAME:')
            self.last_name_label = tk.Label(self.labels_frame, text='LAST NAME:')
            self.course_label = tk.Label(self.labels_frame, text='COURSE:')
            self.year_level_label = tk.Label(self.labels_frame, text='YEAR LEVEL:')
            self.gender = tk.Label(self.labels_frame, text='GENDER:')

            # entries
            self.student_id_entry = tk.Entry(
                self.entries_frame, 
                textvariable=self.id_var,
                width=45)

            self.first_name_entry = tk.Entry(
                self.entries_frame, 
                textvariable=self.first_var,
                width=45)

            self.last_name_entry = tk.Entry(
                self.entries_frame, 
                textvariable=self.last_var,
                width=45)

            self.course_combobox = ttk.Combobox(
                self.entries_frame, 
                textvariable=self.code_var,
                width=45,
                state='readonly')
            self.cursor.execute('SELECT code FROM course_ver2')
            self.course_combobox['values'] = self.cursor.fetchall()

            self.year_level_combobox = ttk.Combobox(
                self.entries_frame, 
                values=('1st Year', '2nd Year', '3rd Year', '4th year'),
                textvariable=self.year_var,
                width=45,
                state='readonly')

            self.gender_combobox = ttk.Combobox(
                self.entries_frame, 
                values=('Male', 'Female'),
                textvariable=self.gender_var,
                width=45,
                state='readonly')
            
        # LAYOUT
            # labels
            self.student_id_label.pack(anchor='w', pady=2)
            self.first_name_label.pack(anchor='w', pady=2)
            self.last_name_label.pack(anchor='w', pady=2)
            self.course_label.pack(anchor='w', pady=2)
            self.year_level_label.pack(anchor='w', pady=2)
            self.gender.pack(anchor='w', pady=2)

            # entries
            self.student_id_entry.pack(pady=2)
            self.first_name_entry.pack(pady=2)
            self.last_name_entry.pack(pady=2)
            self.course_combobox.pack(pady=2)
            self.year_level_combobox.pack(pady=2)
            self.gender_combobox.pack(pady=2)

    # Function to execute the submission for the creation of item  
    def submit_item(self):
        try:
            if self.entity == self.course:
                answer = messagebox.askokcancel(
                    "Registration Information",
                    f"The following {self.entity} is going to be registered.\n\nCOURSE CODE: \t\t{self.code_var.get()}\n\nCOURSE DESCRIPTION: \t{self.desc_var.get()}"
                )
                if answer:
                    query = 'INSERT INTO course_ver2 (code, description) VALUES (%s, %s)'
                    values = (self.code_var.get(), self.desc_var.get(),)
                    self.cursor.execute(query, values)
                    self.db.commit()

            if self.entity == self.student:
                answer = messagebox.askokcancel(
                    "Registration Information",
                    f"The following {self.entity} is going to be registered.\n\nSTUDENT ID:\t{self.id_var.get()}\n\nNAME: \t\t{self.first_var.get()} {self.last_var.get()}\n\nCOURSE: \t{self.code_var.get()}\n\nYEAR LEVEL: \t{self.year_var.get()}\n\nGENDER: \t{self.gender_var.get()}"
                )
                if answer:
                    query = 'INSERT INTO student_ver2 (id, first_name, last_name, year_level, gender, course_key) VALUES (%s, %s, %s, %s, %s, %s)'
                    values = (self.id_var.get(), self.first_var.get(), self.last_var.get(), self.year_var.get(), self.gender_var.get(), self.code_var.get(),)
                    self.cursor.execute(query, values)
                    self.db.commit()

            # Updates the list in the treeview after item creation
            if answer:
                messagebox.showinfo('Registration Successful!', f'{self.entity} successfully registered!')
                self.refresh_list(self.entity)
        except:
            messagebox.showerror('Error', f'An error has occured! Cannot add {self.entity}!')

# R - READ
    def get_info(self, event):
        item = self.treeview.focus()
        info = self.treeview.item(item, 'values')
        
        # WIDGETS
            # toplevel
        self.info_toplevel = tk.Toplevel(self)
        self.info_toplevel.title('Information')
        self.info_toplevel.geometry('500x300')
        self.info_toplevel.resizable(False, False)
        self.info_toplevel.bind('<Control-KeyPress-w>', lambda event: self.info_toplevel.destroy())

            # frames
        self.info_field = tk.LabelFrame(self.info_toplevel, relief='sunken')
        self.labels_frame = tk.Frame(self.info_field)
        self.entries_frame = tk.Frame(self.info_field)

        self.actions_frame = tk.Frame(self.info_toplevel)

        if self.entity == self.course:
            self.cursor.execute('SELECT * FROM course_ver2 WHERE code = %s', (info[0],))
            info = self.cursor.fetchone()
            self.code_var.set(info[0])
            self.desc_var.set(info[1])
            # WIDGETS
                # labels
            self.code_label = tk.Label(self.labels_frame, text='COURSE CODE:')
            self.desc_label = tk.Label(self.labels_frame, text='COURSE DESCRIPTION:')

                # entries
            # self.college_combobox['values'] = self.cursor.fetchall()
            # self.college_combobox.bind('<<ComboboxSelected>>', )
            self.code_entry = tk.Entry(
                self.entries_frame,
                textvariable=self.code_var,
                width=45,
                state='disable')
            self.desc_entry = tk.Entry(
                self.entries_frame,
                textvariable=self.desc_var,
                width=45,
                state='disable')

            # LAYOUT
                # labels
            self.code_label.pack(anchor='w', pady=2)
            self.desc_label.pack(anchor='w', pady=2)
            
                # entries
            self.code_entry.pack(pady=2)
            self.desc_entry.pack(pady=2)

            self.editables = (self.code_entry, self.desc_entry)
            self.key = info[0]
                
        if self.entity == self.student:
            self.cursor.execute('SELECT * FROM student_ver2 WHERE id = %s', (info[0],))
            info = self.cursor.fetchone()

            self.id_var.set(info[0])
            self.first_var.set(info[1])
            self.last_var.set(info[2])
            self.year_var.set(info[3])
            self.gender_var.set(info[4])
            self.code_var.set(info[5])
            # WIDGETS
                # labels
            self.student_id_label = tk.Label(self.labels_frame, text='STUDENT ID:')
            self.first_name_label = tk.Label(self.labels_frame, text='FIRST NAME:')
            self.last_name_label = tk.Label(self.labels_frame, text='LAST NAME:')
            self.course_label = tk.Label(self.labels_frame, text='COURSE:')
            self.year_level_label = tk.Label(self.labels_frame, text='YEAR LEVEL:')
            self.gender = tk.Label(self.labels_frame, text='GENDER:')

                # entries
            self.student_id_entry = tk.Entry(
                self.entries_frame, 
                textvariable=self.id_var,
                width=45,
                state='disable')
            self.first_name_entry = tk.Entry(
                self.entries_frame, 
                textvariable=self.first_var,
                width=45,
                state='disable')
            self.last_name_entry = tk.Entry(
                self.entries_frame, 
                textvariable=self.last_var,
                width=45,
                state='disable')

            self.course_combobox = ttk.Combobox(
                self.entries_frame, 
                textvariable=self.code_var,
                width=45,
                state='disable')
            self.cursor.execute('SELECT code FROM course_ver2')
            self.course_combobox['values'] = self.cursor.fetchall()

            self.year_level_combobox = ttk.Combobox(
                self.entries_frame, 
                values=('1st Year', '2nd Year', '3rd Year', '4th year'),
                textvariable=self.year_var,
                width=45,
                state='disable')

            self.gender_combobox = ttk.Combobox(
                self.entries_frame, 
                values=('Male', 'Female'),
                textvariable=self.gender_var,
                width=45,
                state='disable')
            
            # LAYOUT
                # labels
            self.student_id_label.pack(anchor='w', pady=2)
            self.first_name_label.pack(anchor='w', pady=2)
            self.last_name_label.pack(anchor='w', pady=2)
            self.course_label.pack(anchor='w', pady=2)
            self.year_level_label.pack(anchor='w', pady=2)
            self.gender.pack(anchor='w', pady=2)
                # entries
            self.student_id_entry.pack(pady=2)
            self.first_name_entry.pack(pady=2)
            self.last_name_entry.pack(pady=2)
            self.course_combobox.pack(pady=2)
            self.year_level_combobox.pack(pady=2)
            self.gender_combobox.pack(pady=2)
        
            self.editables = (self.course_combobox, self.year_level_combobox, self.gender_combobox)
            self.key = info[0]
            
            # actions_frame elementS
        self.edit = tk.Button(self.actions_frame, text='Edit', width=20, command=lambda: self.edit_entries(self.editables))
        self.update = tk.Button(self.actions_frame, text='Update', width=20, command=lambda: self.update_item(self.key))
        self.delete = tk.Button(self.actions_frame, text='Delete', width=20, command=lambda: self.delete_item(self.info_toplevel))

        # LAYOUT
            # frames
        self.info_field.pack(fill='x', pady=20)
        self.labels_frame.pack(side='left', expand=True, pady=10)
        self.entries_frame.pack(side='left', expand=True, pady=10)

        # actions layout
        self.actions_frame.pack(side='bottom', fill='x', padx=20, pady=10)

            # actions elements
        self.edit.pack(side='left', expand=True)
        self.update.pack(side='left', expand=True)
        self.delete.pack(side='left', expand=True)

# U -Update
    # Makes necessary entries editable
    def edit_entries(self, editables):
        if self.entity == self.course:
            for editable in editables:
                editable['state'] = 'normal'
        if self.entity == self.student:
            for editable in editables:
                editable['state'] = 'readonly'

    # Updates the item information after editing
    def update_item(self, key):
        try:
            if self.entity == self.course:
                self.cursor.execute('UPDATE course_ver2 SET code = %s, description = %s WHERE code = %s', (self.code_var.get(), self.desc_var.get(), key,))
                self.db.commit()
                update = messagebox.showinfo('Update Successful', 'Course Information Updated!')
            if self.entity == self.student:
                self.cursor.execute('UPDATE student_ver2 SET course_key = %s, year_level = %s, gender = %s WHERE id = %s', (self.code_var.get(), self.year_var.get(), self.gender_var.get(), key,))
                self.db.commit()
                update = messagebox.showinfo('Update Successful', 'Student Information Updated!')

            if update:
                    self.refresh_list(self.entity)
        except:
            messagebox.showerror('Error', 'An error has occured.')

 # D - DELETE
    def delete_item(self, toplevel):
        confirm = False
        if self.entity == self.course:
            self.cursor.execute('SELECT * FROM student_ver2 WHERE course_key = %s', (self.code_var.get(),))
            studentsInCourse = self.cursor.fetchall()
            if len(studentsInCourse) > 0:
                answer = messagebox.askokcancel("Warning", f"Students are currently enrolled in this {self.entity}.\nDo you still want to DELETE this {self.entity}?\n\n\n(If the course is deleted, all currently enrolled students will not belong to any courses.)")
                if answer:
                    confirm = True
            else:
                answer = messagebox.askyesno(
                    'Confirm Deletion',
                    f"Are you sure you want to DELETE THIS {self.entity}?\n\nCOURSE CODE: \t\t{self.code_var.get()}\n\nCOURSE DESCRIPTION: \t{self.desc_var.get()}")
                if answer:
                    confirm = True

            if confirm:
                messagebox.showinfo('DELETION CONFIRMED', f'{self.entity} successfully deleted')
                self.cursor.execute('DELETE FROM course_ver2 WHERE code = %s', (self.code_var.get(),))
                self.db.commit()

        if self.entity == self.student:
            answer = messagebox.askyesno(
                'Confirm Deletion',
                f'Are you sure you want to DELETE THIS {self.entity}?\n\nSTUDENT ID:\t{self.id_var.get()}\n\nNAME: \t\t{self.first_var.get()} {self.last_var.get()}\n\nCOURSE: \t{self.code_var.get()}\n\nYEAR LEVEL: \t{self.year_var.get()}\n\nGENDER: \t{self.gender_var.get()}')

            if answer:
                messagebox.showinfo('DELETION CONFIRMED', f'{self.entity} successfully deleted')
                self.cursor.execute('DELETE FROM student_ver2 WHERE id = %s', (self.id_var.get(),))
                self.db.commit()

        # Updates the list in the treeview after deletion
        if confirm:
            toplevel.destroy()
            self.refresh_list(self.entity)
        else:
            toplevel.destroy()

SSIS_ver2()
