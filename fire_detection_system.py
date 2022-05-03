"""
FUZZY LOGIC ASSIGNMENT PART 2.2 Implementation

"""

# Install libraries (if needed, uncomment, line below)
# pip install numpy, matplotlib

import numpy as np
import matplotlib.pyplot as plt
import warnings


warnings.filterwarnings("error")

""" 
Membership class to easily define membership functions for use.
Returns:
    self [Object]: where self has both accessible x and y values 
"""
class membership:
    
    def __init__(self, *args, **kwargs):
        try:
            self.x = np.linspace(args[0], args[1], args[2])
            self.y = np.zeros_like(self.x)
        except:
            self.x = np.array([kwargs.get('x_input')]).astype('float')
            self.y = np.zeros_like(self.x)
    
    def increasing(self, a, b):
        for i in range(len(self.x)):
            if self.x[i] <= a:
                self.y[i] = 0
            elif self.x[i] >= b:
                self.y[i] = 1
            else:
                self.y[i] = (self.x[i]-a)/(b-a)
        return self
    
    def decreasing(self, a, b):
        self.y = 1-self.increasing(a, b).y
        return self
    
    def trapezoid(self, a, b, c, d):
        for i in range(len(self.x)):
            if self.x[i] < a:
                self.y[i] = 0
            elif self.x[i] > d:
                self.y[i] = 0    
            elif self.x[i] >= a and self.x[i] <= b:
                self.y[i] = (self.x[i]-a)/(b-a)
            elif self.x[i] >= b and self.x[i] <= c:
                self.y[i] = 1
            elif self.x[i] >= c and self.x[i] <= d:
                self.y[i] = (d-self.x[i])/(d-c)
        return self
    
    def gaussian(self, mu, sig):
        self.y = np.exp(-(self.x-mu)**2/(2*sig**2))
        return self
    
    def sigmoid(self, a, b):
        self.y = 1/(1+np.exp(-a*(self.x-b)))
        return self

"""
Membership functions defined globally
"""
# Temperature Membership function
# LOW: 0-40 MID: 28-55 HIGH: 50-100
temp = {'min': 0, 'max': 100, 'low': (24, 40),  'mid': (28, 38, 45, 55),  'hi' : (50, 60)}

temp_low = membership(temp['min'], temp['max'], 1000).decreasing(temp['low'][0], temp['low'][1])
temp_mid = membership(temp['min'], temp['max'], 1000).trapezoid(temp['mid'][0], temp['mid'][1], temp['mid'][2], temp['mid'][3])
temp_hi  = membership(temp['min'], temp['max'], 1000).increasing(temp['hi'][0], temp['hi'][1])

# Smoke Membership function
# LOW: 0-500 MID: 250-750 HIGH: 500-1000
smoke = {'min': 0, 'max': 1000, 'low': (250, 500), 'mid': (250, 500, 500, 750), 'hi' : (500, 750)}

smoke_low = membership(smoke['min'], smoke['max'], 1000).decreasing(smoke['low'][0], smoke['low'][1])
smoke_mid = membership(smoke['min'], smoke['max'], 1000).trapezoid(smoke['mid'][0], smoke['mid'][1], smoke['mid'][2], smoke['mid'][3])
smoke_hi  = membership(smoke['min'], smoke['max'], 1000).increasing(smoke['hi'][0], smoke['hi'][1])

# Humidity Membership function
# LOW: 0-80 HIGH: 70-100
humid = {'min': 0, 'max': 100, 'low': (70, 80), 'hi' : (70, 80)}

humid_low = membership(humid['min'], humid['max'], 1000).decreasing(humid['low'][0], humid['low'][1])
humid_hi  = membership(humid['min'], humid['max'], 1000).increasing(humid['hi'][0], humid['hi'][1])

# CO Membership function
# LOW: 0-50 MID: 40-110 HIGH: 100-150
CO = {'min': 0, 'max': 150, 'low': (40, 50), 'mid': (40, 50, 100, 110), 'hi' : (100, 110)}

