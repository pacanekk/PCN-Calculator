#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Add module path for system installation
if os.path.exists("/usr/share/pcn-calculator"):
    sys.path.insert(0, "/usr/share/pcn-calculator")

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import math
from calculator_engine import CalculatorEngine
from history_manager import HistoryManager
from theme_manager import ThemeManager

class CalculatorApp(ctk.CTk):
    """Main calculator application with modern style"""
    
    def __init__(self):
        super().__init__()
        
        # Inicjalizacja komponentów
        self.engine = CalculatorEngine()
        self.history_manager = HistoryManager()
        self.theme = ThemeManager()
        
        # Stan aplikacji
        self.current_expression = ""
        self.current_result = "0"
        self.is_scientific_mode = False
        self.history_visible = False
        
        # Konfiguracja okna
        self.setup_window()
        
        # Konfiguracja customtkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Budowanie UI
        self.create_ui()
        
        # Obsługa klawiatury
        self.bind_keyboard()
    
    def setup_window(self):
        """Configure main window"""
        self.title("PCN Calculator")
        self.geometry("500x750")
        self.minsize(450, 650)
        self.configure(fg_color=self.theme.get_color("bg_main"))
        
        # Set icon (optional)
        try:
            import tkinter as tk
            # Check system icon location first (RPM install)
            icon_path = "/usr/share/icons/hicolor/256x256/apps/pcn-calculator.png"
            if not os.path.exists(icon_path):
                # Fall back to local icon
                icon_path = "icon.png"
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.iconphoto(True, icon)
        except Exception as e:
            # Icon is optional, continue without it
            pass
    
    def create_ui(self):
        """Budowanie interfejsu użytkownika"""
        # Główny container
        self.main_container = ctk.CTkFrame(
            self,
            fg_color=self.theme.get_color("bg_main"),
            corner_radius=0
        )
        self.main_container.pack(fill="both", expand=True)
        
        # Header z przyciskami trybu i historii
        self.create_header()
        
        # Panel główny (kalkulator + historia)
        self.content_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=self.theme.get_color("bg_main"),
            corner_radius=0
        )
        self.content_frame.pack(fill="both", expand=True, padx=self.theme.get_spacing("large"), pady=self.theme.get_spacing("medium"))
        
        # Panel kalkulatora
        self.calculator_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.theme.get_color("bg_secondary"),
            corner_radius=self.theme.get_corner_radius("large")
        )
        self.calculator_frame.grid(row=0, column=0, sticky="nsew")
        
        # Panel historii (ukryty domyślnie)
        self.history_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.theme.get_color("bg_secondary"),
            corner_radius=self.theme.get_corner_radius("large"),
            width=280
        )
        # Historia jest ukryta na początku (nie gridujemy)
        
        # Konfiguracja grid
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=0)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Wyświetlacz
        self.create_display()
        
        # Panel przycisków
        self.button_frame = ctk.CTkFrame(
            self.calculator_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.button_frame.pack(fill="both", expand=True, padx=self.theme.get_spacing("medium"), pady=self.theme.get_spacing("medium"))
        
        # Przyciski standardowe
        self.create_standard_buttons()
        
        # Panel naukowy (ukryty domyślnie)
        self.scientific_frame = ctk.CTkFrame(
            self.calculator_frame,
            fg_color=self.theme.get_color("bg_tertiary"),
            corner_radius=self.theme.get_corner_radius("medium")
        )
        # Panel naukowy jest ukryty na początku
    
    def create_header(self):
        """Tworzy header z przyciskami trybu i historii"""
        header = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent",
            height=50
        )
        header.pack(fill="x", padx=self.theme.get_spacing("large"), pady=self.theme.get_spacing("medium"))
        header.pack_propagate(False)
        
        # Przycisk trybu
        self.mode_button = ctk.CTkButton(
            header,
            text="Standard",
            font=self.theme.get_font("label"),
            fg_color=self.theme.get_color("btn_function"),
            hover_color=self.theme.get_color("btn_function_hover"),
            text_color=self.theme.get_color("text_primary"),
            corner_radius=self.theme.get_corner_radius("small"),
            width=100,
            command=self.toggle_mode
        )
        self.mode_button.pack(side="left", padx=self.theme.get_spacing("small"))
        
        # History button
        self.history_button = ctk.CTkButton(
            header,
            text="History",
            font=self.theme.get_font("label"),
            fg_color=self.theme.get_color("btn_function"),
            hover_color=self.theme.get_color("btn_function_hover"),
            text_color=self.theme.get_color("text_primary"),
            corner_radius=self.theme.get_corner_radius("small"),
            width=100,
            command=self.toggle_history
        )
        self.history_button.pack(side="right", padx=self.theme.get_spacing("small"))
    
    def create_display(self):
        """Tworzy wyświetlacz z historią i wynikiem"""
        display_container = ctk.CTkFrame(
            self.calculator_frame,
            fg_color=self.theme.get_color("bg_tertiary"),
            corner_radius=self.theme.get_corner_radius("medium")
        )
        display_container.pack(fill="x", padx=self.theme.get_spacing("medium"), pady=self.theme.get_spacing("medium"))
        
        # Historia bieżącego działania
        self.history_display = ctk.CTkLabel(
            display_container,
            text="",
            font=self.theme.get_font("display_small"),
            text_color=self.theme.get_color("text_secondary"),
            anchor="e"
        )
        self.history_display.pack(fill="x", padx=self.theme.get_spacing("large"), pady=(self.theme.get_spacing("medium"), 0))
        
        # Główny wynik (Entry dla możliwości kopiowania)
        self.result_display = ctk.CTkEntry(
            display_container,
            font=self.theme.get_font("display_large"),
            text_color=self.theme.get_color("text_primary"),
            fg_color="transparent",
            border_width=0,
            corner_radius=0,
            justify="right"
        )
        self.result_display.insert(0, "0")
        self.result_display.pack(fill="x", padx=self.theme.get_spacing("large"), pady=(0, self.theme.get_spacing("medium")))
    
    def create_standard_buttons(self):
        """Tworzy przyciski trybu standardowego"""
        # Układ przycisków
        button_layout = [
            # Row 0
            ["C", "CE", "⌫", "÷"],
            # Row 1
            ["7", "8", "9", "×"],
            # Row 2
            ["4", "5", "6", "−"],
            # Row 3
            ["1", "2", "3", "+"],
            # Row 4
            ["±", "0", ".", "="],
        ]
        
        for row_idx, row in enumerate(button_layout):
            for col_idx, button_text in enumerate(row):
                self.create_button(button_text, row_idx, col_idx)
    
    def create_button(self, text: str, row: int, col: int):
        """Tworzy pojedynczy przycisk"""
        # Określ typ przycisku
        if text in ["+", "−", "×", "÷"]:
            button_type = "operator"
        elif text in ["=", "C", "CE", "⌫", "±"]:
            button_type = "function"
        else:
            button_type = "number"
        
        style = self.theme.get_button_style(button_type)
        
        button = ctk.CTkButton(
            self.button_frame,
            text=text,
            font=style["font"],
            fg_color=style["fg_color"],
            hover_color=style["hover_color"],
            text_color=style["text_color"],
            corner_radius=style["corner_radius"],
            command=lambda t=text: self.on_button_click(t)
        )
        
        # Grid configuration
        button.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
        
        # Configure grid weights
        self.button_frame.grid_rowconfigure(row, weight=1)
        self.button_frame.grid_columnconfigure(col, weight=1)
    
    def create_scientific_buttons(self):
        """Tworzy przyciski trybu naukowego"""
        scientific_buttons = [
            ["sin", "cos", "tan"],
            ["log", "ln", "√"],
            ["x²", "xʸ", "1/x"],
            ["(", ")", "%"],
            ["π", "e", "10^x"],
        ]
        
        for row_idx, row in enumerate(scientific_buttons):
            for col_idx, button_text in enumerate(row):
                style = self.theme.get_button_style("scientific")
                
                button = ctk.CTkButton(
                    self.scientific_frame,
                    text=button_text,
                    font=style["font"],
                    fg_color=style["fg_color"],
                    hover_color=style["hover_color"],
                    text_color=style["text_color"],
                    corner_radius=style["corner_radius"],
                    command=lambda t=button_text: self.on_scientific_click(t)
                )
                
                button.grid(row=row_idx, column=col_idx, sticky="nsew", padx=2, pady=2)
                self.scientific_frame.grid_rowconfigure(row_idx, weight=1)
                self.scientific_frame.grid_columnconfigure(col_idx, weight=1)
    
    def create_history_panel(self):
        """Create history panel"""
        # History header
        history_header = ctk.CTkFrame(
            self.history_frame,
            fg_color="transparent"
        )
        history_header.pack(fill="x", padx=self.theme.get_spacing("medium"), pady=self.theme.get_spacing("medium"))
        
        title_label = ctk.CTkLabel(
            history_header,
            text="History",
            font=self.theme.get_font("button_operator"),
            text_color=self.theme.get_color("text_primary")
        )
        title_label.pack(side="left")
        
        clear_button = ctk.CTkButton(
            history_header,
            text="Clear",
            font=self.theme.get_font("button_function"),
            fg_color="transparent",
            hover_color=self.theme.get_color("bg_hover"),
            text_color=self.theme.get_color("text_secondary"),
            corner_radius=self.theme.get_corner_radius("small"),
            width=60,
            height=30,
            command=self.clear_history
        )
        clear_button.pack(side="right")
        
        # Lista historii
        self.history_listbox = ctk.CTkScrollableFrame(
            self.history_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.history_listbox.pack(fill="both", expand=True, padx=self.theme.get_spacing("medium"), pady=self.theme.get_spacing("small"))
        
        self.refresh_history_display()
    
    def on_button_click(self, text: str):
        """Obsługa kliknięcia przycisku"""
        if text == "C":
            self.clear_all()
        elif text == "CE":
            self.clear_entry()
        elif text == "⌫":
            self.backspace()
        elif text == "±":
            self.negate()
        elif text == "=":
            self.calculate()
        elif text in ["+", "−", "×", "÷"]:
            self.add_operator(text)
        elif text == ".":
            self.add_decimal()
        else:
            self.add_digit(text)
    
    def on_scientific_click(self, text: str):
        """Obsługa kliknięcia przycisku naukowego"""
        if text in ["sin", "cos", "tan", "log", "ln", "√"]:
            self.add_function(text)
        elif text == "x²":
            self.add_function("square")
        elif text == "xʸ":
            self.add_operator("^")
        elif text == "1/x":
            self.add_function("reciprocal")
        elif text == "10^x":
            self.add_function("10pow")
        elif text in ["(", ")"]:
            self.add_parenthesis(text)
        elif text == "%":
            self.add_operator("%")
        elif text == "π":
            self.add_constant("π")
        elif text == "e":
            self.add_constant("e")
    
    def add_digit(self, digit: str):
        """Dodaje cyfrę do wyrażenia"""
        if self.current_result == "0" or self.current_result == "Błąd":
            self.current_result = digit
        else:
            self.current_result += digit
        self.update_display()
    
    def add_operator(self, operator: str):
        """Dodaje operator do wyrażenia"""
        self.current_result += operator
        self.update_display()
    
    def add_decimal(self):
        """Dodaje przecinek"""
        if "." not in self.current_result:
            self.current_result += "."
        self.update_display()
    
    def add_function(self, func: str):
        """Dodaje funkcję"""
        if func == "square":
            self.current_result += "^2"
        elif func == "reciprocal":
            self.current_result = "1/(" + self.current_result + ")"
        elif func == "10pow":
            self.current_result = "10^(" + self.current_result + ")"
        else:
            self.current_result += func + "("
        self.update_display()
    
    def add_parenthesis(self, paren: str):
        """Dodaje nawias"""
        self.current_result += paren
        self.update_display()
    
    def add_constant(self, const: str):
        """Dodaje stałą"""
        if self.current_result == "0":
            self.current_result = const
        else:
            self.current_result += const
        self.update_display()
    
    def clear_all(self):
        """Czyści wszystko"""
        self.current_expression = ""
        self.current_result = "0"
        self.update_display()
    
    def clear_entry(self):
        """Czyści bieżący wpis"""
        self.current_result = "0"
        self.update_display()
    
    def backspace(self):
        """Usuwa ostatni znak"""
        if len(self.current_result) > 1:
            self.current_result = self.current_result[:-1]
        else:
            self.current_result = "0"
        self.update_display()
    
    def negate(self):
        """Zmienia znak"""
        if self.current_result != "0":
            if self.current_result.startswith("-"):
                self.current_result = self.current_result[1:]
            else:
                self.current_result = "-" + self.current_result
        self.update_display()
    
    def calculate(self):
        """Oblicza wynik"""
        expression = self.current_result
        # Konwertuj symbole Unicode na ASCII dla parsera
        expression = expression.replace('×', '*').replace('÷', '/').replace('−', '-')
        result = self.engine.evaluate(expression)
        
        if isinstance(result, str) and result.startswith("Błąd"):
            self.current_result = result
        else:
            # Zapisz do historii
            self.history_manager.add_entry(expression, str(result))
            self.refresh_history_display()
            
            self.current_expression = expression
            self.current_result = str(result)
        
        self.update_display()
    
    def update_display(self):
        """Aktualizuje wyświetlacz"""
        self.result_display.delete(0, "end")
        self.result_display.insert(0, self.current_result)
        
        if self.current_expression:
            self.history_display.configure(text=self.current_expression + " =")
        else:
            self.history_display.configure(text="")
    
    def toggle_mode(self):
        """Przełącza tryb standardowy/naukowy"""
        self.is_scientific_mode = not self.is_scientific_mode
        
        if self.is_scientific_mode:
            self.mode_button.configure(text="Scientific")
            
            # Pokaż panel naukowy
            if not hasattr(self, 'scientific_buttons_created'):
                self.create_scientific_buttons()
                self.scientific_buttons_created = True
            
            self.scientific_frame.pack(fill="x", padx=self.theme.get_spacing("medium"), pady=(0, self.theme.get_spacing("medium")))
        else:
            self.mode_button.configure(text="Standard")
            self.scientific_frame.pack_forget()
    
    def toggle_history(self):
        """Toggle history panel"""
        self.history_visible = not self.history_visible
        
        if self.history_visible:
            self.history_button.configure(text="✕ History")
            
            if not hasattr(self, 'history_panel_created'):
                self.create_history_panel()
                self.history_panel_created = True
            
            # Show history in grid
            self.history_frame.grid(row=0, column=1, sticky="nsew", padx=(self.theme.get_spacing("small"), 0))
        else:
            self.history_button.configure(text="History")
            self.history_frame.grid_forget()
    
    def refresh_history_display(self):
        """Odświeża wyświetlanie historii"""
        if hasattr(self, 'history_listbox'):
            # Wyczyść
            for widget in self.history_listbox.winfo_children():
                widget.destroy()
            
            # Dodaj wpisy
            history = self.history_manager.get_history()
            for entry in history:
                self.create_history_entry(entry)
    
    def create_history_entry(self, entry: dict):
        """Tworzy wpis historii"""
        entry_frame = ctk.CTkFrame(
            self.history_listbox,
            fg_color=self.theme.get_color("bg_tertiary"),
            corner_radius=self.theme.get_corner_radius("small")
        )
        entry_frame.pack(fill="x", pady=2)
        
        # Wyrażenie (Entry dla możliwości kopiowania)
        expr_entry = ctk.CTkEntry(
            entry_frame,
            font=self.theme.get_font("history"),
            text_color=self.theme.get_color("text_secondary"),
            fg_color="transparent",
            border_width=0,
            corner_radius=0,
            justify="left"
        )
        expr_entry.insert(0, entry["expression"])
        expr_entry.pack(fill="x", padx=self.theme.get_spacing("small"), pady=(self.theme.get_spacing("small"), 0))
        
        # Wynik (Entry dla możliwości kopiowania)
        result_entry = ctk.CTkEntry(
            entry_frame,
            font=self.theme.get_font("button_operator"),
            text_color=self.theme.get_color("text_primary"),
            fg_color="transparent",
            border_width=0,
            corner_radius=0,
            justify="left"
        )
        result_entry.insert(0, f"= {entry['result']}")
        result_entry.pack(fill="x", padx=self.theme.get_spacing("small"), pady=(0, self.theme.get_spacing("small")))
        
        # Kliknięcie prawym przyciskiem wstawia wynik
        entry_frame.bind("<Button-3>", lambda e, r=entry["result"]: self.insert_from_history(r))
        expr_entry.bind("<Button-3>", lambda e, r=entry["result"]: self.insert_from_history(r))
        result_entry.bind("<Button-3>", lambda e, r=entry["result"]: self.insert_from_history(r))
    
    def insert_from_history(self, result: str):
        """Wstawia wynik z historii"""
        self.current_result = result
        self.update_display()
    
    def clear_history(self):
        """Czyści historię"""
        self.history_manager.clear_history()
        self.refresh_history_display()
    
    def bind_keyboard(self):
        """Binduje klawisze klawiatury"""
        self.bind("<Key>", self.on_key_press)
    
    def on_key_press(self, event):
        """Obsługa naciśnięcia klawisza"""
        key = event.char
        
        if key.isdigit():
            self.add_digit(key)
        elif key == ".":
            self.add_decimal()
        elif key == "+":
            self.add_operator("+")
        elif key == "-":
            self.add_operator("−")
        elif key == "*":
            self.add_operator("×")
        elif key == "/":
            self.add_operator("÷")
        elif key == "\r" or key == "=":
            self.calculate()
        elif key == "\x08":  # Backspace
            self.backspace()
        elif key == "\x1b":  # Escape
            self.clear_all()
        elif key == "(" or key == ")":
            self.add_parenthesis(key)
        elif key == "^":
            self.add_operator("^")
        elif key == "%":
            self.add_operator("%")

def main():
    app = CalculatorApp()
    app.mainloop()

if __name__ == "__main__":
    main()
