#!/usr/bin/env python3
"""
QuickMed Calc - A Clinical Calculator & Decision Aid for Medical Professionals
Created for General Physicians and Medical Practitioners

IMPORTANT MEDICAL DISCLAIMER:
This software is for educational and reference purposes only.
It is not intended to replace clinical judgment or professional medical advice.
Always verify calculations independently and consult current medical literature.
Users are responsible for ensuring accuracy before making clinical decisions.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import os
import json
from datetime import datetime
import math

class QuickMedCalc:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("QuickMed Calc - Clinical Calculator")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database
        self.init_database()
        
        # Calculator registry - must be defined before creating interface
        self.calculators = {
            'bmi': 'BMI Calculator',
            'bsa': 'Body Surface Area',
            'creatinine': 'Creatinine Clearance',
            'gcs': 'Glasgow Coma Scale',
            'wells': 'Wells Score (DVT)',
            'apgar': 'APGAR Score',
            'pediatric': 'Pediatric Dosing',
            'chads2': 'CHADS₂ Score'
        }
        
        # Create main interface
        self.create_main_interface()
        
    def init_database(self):
        """Initialize SQLite database for notes and data storage"""
        self.db_path = 'quickmed_data.db'
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create notes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                calculator_type TEXT,
                patient_info TEXT,
                calculation_result TEXT,
                notes TEXT
            )
        ''')
        
        # Create favorites table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                calculator_name TEXT UNIQUE
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def create_main_interface(self):
        """Create the main application interface"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="QuickMed Calc", 
                              font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=15)
        
        # Search frame
        search_frame = tk.Frame(self.root, bg='#f0f0f0')
        search_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_frame, text="Quick Search:", font=('Arial', 12)).pack(anchor='w')
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_calculators)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 11))
        search_entry.pack(fill='x', pady=5)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Calculator list
        left_panel = tk.Frame(main_frame, bg='white', width=250)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        tk.Label(left_panel, text="Medical Calculators", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Calculator buttons frame
        self.calc_frame = tk.Frame(left_panel, bg='white')
        self.calc_frame.pack(fill='both', expand=True, padx=10)
        
        # Right panel - Calculator interface
        self.right_panel = tk.Frame(main_frame, bg='white')
        self.right_panel.pack(side='right', fill='both', expand=True)
        
        # Load calculator buttons
        self.create_calculator_buttons()
        
        # Show welcome message initially
        self.show_welcome()
        
    def create_calculator_buttons(self):
        """Create buttons for all calculators"""
        for widget in self.calc_frame.winfo_children():
            widget.destroy()
            
        for calc_key, calc_name in self.calculators.items():
            if not self.search_var.get() or self.search_var.get().lower() in calc_name.lower():
                btn = tk.Button(self.calc_frame, text=calc_name,
                              command=lambda k=calc_key: self.load_calculator(k),
                              font=('Arial', 10), bg='#3498db', fg='white',
                              relief='flat', pady=8)
                btn.pack(fill='x', pady=2)
                
    def filter_calculators(self, *args):
        """Filter calculator list based on search"""
        self.create_calculator_buttons()
        
    def show_welcome(self):
        """Show welcome message"""
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        welcome_frame = tk.Frame(self.right_panel, bg='white')
        welcome_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(welcome_frame, text="Welcome to QuickMed Calc", 
                font=('Arial', 18, 'bold')).pack(pady=20)
        
        tk.Label(welcome_frame, text="Select a calculator from the left panel or use quick search.",
                font=('Arial', 12)).pack()
        
        # Medical disclaimer
        disclaimer = tk.Text(welcome_frame, height=8, wrap='word', bg='#fff2cc', 
                            font=('Arial', 10))
        disclaimer.pack(fill='x', pady=20)
        disclaimer.insert('1.0', 
            "MEDICAL DISCLAIMER:\n\n"
            "This software is for educational and reference purposes only. "
            "It is not intended to replace clinical judgment or professional medical advice. "
            "Always verify calculations independently and consult current medical literature. "
            "Users are responsible for ensuring accuracy before making clinical decisions.\n\n"
            "All calculations should be validated against current clinical guidelines.")
        disclaimer.config(state='disabled')
        
    def load_calculator(self, calc_type):
        """Load specific calculator interface"""
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
            
        if calc_type == 'bmi':
            self.create_bmi_calculator()
        elif calc_type == 'bsa':
            self.create_bsa_calculator()
        elif calc_type == 'creatinine':
            self.create_creatinine_calculator()
        elif calc_type == 'gcs':
            self.create_gcs_calculator()
        elif calc_type == 'wells':
            self.create_wells_calculator()
        elif calc_type == 'apgar':
            self.create_apgar_calculator()
        elif calc_type == 'pediatric':
            self.create_pediatric_calculator()
        elif calc_type == 'chads2':
            self.create_chads2_calculator()
            
    def create_calculator_frame(self, title):
        """Create common calculator frame structure"""
        main_frame = tk.Frame(self.right_panel, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(main_frame, text=title, font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # Calculator frame
        calc_frame = tk.Frame(main_frame, bg='white')
        calc_frame.pack(fill='x', pady=(0, 20))
        
        # Result frame
        result_frame = tk.Frame(main_frame, bg='#e8f5e8')
        result_frame.pack(fill='x', pady=(0, 20))
        
        # Notes frame
        notes_frame = tk.Frame(main_frame, bg='white')
        notes_frame.pack(fill='both', expand=True)
        
        return calc_frame, result_frame, notes_frame
        
    def create_bmi_calculator(self):
        """BMI Calculator"""
        calc_frame, result_frame, notes_frame = self.create_calculator_frame("BMI Calculator")
        
        # Input fields
        tk.Label(calc_frame, text="Weight (kg):").grid(row=0, column=0, sticky='w', pady=5)
        weight_entry = tk.Entry(calc_frame)
        weight_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(calc_frame, text="Height (cm):").grid(row=1, column=0, sticky='w', pady=5)
        height_entry = tk.Entry(calc_frame)
        height_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Result display
        result_label = tk.Label(result_frame, text="BMI: -- | Category: --", 
                               font=('Arial', 12, 'bold'))
        result_label.pack(pady=10)
        
        def calculate_bmi():
            try:
                weight = float(weight_entry.get())
                height = float(height_entry.get()) / 100  # Convert cm to m
                bmi = weight / (height ** 2)
                
                # Determine category
                if bmi < 18.5:
                    category = "Underweight"
                elif 18.5 <= bmi < 25:
                    category = "Normal weight"
                elif 25 <= bmi < 30:
                    category = "Overweight"
                else:
                    category = "Obese"
                    
                result_text = f"BMI: {bmi:.1f} | Category: {category}"
                result_label.config(text=result_text)
                
                # Save to database
                self.save_calculation('BMI', f"Weight: {weight}kg, Height: {height_entry.get()}cm", result_text)
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
                
        tk.Button(calc_frame, text="Calculate BMI", command=calculate_bmi,
                 bg='#2ecc71', fg='white', font=('Arial', 10)).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Notes section
        self.create_notes_section(notes_frame)
        
    def create_bsa_calculator(self):
        """Body Surface Area Calculator (Mosteller formula)"""
        calc_frame, result_frame, notes_frame = self.create_calculator_frame("Body Surface Area (BSA)")
        
        tk.Label(calc_frame, text="Weight (kg):").grid(row=0, column=0, sticky='w', pady=5)
        weight_entry = tk.Entry(calc_frame)
        weight_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(calc_frame, text="Height (cm):").grid(row=1, column=0, sticky='w', pady=5)
        height_entry = tk.Entry(calc_frame)
        height_entry.grid(row=1, column=1, padx=10, pady=5)
        
        result_label = tk.Label(result_frame, text="BSA: -- m²", font=('Arial', 12, 'bold'))
        result_label.pack(pady=10)
        
        def calculate_bsa():
            try:
                weight = float(weight_entry.get())
                height = float(height_entry.get())
                # Mosteller formula
                bsa = math.sqrt((weight * height) / 3600)
                
                result_text = f"BSA: {bsa:.2f} m² (Mosteller formula)"
                result_label.config(text=result_text)
                
                self.save_calculation('BSA', f"Weight: {weight}kg, Height: {height}cm", result_text)
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
                
        tk.Button(calc_frame, text="Calculate BSA", command=calculate_bsa,
                 bg='#2ecc71', fg='white', font=('Arial', 10)).grid(row=2, column=0, columnspan=2, pady=10)
        
        self.create_notes_section(notes_frame)
        
    def create_creatinine_calculator(self):
        """Creatinine Clearance Calculator (Cockcroft-Gault)"""
        calc_frame, result_frame, notes_frame = self.create_calculator_frame("Creatinine Clearance (Cockcroft-Gault)")
        
        tk.Label(calc_frame, text="Age (years):").grid(row=0, column=0, sticky='w', pady=5)
        age_entry = tk.Entry(calc_frame)
        age_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(calc_frame, text="Weight (kg):").grid(row=1, column=0, sticky='w', pady=5)
        weight_entry = tk.Entry(calc_frame)
        weight_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(calc_frame, text="Serum Creatinine (mg/dL):").grid(row=2, column=0, sticky='w', pady=5)
        creat_entry = tk.Entry(calc_frame)
        creat_entry.grid(row=2, column=1, padx=10, pady=5)
        
        gender_var = tk.StringVar(value="male")
        tk.Label(calc_frame, text="Gender:").grid(row=3, column=0, sticky='w', pady=5)
        gender_frame = tk.Frame(calc_frame, bg='white')
        gender_frame.grid(row=3, column=1, sticky='w', padx=10, pady=5)
        tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="male", bg='white').pack(side='left')
        tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="female", bg='white').pack(side='left')
        
        result_label = tk.Label(result_frame, text="Creatinine Clearance: -- mL/min", 
                               font=('Arial', 12, 'bold'))
        result_label.pack(pady=10)
        
        def calculate_creatinine():
            try:
                age = float(age_entry.get())
                weight = float(weight_entry.get())
                creatinine = float(creat_entry.get())
                gender = gender_var.get()
                
                # Cockcroft-Gault formula
                clcr = ((140 - age) * weight) / (72 * creatinine)
                if gender == "female":
                    clcr *= 0.85
                    
                # Interpretation
                if clcr >= 90:
                    interpretation = "Normal"
                elif clcr >= 60:
                    interpretation = "Mild decrease"
                elif clcr >= 30:
                    interpretation = "Moderate decrease"
                elif clcr >= 15:
                    interpretation = "Severe decrease"
                else:
                    interpretation = "Kidney failure"
                
                result_text = f"CrCl: {clcr:.1f} mL/min ({interpretation})"
                result_label.config(text=result_text)
                
                self.save_calculation('Creatinine Clearance', 
                                    f"Age: {age}, Weight: {weight}kg, SCr: {creatinine}mg/dL, {gender}", 
                                    result_text)
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
                
        tk.Button(calc_frame, text="Calculate CrCl", command=calculate_creatinine,
                 bg='#2ecc71', fg='white', font=('Arial', 10)).grid(row=4, column=0, columnspan=2, pady=10)
        
        self.create_notes_section(notes_frame)
        
    def create_gcs_calculator(self):
        """Glasgow Coma Scale Calculator"""
        calc_frame, result_frame, notes_frame = self.create_calculator_frame("Glasgow Coma Scale (GCS)")
        
        # Eye Opening
        tk.Label(calc_frame, text="Eye Opening:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=(10,5))
        eye_var = tk.IntVar()
        eye_options = [
            (4, "Spontaneous"),
            (3, "To voice"),
            (2, "To pain"),
            (1, "None")
        ]
        
        for i, (score, description) in enumerate(eye_options):
            tk.Radiobutton(calc_frame, text=f"{score}: {description}", 
                          variable=eye_var, value=score, bg='white').grid(row=i+1, column=0, sticky='w')
        
        # Verbal Response
        tk.Label(calc_frame, text="Verbal Response:", font=('Arial', 10, 'bold')).grid(row=0, column=1, sticky='w', pady=(10,5), padx=(20,0))
        verbal_var = tk.IntVar()
        verbal_options = [
            (5, "Oriented"),
            (4, "Confused"),
            (3, "Inappropriate words"),
            (2, "Incomprehensible"),
            (1, "None")
        ]
        
        for i, (score, description) in enumerate(verbal_options):
            tk.Radiobutton(calc_frame, text=f"{score}: {description}", 
                          variable=verbal_var, value=score, bg='white').grid(row=i+1, column=1, sticky='w', padx=(20,0))
        
        # Motor Response
        tk.Label(calc_frame, text="Motor Response:", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky='w', pady=(10,5), padx=(20,0))
        motor_var = tk.IntVar()
        motor_options = [
            (6, "Obeys commands"),
            (5, "Localizes pain"),
            (4, "Withdraws from pain"),
            (3, "Flexion to pain"),
            (2, "Extension to pain"),
            (1, "None")
        ]
        
        for i, (score, description) in enumerate(motor_options):
            tk.Radiobutton(calc_frame, text=f"{score}: {description}", 
                          variable=motor_var, value=score, bg='white').grid(row=i+1, column=2, sticky='w', padx=(20,0))
        
        result_label = tk.Label(result_frame, text="GCS: -- | Interpretation: --", 
                               font=('Arial', 12, 'bold'))
        result_label.pack(pady=10)
        
        def calculate_gcs():
            eye = eye_var.get()
            verbal = verbal_var.get()
            motor = motor_var.get()
            
            if eye == 0 or verbal == 0 or motor == 0:
                messagebox.showwarning("Warning", "Please select all GCS components")
                return
                
            total = eye + verbal + motor
            
            # Interpretation
            if total >= 13:
                interpretation = "Mild brain injury"
            elif total >= 9:
                interpretation = "Moderate brain injury"
            else:
                interpretation = "Severe brain injury"
                
            result_text = f"GCS: {total}/15 (E{eye}V{verbal}M{motor}) | {interpretation}"
            result_label.config(text=result_text)
            
            self.save_calculation('GCS', f"E{eye}V{verbal}M{motor}", result_text)
            
        tk.Button(calc_frame, text="Calculate GCS", command=calculate_gcs,
                 bg='#2ecc71', fg='white', font=('Arial', 10)).grid(row=7, column=0, columnspan=3, pady=20)
        
        self.create_notes_section(notes_frame)
        
    def create_wells_calculator(self):
        """Wells Score for DVT Calculator"""
        calc_frame, result_frame, notes_frame = self.create_calculator_frame("Wells Score for DVT")
        
        # Create variables for each criterion
        criteria = [
            ("Active cancer (treatment ongoing or within 6 months)", 1),
            ("Paralysis, paresis, or recent plaster immobilization", 1),
            ("Recently bedridden for >3 days or major surgery within 12 weeks", 1),
            ("Localized tenderness along distribution of deep venous system", 1),
            ("Entire leg swollen", 1),
            ("Calf swelling >3 cm compared to asymptomatic leg", 1),
            ("Pitting edema confined to symptomatic leg", 1),
            ("Collateral superficial veins (non-varicose)", 1),
            ("Previously documented DVT", 1),
            ("Alternative diagnosis at least as likely as DVT", -2)
        ]
        
        criterion_vars = []
        for i, (criterion, points) in enumerate(criteria):
            var = tk.IntVar()
            criterion_vars.append((var, points))
            cb = tk.Checkbutton(calc_frame, text=f"{criterion} ({points:+d} point{'s' if abs(points) != 1 else ''})",
                               variable=var, bg='white', anchor='w', justify='left')
            cb.grid(row=i, column=0, sticky='w', pady=2, padx=5)
        
        result_label = tk.Label(result_frame, text="Wells Score: -- | Risk: --", 
                               font=('Arial', 12, 'bold'))
        result_label.pack(pady=10)
        
        def calculate_wells():
            total_score = sum(var.get() * points for var, points in criterion_vars)
            
            # Risk interpretation
            if total_score >= 2:
                risk = "High (DVT likely - consider imaging)"
            elif total_score >= 1:
                risk = "Moderate"
            else:
                risk = "Low (DVT unlikely)"
                
            result_text = f"Wells Score: {total_score} | Risk: {risk}"
            result_label.config(text=result_text)
            
            # Create summary of selected criteria
            selected = [criteria[i][0] for i, (var, _) in enumerate(criterion_vars) if var.get()]
            summary = "; ".join(selected) if selected else "No criteria selected"
            
            self.save_calculation('Wells DVT', summary, result_text)
            
        tk.Button(calc_frame, text="Calculate Wells Score", command=calculate_wells,
                 bg='#2ecc71', fg='white', font=('Arial', 10)).grid(row=len(criteria), column=0, pady=20)
        
        self.create_notes_section(notes_frame)
        
    def create_apgar_calculator(self):
        """APGAR Score Calculator"""
        calc_frame, result_frame, notes_frame = self.create_calculator_frame("APGAR Score")
        
        # APGAR criteria
        criteria = [
            ("Heart Rate", ["Absent", "< 100 bpm", "> 100 bpm"]),
            ("Respiratory Effort", ["Absent", "Weak cry", "Strong cry"]),
            ("Muscle Tone", ["Flaccid", "Some flexion", "Active motion"]),
            ("Reflex Response", ["No response", "Grimace", "Cry/cough"]),
            ("Color", ["Blue/pale", "Body pink, extremities blue", "Completely pink"])
        ]
        
        apgar_vars = []
        for i, (criterion, options) in enumerate(criteria):
            tk.Label(calc_frame, text=f"{criterion}:", font=('Arial', 10, 'bold')).grid(row=i*4, column=0, sticky='w', pady=(10,0))
            
            var = tk.IntVar()
            apgar_vars.append(var)
            
            for j, option in enumerate(options):
                tk.Radiobutton(calc_frame, text=f"{j}: {option}", 
                              variable=var, value=j, bg='white').grid(row=i*4+j+1, column=0, sticky='w', padx=20)
        
        result_label = tk.Label(result_frame, text="APGAR Score: -- | Status: --", 
                               font=('Arial', 12, 'bold'))
        result_label.pack(pady=10)
        
        def calculate_apgar():
            total_score = sum(var.get() for var in apgar_vars)
            
            # Interpretation
            if total_score >= 7:
                status = "Normal"
            elif total_score >= 4:
                status = "Moderately depressed"
            else:
                status = "Severely depressed"
                
            result_text = f"APGAR Score: {total_score}/10 | Status: {status}"
            result_label.config(text=result_text)
            
            # Create detailed breakdown
            breakdown = [f"{criteria[i][0]}: {var.get()}" for i, var in enumerate(apgar_vars)]
            summary = "; ".join(breakdown)
            
            self.save_calculation('APGAR', summary, result_text)
            
        tk.Button(calc_frame, text="Calculate APGAR", command=calculate_apgar,
                 bg='#2ecc71', fg='white', font=('Arial', 10)).grid(row=len(criteria)*4+1, column=0, pady=20)
        
        self.create_notes_section(notes_frame)
        
    def create_pediatric_calculator(self):
        """Pediatric Weight-Based Dosing Calculator"""
        calc_frame, result_frame, notes_frame = self.create_calculator_frame("Pediatric Dosing Calculator")
        
        tk.Label(calc_frame, text="Child's Weight (kg):").grid(row=0, column=0, sticky='w', pady=5)
        weight_entry = tk.Entry(calc_frame)
        weight_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(calc_frame, text="Dose per kg (mg/kg):").grid(row=1, column=0, sticky='w', pady=5)
        dose_entry = tk.Entry(calc_frame)
        dose_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(calc_frame, text="Frequency (doses per day):").grid(row=2, column=0, sticky='w', pady=5)
        freq_entry = tk.Entry(calc_frame)
        freq_entry.grid(row=2, column=1, padx=10, pady=5)
        
        result_text = tk.Text(result_frame, height=6, width=50)
        result_text.pack(pady=10)
        
        def calculate_pediatric_dose():
            try:
                weight = float(weight_entry.get())
                dose_per_kg = float(dose_entry.get())
                frequency = int(freq_entry.get())
                
                total_daily_dose = weight * dose_per_kg
                single_dose = total_daily_dose / frequency
                
                results = f"""Pediatric Dosing Calculation:
                
Child's Weight: {weight} kg
Dose: {dose_per_kg} mg/kg

Single Dose: {single_dose:.1f} mg
Total Daily Dose: {total_daily_dose:.1f} mg
Frequency: {frequency} times per day

Note: Always verify against pediatric dosing guidelines and maximum adult doses."""
                
                result_text.delete(1.0, tk.END)
                result_text.insert(1.0, results)
                
                summary = f"Weight: {weight}kg, {dose_per_kg}mg/kg, {frequency}x/day"
                calc_result = f"Single dose: {single_dose:.1f}mg, Daily: {total_daily_dose:.1f}mg"
                self.save_calculation('Pediatric Dosing', summary, calc_result)
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers")
                
        tk.Button(calc_frame, text="Calculate Dose", command=calculate_pediatric_dose,
                 bg='#2ecc71', fg='white', font=('Arial', 10)).grid(row=3, column=0, columnspan=2, pady=10)
        
        self.create_notes_section(notes_frame)
        
    def create_chads2_calculator(self):
        """CHADS₂ Score Calculator for Stroke Risk"""
        calc_frame, result_frame, notes_frame = self.create_calculator_frame("CHADS₂ Score (Stroke Risk)")
        
        criteria = [
            ("Congestive heart failure", 1),
            ("Hypertension", 1),
            ("Age ≥ 75 years", 1),
            ("Diabetes mellitus", 1),
            ("Prior stroke or TIA", 2)
        ]
        
        chads_vars = []
        for i, (criterion, points) in enumerate(criteria):
            var = tk.IntVar()
            chads_vars.append((var, points))
            cb = tk.Checkbutton(calc_frame, text=f"{criterion} ({points} point{'s' if points > 1 else ''})",
                               variable=var, bg='white')
            cb.grid(row=i, column=0, sticky='w', pady=5, padx=5)
        
        result_label = tk.Label(result_frame, text="CHADS₂ Score: -- | Risk: --", 
                               font=('Arial', 12, 'bold'))
        result_label.pack(pady=10)
        
        def calculate_chads2():
            total_score = sum(var.get() * points for var, points in chads_vars)
            
            # Risk interpretation and recommendation
            if total_score == 0:
                risk = "Low (0.5% annual stroke risk)"
                recommendation = "Aspirin or no therapy"
            elif total_score == 1:
                risk = "Low-Moderate (1.5% annual stroke risk)"
                recommendation = "Aspirin or anticoagulation"
            elif total_score == 2:
                risk = "Moderate (2.5% annual stroke risk)"
                recommendation = "Anticoagulation recommended"
            else:
                risk = f"High ({1.5 + (total_score-1)*1.5:.1f}% annual stroke risk)"
                recommendation = "Anticoagulation strongly recommended"
                
            result_text = f"CHADS₂ Score: {total_score} | Risk: {risk}"
            result_label.config(text=result_text)
            
            # Show recommendation
            rec_label = tk.Label(result_frame, text=f"Recommendation: {recommendation}", 
                               font=('Arial', 10), fg='#2c3e50')
            # Clear previous recommendation labels
            for widget in result_frame.winfo_children():
                if isinstance(widget, tk.Label) and "Recommendation" in widget.cget("text"):
                    widget.destroy()
            rec_label.pack()
            
            selected = [criteria[i][0] for i, (var, _) in enumerate(chads_vars) if var.get()]
            summary = "; ".join(selected) if selected else "No risk factors"
            
            self.save_calculation('CHADS2', summary, f"{result_text} | {recommendation}")
            
        tk.Button(calc_frame, text="Calculate CHADS₂", command=calculate_chads2,
                 bg='#2ecc71', fg='white', font=('Arial', 10)).grid(row=len(criteria), column=0, pady=20)
        
        self.create_notes_section(notes_frame)
        
    def create_notes_section(self, parent_frame):
        """Create notes section for patient information"""
        tk.Label(parent_frame, text="Patient Notes:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10,5))
        
        notes_text = scrolledtext.ScrolledText(parent_frame, height=8, width=60)
        notes_text.pack(fill='both', expand=True, pady=5)
        
        def save_notes():
            notes = notes_text.get(1.0, tk.END).strip()
            if notes:
                # Save to database with current timestamp
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO patient_notes (timestamp, calculator_type, patient_info, notes)
                    VALUES (?, ?, ?, ?)
                ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Manual Note', '', notes))
                conn.commit()
                conn.close()
                messagebox.showinfo("Saved", "Notes saved successfully!")
                
        tk.Button(parent_frame, text="Save Notes", command=save_notes,
                 bg='#34495e', fg='white', font=('Arial', 9)).pack(pady=5)
        
    def save_calculation(self, calc_type, inputs, result, patient_info=""):
        """Save calculation to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patient_notes (timestamp, calculator_type, patient_info, calculation_result, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), calc_type, patient_info, result, inputs))
        conn.commit()
        conn.close()
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = QuickMedCalc()
    app.run()