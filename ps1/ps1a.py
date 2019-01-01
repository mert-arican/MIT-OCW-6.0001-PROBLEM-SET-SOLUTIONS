#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 22:18:08 2018

@author: mertarican
"""

""" Calculates how many months it is going to take
 in order to pay for a down payment. """

annual_salary = float(input("Enter your annual salary: "))

portion_saved = float(input("Enter your saving rate: "))

total_cost = float(input("Enter your dream house's cost: "))

portion_down_payment = total_cost / 4.0

current_savings = 0.0

monthly_investment_return = 0.04 / 12.0

monthly_salary = annual_salary / 12.0

number_of_months = 0

while current_savings < portion_down_payment :
    current_savings += (current_savings * monthly_investment_return)
    current_savings += (monthly_salary * portion_saved)
    number_of_months += 1

print("Number of months:", str(number_of_months))

    
    

        






