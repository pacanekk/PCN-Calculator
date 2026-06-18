#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ThemeManager:
    """Manages modern theme"""
    
    def __init__(self):
        # Modern Dark Theme Colors
        self.colors = {
            # Background colors
            "bg_main": "#1e1e1e",           # Główne tło
            "bg_secondary": "#252526",     # Drugie tło
            "bg_tertiary": "#2d2d2d",      # Trzecie tło (display)
            "bg_hover": "#3c3c3c",         # Hover
            
            # Button colors
            "btn_number": "#3b3b3b",       # Przyciski numeryczne
            "btn_number_hover": "#4a4a4a",
            "btn_operator": "#ff9f0a",      # Przyciski operatorów
            "btn_operator_hover": "#ffb340",
            "btn_function": "#5c5c5c",     # Przyciski funkcji
            "btn_function_hover": "#6c6c6c",
            "btn_equals": "#ff9f0a",       # Przycisk =
            "btn_equals_hover": "#ffb340",
            
            # Text colors
            "text_primary": "#ffffff",     # Główny tekst
            "text_secondary": "#aaaaaa",   # Drugorzędny tekst
            "text_disabled": "#666666",    # Wyłączony tekst
            
            # Accent colors
            "accent": "#0078d4",           # Akcent Windows
            "accent_hover": "#1084d8",
            
            # Border colors
            "border": "#404040",           # Obramowanie
            "border_focus": "#0078d4",     # Obramowanie focus
            
            # Special
            "error": "#e81123",            # Błąd
            "success": "#107c10",          # Sukces
        }
        
        # Font configurations
        self.fonts = {
            "display_large": ("Segoe UI", 52, "bold"),
            "display_small": ("Segoe UI", 22, "normal"),
            "button_number": ("Segoe UI", 28, "normal"),
            "button_operator": ("Segoe UI", 30, "bold"),
            "button_function": ("Segoe UI", 20, "normal"),
            "button_scientific": ("Segoe UI", 16, "normal"),
            "label": ("Segoe UI", 16, "normal"),
            "history": ("Segoe UI", 16, "normal"),
        }
        
        # Corner radius (modern style)
        self.corner_radius = {
            "small": 8,
            "medium": 12,
            "large": 16,
            "xlarge": 20,
        }
        
        # Padding and spacing
        self.spacing = {
            "tiny": 4,
            "small": 8,
            "medium": 12,
            "large": 16,
            "xlarge": 24,
        }
    
    def get_color(self, name: str) -> str:
        """Zwraca kolor o podanej nazwie"""
        return self.colors.get(name, "#ffffff")
    
    def get_font(self, name: str) -> tuple:
        """Zwraca czcionkę o podanej nazwie"""
        return self.fonts.get(name, ("Segoe UI", 12, "normal"))
    
    def get_corner_radius(self, size: str = "medium") -> int:
        """Zwraca promień zaokrąglenia"""
        return self.corner_radius.get(size, 12)
    
    def get_spacing(self, size: str = "medium") -> int:
        """Zwraca odstęp"""
        return self.spacing.get(size, 12)
    
    def get_button_style(self, button_type: str) -> dict:
        """Zwraca styl przycisku"""
        styles = {
            "number": {
                "fg_color": self.colors["btn_number"],
                "hover_color": self.colors["btn_number_hover"],
                "text_color": self.colors["text_primary"],
                "corner_radius": self.corner_radius["medium"],
                "font": self.fonts["button_number"],
            },
            "operator": {
                "fg_color": self.colors["btn_operator"],
                "hover_color": self.colors["btn_operator_hover"],
                "text_color": self.colors["text_primary"],
                "corner_radius": self.corner_radius["medium"],
                "font": self.fonts["button_operator"],
            },
            "function": {
                "fg_color": self.colors["btn_function"],
                "hover_color": self.colors["btn_function_hover"],
                "text_color": self.colors["text_primary"],
                "corner_radius": self.corner_radius["medium"],
                "font": self.fonts["button_function"],
            },
            "equals": {
                "fg_color": self.colors["btn_equals"],
                "hover_color": self.colors["btn_equals_hover"],
                "text_color": self.colors["text_primary"],
                "corner_radius": self.corner_radius["medium"],
                "font": self.fonts["button_operator"],
            },
            "scientific": {
                "fg_color": self.colors["btn_function"],
                "hover_color": self.colors["btn_function_hover"],
                "text_color": self.colors["text_primary"],
                "corner_radius": self.corner_radius["small"],
                "font": self.fonts["button_scientific"],
            },
        }
        return styles.get(button_type, styles["number"])