CO_low = membership(CO['min'], CO['max'], 1000).decreasing(CO['low'][0], CO['low'][1])
CO_mid = membership(CO['min'], CO['max'], 1000).trapezoid(CO['mid'][0], CO['mid'][1], CO['mid'][2], CO['mid'][3])
CO_hi  = membership(CO['min'], CO['max'], 1000).increasing(CO['hi'][0], CO['hi'][1])

# Fire risk Membership function
# LOW: 0-40 MID: 30-70 HIGH: 60-100
fire = {'min': 0, 'max': 100, 'low': (-0.25, 25), 'mid': (50, 10), 'hi' : (0.25, 75)}
fire_low = membership(fire['min'], fire['max'], 1000).sigmoid(fire['low'][0], fire['low'][1])
fire_mid = membership(fire['min'], fire['max'], 1000).gaussian(fire['mid'][0], fire['mid'][1])
fire_hi  = membership(fire['min'], fire['max'], 1000).sigmoid(fire['hi'][0], fire['hi'][1])


"""
Function to generate rules given input values: temperature, smoke, humidity, CO
Returns:
    comp: dictionary object of all membership functions
"""
def evaluate_rules(input_temp, input_smoke, input_humid, input_co):
    
    comp = dict()
    comp["temp_input_low"] = membership(x_input=input_temp).decreasing(temp['low'][0], temp['low'][1]).y
    comp["temp_input_mid"] = membership(x_input=input_temp).trapezoid(temp['mid'][0], temp['mid'][1], temp['mid'][2], temp['mid'][3]).y
    comp["temp_input_hi"] = membership(x_input=input_temp).increasing(temp['hi'][0], temp['hi'][1]).y
    
    comp["smoke_input_low"] = membership(x_input=input_smoke).decreasing(smoke['low'][0], smoke['low'][1]).y
    comp["smoke_input_mid"] = membership(x_input=input_smoke).trapezoid(smoke['mid'][0], smoke['mid'][1], smoke['mid'][2], smoke['mid'][3]).y
    comp["smoke_input_hi"] = membership(x_input=input_smoke).increasing(smoke['hi'][0], smoke['hi'][1]).y
    
    comp["humid_input_low"] = membership(x_input=input_humid).decreasing(humid['low'][0], humid['low'][1]).y
    comp["humid_input_hi"]  = membership(x_input=input_humid).increasing(humid['hi'][0], humid['hi'][1]).y
    
    comp["CO_input_low"] = membership(x_input=input_co).decreasing(CO['low'][0], CO['low'][1]).y
    comp["CO_input_mid"] = membership(x_input=input_co).trapezoid(CO['mid'][0], CO['mid'][1], CO['mid'][2], CO['mid'][3]).y
    comp["CO_input_hi"]  = membership(x_input=input_co).increasing(CO['hi'][0], CO['hi'][1]).y
        
    return comp


