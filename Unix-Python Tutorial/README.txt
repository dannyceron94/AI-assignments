Name:
	Danny Ceron Garcia 918581149

Description:
   Q1:
      In question 1, there was really no much thinking, the code was very simple.
      We just had to copy paste the given code.
   Q2:
      in question 2, we had to return the total price of the order list, so i had to create a
      variable that could hold summation of total cost for all the items in the order list.
      in oder to get the price of that an item, we would have look up the item in the fruitPrices  
      dictionary, since in the loop we can get the name and quantity of the items the system wishes to buy.
      in one line we can obtain the items quantity total cost and add it to the total cost of the order list

   Q3:
      question 3 was very similar to question two, so code was very similar.
      the only difference is that we had to deal with shop instances which contain the prices of each item.
      the most simple but not efficient way to do this was to use nested loop
      1st loop iterates through each stores instance, the second loop does the shopping,
      like in Q2, in each loop iteration the program calculates and stores the item quantity
      total cost.
      
      because we want the store with the cheapest total cost, we want the program to
      keep track of the total cost of the order list for each store.
      once program calculates the total cost of the order list in each store instance
      it will compare the preveous store total cost with the current store total cost
      and it will keep track the store with the cheapest total cost.