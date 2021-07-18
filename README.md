**Order Distribution Logic**:

1. Group & Sort the orders by their slot numbers.

2. For each slot, sort the orders by their weight. Now, pick up the orders one by one:
    a. Deliver as many orders as you can on a single bike.
    b. After you're done delivering orders on Bike, start delivering the remaining on scooters, and then on truck.
    c. While doing steps a,b we keep in mind the limitations of availability of vehicles.

3. **API Endpoints exposed**:

    a. *"/"* -> adds some random orders & vehicles in database.
    
    b. *"/orders"* -> prints out all the current orders.
    
    c. *"/deliver"* -> delivers & returns the status of the orders using above logic.