"""
Define 12 rules for Fire Detection System
min: AND
fmin: composition operation
Return 
    All 12 rules
"""
def rules_composition(user_input_temp, user_input_smoke, user_input_humid, user_input_co):
    # Rule 1: If Temperature is LOW and Smoke is LOW and Humidity is HIGH and CO is LOW, *then* Presence of Fire is LOW  
    R1 = evaluate_rules(user_input_temp, user_input_smoke, user_input_humid, user_input_co)
    R1 = min(R1["temp_input_low"], min(R1["smoke_input_low"], min(R1["humid_input_hi"], R1["CO_input_low"])))
    R1 = np.fmin(fire_low.y, R1)

    # Rule 2: If Temperature is LOW and Smoke is HIGH and Humidity is HIGH and CO is MID, *then* Presence of Fire is LOW  
    R2 = evaluate_rules(user_input_temp, user_input_smoke, user_input_humid, user_input_co)
    R2 = min(R2["temp_input_low"], min(R2["smoke_input_mid"], min(R2["humid_input_hi"], R2["CO_input_mid"])))
    R2 = np.fmin(fire_low.y, R2)

    # Rule 3: If Temperature is HIGH and Smoke is LOW and Humidity is HIGH and CO is LOW, *then* Presence of Fire is LOW  
    R3 = evaluate_rules(user_input_temp, user_input_smoke, user_input_humid, user_input_co)
    R3 = min(R3["temp_input_hi"], min(R3["smoke_input_low"], min(R3["humid_input_hi"], R3["CO_input_low"])))
    R3 = np.fmin(fire_low.y, R3)

    # Rule 4: If Temperature is LOW and Smoke is LOW and Humidity is LOW and CO is LOW, *then* Presence of Fire is LOW  
    R4 = evaluate_rules(user_input_temp, user_input_smoke, user_input_humid, user_input_co)
    R4 = min(R4["temp_input_low"], min(R4["smoke_input_low"], min(R4["humid_input_low"], R4["CO_input_low"])))
    R4 = np.fmin(fire_low.y, R4)

    # Rule 5: If Temperature is LOW and Smoke is LOW and Humidity is HIGH and CO is HIGH, *then* Presence of Fire is LOW  
    R5 = evaluate_rules(user_input_temp, user_input_smoke, user_input_humid, user_input_co)
    R5 = min(R5["temp_input_low"], min(R5["smoke_input_low"], min(R5["humid_input_hi"], R5["CO_input_hi"])))
    R5 = np.fmin(fire_low.y, R5)

    # Rule 6: If Temperature is MID and Smoke is MID and Humidity is LOW and CO is MID, *then* Presence of Fire is MID  
    R6 = evaluate_rules(user_input_temp, user_input_smoke, user_input_humid, user_input_co)
    R6 = min(R6["temp_input_mid"], min(R6["smoke_input_mid"], min(R6["humid_input_low"], R6["CO_input_mid"])))
    R6 = np.fmin(fire_mid.y, R6)

    # Rule 7: If Temperature is LOW and Smoke is HIGH and Humidity is HIGH and CO is HIGH, *then* Presence of Fire is MID  
    R7 = evaluate_rules(user_input_temp, user_input_smoke, user_input_humid, user_input_co)
    R7 = min(R7["temp_input_low"], min(R7["smoke_input_hi"], min(R7["humid_input_hi"], R7["CO_input_hi"])))
    R7 = np.fmin(fire_mid.y, R7)

    # Rule 8: If Temperature is LOW and Smoke is HIGH and Humidity is LOW and CO is HIGH, *then* Presence of Fire is HIGH  
    R8 = evaluate_rules(user_input_temp, user_input_smoke, user_input_humid, user_input_co)
    R8 = min(R8["temp_input_low"], min(R8["smoke_input_hi"], min(R8["humid_input_low"], R8["CO_input_hi"])))
    R8 = np.fmin(fire_hi.y, R8)

    # Rule 9: If Temperature is HIGH and Smoke is LOW and Humidity is LOW and CO is HIGH, *then* Presence of Fire is HIGH  
    R9 = evaluate_rules(user_input_temp, user_input_smoke, user_input_humid, user_input_co)
    R9 = min(R9["temp_input_hi"], min(R9["smoke_input_low"], min(R9["humid_input_low"], R9["CO_input_hi"])))
    R9 = np.fmin(fire_hi.y, R9)

    # Rule 10: If Temperature is HIGH and Smoke is HIGH and Humidity is HIGH and CO is HIGH, *then* Presence of Fire is HIGH  
    R10 = evaluate_rules(user_input_temp, user_input_smoke, user_input_humid, user_input_co)
    R10 = min(R10["temp_input_hi"], min(R10["smoke_input_hi"], min(R10["humid_input_hi"], R10["CO_input_hi"])))
    R10 = np.fmin(fire_hi.y, R10)

    # Rule 11: If Temperature is HIGH and Smoke is HIGH and Humidity is LOW and CO is LOW, *then* Presence of Fire is HIGH  
    R11 = evaluate_rules(user_input_temp, user_input_smoke, user_input_humid, user_input_co)
    R11 = min(R11["temp_input_hi"], min(R11["smoke_input_hi"], min(R11["humid_input_low"], R11["CO_input_low"])))
    R11 = np.fmin(fire_hi.y, R11)

    # Rule 12: If Temperature is HIGH and Smoke is HIGH and Humidity is LOW and CO is HIGH, *then* Presence of Fire is HIGH  
    R12 = evaluate_rules(user_input_temp, user_input_smoke, user_input_humid, user_input_co)
    R12 = min(R12["temp_input_hi"], min(R12["smoke_input_hi"], min(R12["humid_input_low"], R12["CO_input_hi"])))
    R12 = np.fmin(fire_hi.y, R12)

    return R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12

