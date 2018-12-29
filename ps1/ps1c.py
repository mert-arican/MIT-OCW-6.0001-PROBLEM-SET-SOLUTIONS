#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 10:09:07 2018

@author: mertarican
"""

"""This program calculates the best saving rate using
bisection search for given values."""

annual_salary = float(input("Enter your annual Salary: "))

total_cost = 1000000

semi_annual_raise = 0.07

current_savings = 0.0

portion_down_payment = total_cost / 4.0

monthly_salary = annual_salary / 12.0

monthly_investment_return = 0.04 / 12.0

number_of_months = 0

low = 0

high = 10000

guess = (low + high) // 2

bisectionCount = 0

while number_of_months < 37 :
    """ Increase current_savings as needed also raise salary every 6 month
    and check after 36 months that whether guess is good enough or not. If not 
    change the upper or lower limit depend on the value of guess and initialize 
    all values that are have to be initialized. This is going to cause while loop
    to continue until it reaches a good enough guess.
    """
    current_savings += (current_savings * monthly_investment_return)
    current_savings += (monthly_salary * (guess / 10000))
    number_of_months += 1
    if number_of_months % 6 == 0:
        monthly_salary += (monthly_salary * semi_annual_raise)    
    if number_of_months == 36:
        if current_savings >= (portion_down_payment - 100) and current_savings <= (portion_down_payment + 100):
            print("YEAY\n" + "Steps in bisection search: " + str(bisectionCount) + "\nBest savings rate: " + str(guess / 10000))
        else:
            if current_savings > portion_down_payment:
                high = guess
            else:
                low = guess
            number_of_months = 0; monthly_salary = annual_salary / 12.0 ; current_savings = 0
            bisectionCount += 1; guess = (high + low) // 2


    
