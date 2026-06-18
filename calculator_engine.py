#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import re
from typing import List, Union, Optional

class CalculatorEngine:
    """Silnik kalkulatora - parser i obliczanie wyrażeń bez eval()"""
    
    def __init__(self):
        self.constants = {
            'π': math.pi,
            'e': math.e,
            'pi': math.pi,
        }
        
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log10,
            'ln': math.log,
            'sqrt': math.sqrt,
            'abs': abs,
        }
    
    def evaluate(self, expression: str) -> Union[float, str]:
        """
        Oblicza wyrażenie matematyczne bez użycia eval()
        Obsługuje: +, -, *, /, ^, %, (), funkcje, stałe
        """
        try:
            # Usuń białe znaki
            expr = expression.replace(' ', '')
            
            if not expr:
                return 0
            
            # Zastąp stałe
            for const, value in self.constants.items():
                expr = expr.replace(const, str(value))
            
            # Parsuj i oblicz
            result = self._parse_expression(expr)
            
            # Zaokrąglij jeśli jest blisko liczby całkowitej
            if abs(result - round(result)) < 1e-10:
                result = round(result)
            
            return result
            
        except ZeroDivisionError:
            return "Błąd: Dzielenie przez zero"
        except ValueError as e:
            return f"Błąd: {str(e)}"
        except Exception as e:
            return f"Błąd: {str(e)}"
    
    def _parse_expression(self, expr: str) -> float:
        """Główny parser - obsługuje operatorów z różnym priorytetem"""
        return self._parse_addition_subtraction(expr)
    
    def _parse_addition_subtraction(self, expr: str) -> float:
        """Parsuje + i - (najniższy priorytet)"""
        tokens = self._split_by_operators(expr, ['+', '-'], preserve=True)
        
        if len(tokens) == 1:
            return self._parse_multiplication_division(tokens[0])
        
        result = self._parse_multiplication_division(tokens[0])
        
        i = 1
        while i < len(tokens):
            operator = tokens[i]
            next_value = self._parse_multiplication_division(tokens[i + 1])
            
            if operator == '+':
                result += next_value
            elif operator == '-':
                result -= next_value
            
            i += 2
        
        return result
    
    def _parse_multiplication_division(self, expr: str) -> float:
        """Parsuje *, /, % (średni priorytet)"""
        tokens = self._split_by_operators(expr, ['*', '/', '%'], preserve=True)
        
        if len(tokens) == 1:
            return self._parse_power(tokens[0])
        
        result = self._parse_power(tokens[0])
        
        i = 1
        while i < len(tokens):
            operator = tokens[i]
            next_value = self._parse_power(tokens[i + 1])
            
            if operator == '*':
                result *= next_value
            elif operator == '/':
                if next_value == 0:
                    raise ZeroDivisionError()
                result /= next_value
            elif operator == '%':
                result %= next_value
            
            i += 2
        
        return result
    
    def _parse_power(self, expr: str) -> float:
        """Parsuje ^ (wysoki priorytet)"""
        tokens = self._split_by_operators(expr, ['^'], preserve=True)
        
        if len(tokens) == 1:
            return self._parse_unary(tokens[0])
        
        result = self._parse_unary(tokens[0])
        
        i = 1
        while i < len(tokens):
            next_value = self._parse_unary(tokens[i + 1])
            result **= next_value
            i += 2
        
        return result
    
    def _parse_unary(self, expr: str) -> float:
        """Parsuje operatory unarne (+, -) i funkcje"""
        # Obsługa funkcji
        for func_name, func in self.functions.items():
            if expr.startswith(func_name + '(') and expr.endswith(')'):
                inner = expr[len(func_name)+1:-1]
                inner_value = self._parse_expression(inner)
                return func(inner_value)
        
        # Obsługa unarnego +/-
        if expr.startswith('+'):
            return self._parse_unary(expr[1:])
        if expr.startswith('-'):
            return -self._parse_unary(expr[1:])
        
        return self._parse_parentheses(expr)
    
    def _parse_parentheses(self, expr: str) -> float:
        """Parsuje nawiasy"""
        if expr.startswith('(') and expr.endswith(')'):
            # Sprawdź czy to są pasujące nawiasy
            depth = 0
            for i, char in enumerate(expr):
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                if depth == 0 and i == len(expr) - 1:
                    return self._parse_expression(expr[1:-1])
        
        return self._parse_number(expr)
    
    def _parse_number(self, expr: str) -> float:
        """Parsuje liczbę"""
        try:
            return float(expr)
        except ValueError:
            raise ValueError(f"Nieprawidłowe wyrażenie: {expr}")
    
    def _split_by_operators(self, expr: str, operators: List[str], preserve: bool = False) -> List[str]:
        """
        Dzieli wyrażenie przez operatory z uwzględnieniem nawiasów
        preserve=True zachowuje operatory w wyniku
        """
        if not expr:
            return []
        
        tokens = []
        current = ""
        depth = 0
        
        for char in expr:
            if char == '(':
                depth += 1
                current += char
            elif char == ')':
                depth -= 1
                current += char
            elif char in operators and depth == 0:
                if preserve:
                    tokens.append(current)
                    tokens.append(char)
                else:
                    tokens.append(current)
                current = ""
            else:
                current += char
        
        if current:
            tokens.append(current)
        
        # Usuń puste tokeny
        tokens = [t for t in tokens if t]
        
        return tokens
    
    def calculate_scientific(self, operation: str, value: float) -> float:
        """Oblicza funkcje naukowe"""
        if operation == 'sin':
            return math.sin(math.radians(value))
        elif operation == 'cos':
            return math.cos(math.radians(value))
        elif operation == 'tan':
            return math.tan(math.radians(value))
        elif operation == 'log':
            return math.log10(value)
        elif operation == 'ln':
            return math.log(value)
        elif operation == 'sqrt':
            return math.sqrt(value)
        elif operation == 'square':
            return value ** 2
        elif operation == 'cube':
            return value ** 3
        elif operation == 'reciprocal':
            return 1 / value
        elif operation == 'negate':
            return -value
        elif operation == 'percent':
            return value / 100
        else:
            raise ValueError(f"Nieznana operacja: {operation}")