"""
Prompts user to enter input values
Returns:
    self [Object]: where self has both accessible x and y values 
"""
def userinput():
    cont = 0
    user_input = dict()
    
    while cont != 1:
        while True:
            try:
                user_input_temp = float(input("Enter temperature: "))
                if user_input_temp < 0:
                    print("Temperature must be 0 or greater, try again.")
                    continue
                elif user_input_temp > 100:
                    print("Temperature must be 100 or lower, try again.")
                    continue
                user_input["temp"] = user_input_temp
                break
            except ValueError:
                print("Input must be a float, try again.")
        while True:
            try:
                user_input_smoke = float(input("Enter smoke level: "))
                if user_input_smoke < 0:
                    print("Smoke level must be 0 or greater, try again.")
                    continue
                elif user_input_smoke > 1000:
                    print("Smoke level must be 1000 or lower, try again")
                    continue
                user_input["smoke"] = user_input_smoke
                break
            except ValueError:
                print("Input must be a float, try again.")
        while True:
            try:
                user_input_humid = float(input("Enter humidity: "))
                if 100 >= user_input_humid < 0:
                    print("Humidity must be greater than 0%, try again.")
                    continue
                elif user_input_humid > 100:
                    print("Humidity must be 100 or lower, try again.")
                    continue
                user_input["humid"] = user_input_humid
                break
            except ValueError:
                print("Input must be a float, try again.")
        while True:
            try:
                user_input_co = float(input("Enter CO level: "))
                if 150 >= user_input_co < 0:
                    print("CO level must be greater than 0, try again.")
                    continue
                elif user_input_co > 150:
                    print("CO input must be 150 or lower, try again.")
                    continue
                user_input["co"] = user_input_co
                break
            except ValueError:
                print("Input must be a float, try again.")
        return user_input
      

