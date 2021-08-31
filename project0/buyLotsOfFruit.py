# buyLotsOfFruit.py
# -----------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
To run this script, type

  python buyLotsOfFruit.py
  
Once you have correctly implemented the buyLotsOfFruit function,
the script should produce the output:

Cost of [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)] is 12.25
"""

#This is a dictionary
fruitPrices = {'apples':2.00, 'oranges': 1.50, 'pears': 1.75,
              'limes':0.75, 'strawberries':1.00}

def buyLotsOfFruit(orderList):
    """
        orderList: List of (fruit, numPounds) tuples
            
    Returns cost of order
    """ 
    totalCost = 0.0             
    for i in range(0,len(orderList)-1):
        #If the fruit is in fruitPrices
        if(orderList[i][0]) in fruitPrices:
            #How to access the value in fruitPrices that matches the key orderList[i][1]??????????
            #totalCost = totalCost + (orderList[i][2]*fruitPrices[`orderList[i][1]`]
            if(orderList[i][0] == fruitPrices.keys()[0]):
                totalCost = totalCost + (orderList[i][1]*fruitPrices[fruitPrices.keys()[0]])
            elif(orderList[i][0] == fruitPrices.keys()[1]):
                totalCost = totalCost + (orderList[i][1]*fruitPrices[fruitPrices.keys()[1]])
            elif(orderList[i][0] == fruitPrices.keys()[2]):
                totalCost = totalCost + (orderList[i][1]*fruitPrices[fruitPrices.keys()[2]])
            elif(orderList[i][0] == fruitPrices.keys()[3]):
                totalCost = totalCost + (orderList[i][1]*fruitPrices[fruitPrices.keys()[3]])
            elif(orderList[i][0] == fruitPrices.keys()[4]):
                totalCost = totalCost + (orderList[i][1]*fruitPrices[fruitPrices.keys()[4]])
        #The fruit is not in our prices list
        else:
            print("You have entered a fruit that is not in our records.")
            return None
    
    return totalCost
    
# Main Method    
if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orderList = [ ('apples', 2.0), ('pears', 3.0), ('limes', 4.0) ]
    print ('Cost of', orderList, 'is', buyLotsOfFruit(orderList))