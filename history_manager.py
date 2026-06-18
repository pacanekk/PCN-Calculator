#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict, Optional
from datetime import datetime
import json
import os

class HistoryManager:
    """Zarządza historią obliczeń"""
    
    def __init__(self, max_entries: int = 100):
        self.max_entries = max_entries
        self.history: List[Dict[str, str]] = []
        self.history_file = "calculator_history.json"
        self.load_history()
    
    def add_entry(self, expression: str, result: str) -> None:
        """Dodaje wpis do historii"""
        entry = {
            "expression": expression,
            "result": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.history.insert(0, entry)
        
        # Ogranicz liczbę wpisów
        if len(self.history) > self.max_entries:
            self.history = self.history[:self.max_entries]
        
        self.save_history()
    
    def get_history(self) -> List[Dict[str, str]]:
        """Zwraca całą historię"""
        return self.history
    
    def clear_history(self) -> None:
        """Czyści historię"""
        self.history = []
        self.save_history()
    
    def delete_entry(self, index: int) -> None:
        """Usuwa wpis o podanym indeksie"""
        if 0 <= index < len(self.history):
            self.history.pop(index)
            self.save_history()
    
    def save_history(self) -> None:
        """Zapisuje historię do pliku"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Błąd przy zapisywaniu historii: {e}")
    
    def load_history(self) -> None:
        """Wczytuje historię z pliku"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Błąd przy wczytywaniu historii: {e}")
            self.history = []
    
    def get_entry(self, index: int) -> Optional[Dict[str, str]]:
        """Zwraca wpis o podanym indeksie"""
        if 0 <= index < len(self.history):
            return self.history[index]
        return None
    
    def search_history(self, query: str) -> List[Dict[str, str]]:
        """Wyszukuje wpisy w historii"""
        query = query.lower()
        results = []
        for entry in self.history:
            if query in entry["expression"].lower() or query in entry["result"].lower():
                results.append(entry)
        return results
