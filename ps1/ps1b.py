#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 23:23:32 2018

@author: mertarican
"""

""" Calculates how many months it is going to take
 in order to pay for a down payment. Adds raise to the salary each six months."""
 
annual_salary = float(input("Enter your starting annual salary: "))

portion_saved = float(input("Enter the percent of yout salary to save, as a decimal: "))

total_cost = float(input("Enter the cost of yout dream home: "))

semi_annual_raise = float(input("Enter your semi-annual raise, as a decimal: "))

portion_down_payment = total_cost / 4.0

monthly_salary = annual_salary / 12.0

current_savings = 0.0

monthly_investment_return = 0.04 / 12.0

number_of_months = 0

while current_savings < portion_down_payment :
    current_savings += (current_savings * monthly_investment_return)
    current_savings += (monthly_salary * portion_saved)
    number_of_months += 1
    if number_of_months % 6 == 0:
        monthly_salary += (monthly_salary * semi_annual_raise)

print("Number of months:", str(number_of_months))