"""
Generate plots: input membership functions, output fire risk membership

"""
def generate_plots(R, user_input):
    temp_input_low = membership(x_input=user_input["temp"]).decreasing(temp['low'][0], temp['low'][1])
    temp_input_mid = membership(x_input=user_input["temp"]).trapezoid(temp['mid'][0], temp['mid'][1], temp['mid'][2], temp['mid'][3])
    temp_input_hi  = membership(x_input=user_input["temp"]).increasing(temp['hi'][0], temp['hi'][1])
    
    smoke_input_low = membership(x_input=user_input["smoke"]).decreasing(smoke['low'][0], smoke['low'][1])
    smoke_input_mid = membership(x_input=user_input["smoke"]).trapezoid(smoke['mid'][0], smoke['mid'][1], smoke['mid'][2], smoke['mid'][3])
    smoke_input_hi  = membership(x_input=user_input["smoke"]).increasing(smoke['hi'][0], smoke['hi'][1])

    humid_input_low = membership(x_input=user_input["humid"]).decreasing(humid['low'][0], humid['low'][1])
    humid_input_hi  = membership(x_input=user_input["humid"]).increasing(humid['hi'][0], humid['hi'][1])

    CO_input_low = membership(x_input=user_input["co"]).decreasing(CO['low'][0], CO['low'][1])
    CO_input_mid = membership(x_input=user_input["co"]).trapezoid(CO['mid'][0], CO['mid'][1], CO['mid'][2], CO['mid'][3])
    CO_input_hi  = membership(x_input=user_input["co"]).increasing(CO['hi'][0], CO['hi'][1])
    
    plt.figure(figsize=(20, 10), dpi=100)

    plt.subplot(241)
    plt.title('Input 1 - Temperature (°C)')
    plt.plot(temp_low.x, temp_low.y,label="Low")
    plt.plot(temp_mid.x, temp_mid.y, label="Mid")
    plt.plot(temp_hi.x, temp_hi.y, label="High")
    plt.scatter(temp_input_low.x, temp_input_low.y)
    plt.scatter(temp_input_mid.x, temp_input_mid.y)
    plt.scatter(temp_input_hi.x, temp_input_hi.y)
    plt.legend()

    plt.subplot(242)
    plt.title('Input 2 - Smoke (ppm)')
    plt.plot(smoke_low.x, smoke_low.y, label="Low")
    plt.plot(smoke_mid.x, smoke_mid.y, label="Mid")
    plt.plot(smoke_hi.x, smoke_hi.y, label="High")
    plt.scatter(smoke_input_low.x, smoke_input_low.y)
    plt.scatter(smoke_input_mid.x, smoke_input_mid.y)
    plt.scatter(smoke_input_hi.x, smoke_input_hi.y)
    plt.legend()

    plt.subplot(243)
    plt.title('Input 3 - Humidity (%)')
    plt.plot(humid_low.x, humid_low.y, label="Low")
    plt.plot(humid_hi.x, humid_hi.y, label="High")
    plt.scatter(humid_input_low.x, humid_input_low.y)
    plt.scatter(humid_input_hi.x, humid_input_hi.y)
    plt.legend()

    plt.subplot(244)
    plt.title('Input 4 - CO (ppm)')
    plt.plot(CO_low.x, CO_low.y, label="Low")
    plt.plot(CO_mid.x, CO_mid.y, label="Mid")
    plt.plot(CO_hi.x, CO_hi.y, label="High")
    plt.scatter(CO_input_low.x, CO_input_low.y)
    plt.scatter(CO_input_mid.x, CO_input_mid.y)
    plt.scatter(CO_input_hi.x, CO_input_hi.y)
    plt.legend()

    plt.subplot(212)
    plt.title('Output - Fire Risk (%)')
    plt.plot(fire_low.x, fire_low.y, label="Low")
    plt.plot(fire_mid.x, fire_mid.y, label="Mid")
    plt.plot(fire_hi.x, fire_hi.y, label="High")
    plt.fill_between(np.linspace(0,100,1000), R, alpha=0.5, color='gray')
    plt.legend()
    

if __name__ == "__main__":
    valid_input = True
   
    
    while valid_input:
        print("-----------------------------------------------------")
        print("WELCOME TO THE FUZZY LOGIC FIRE DETECTION SYSTEM\n\n")
        user_input = userinput()

        R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12 = rules_composition(user_input["temp"], user_input["smoke"], user_input["humid"], user_input["co"])
        R = np.maximum(R1, np.maximum(R2, np.maximum(R3, np.maximum(R4, np.maximum(R5, np.maximum(R6, np.maximum(R7, np.maximum(R8, np.maximum(R9, np.maximum(R10, np.maximum(R11, R12)))))))))))
 
        try:
            centroid = np.trapz(R*(np.linspace(0,100,1000)))/np.trapz(R)
            print("Centroid value is :", centroid, "\n")
            valid_input = False            
        except RuntimeWarning:
            print("Sensor value ambiguous. Please try again.")
            valid_input = True
            
    generate_plots(R, user_input)   
    plt.show() #display plots!

    print("\n Exiting.... ", "\n")
    print("-----------------------------------------------------")