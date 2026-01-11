
USE kola_data;
SHOW TABLES;

--  Data Analyst – SQL Questions & Queries
-- 0. Retrieve all columns from the bookings table
DESC bookings;

-- 1. Retrieve all successful bookings
SELECT *
FROM bookings
WHERE Booking_Status = 'Successfull';

-- 2. Count the total number of successful bookings
SELECT COUNT(*) AS total_number_of_successful_booking
FROM bookings
WHERE Booking_Status = 'Successfull';

-- 3. Find the average ride distance for each vehicle type
SELECT 
    Vehicle_Type,
    ROUND(AVG(Ride_Distance), 2) AS Average_Ride_Distance
FROM bookings
GROUP BY Vehicle_Type;

-- 4. Get the total number of rides cancelled by customers
SELECT COUNT(*) AS Total_Number_Of_Cancelled_Ride
FROM bookings
WHERE Booking_Status = 'Cancelled by Customer';

-- 5. List the top 5 customers who booked the highest number of rides
SELECT 
    Customer_ID,
    COUNT(*) AS Total_Number_Of_Rides
FROM bookings
GROUP BY Customer_ID
ORDER BY Total_Number_Of_Rides DESC
LIMIT 5;

-- 6. Get the number of rides cancelled by drivers due to personal and car-related issues
SELECT COUNT(*) AS Rides_Cancelled_By_Drivers_Due_To_Personal_And_Car_Related_Issues
FROM bookings
WHERE Booking_Status = 'Cancelled by Driver'
  AND Driver_Cancel_Reason = 'Personal & Car related issues';

-- 7. Find the maximum and minimum driver ratings for Prime Sedan bookings
SELECT 
    Vehicle_Type,
    MAX(Driver_Ratings) AS Maximum_Driver_Rating,
    MIN(Driver_Ratings) AS Minimum_Driver_Rating
FROM bookings
WHERE Vehicle_Type = 'Prime Sedan';

-- 8. Retrieve all rides where payment was made using UPI
SELECT 
    Customer_ID,
    Booking_ID,
    Payment_Method
FROM bookings
WHERE Payment_Method = 'UPI';

-- 9. Count how many customers paid using UPI
SELECT COUNT(*) AS Total_Count_Of_Customers_Paid_Using_UPI
FROM bookings
WHERE Payment_Method = 'UPI';

-- 10. Find the average customer rating for each vehicle type
SELECT 
    Vehicle_Type,
    ROUND(AVG(Customer_Rating), 2) AS Average_Customer_Rating
FROM bookings
GROUP BY Vehicle_Type;

-- 11. Calculate the total booking value of rides completed successfully
SELECT 
    SUM(Booking_Value) AS total_successful_booking_value
FROM bookings
WHERE Booking_Status = 'Successfull';

-- 12. List all incomplete rides along with their reasons
SELECT 
    Booking_ID,
    Incomplete_Rides_Reason
FROM bookings
WHERE Booking_Status = 'Incomplete';

-- Bonus / Advanced Analysis
-- 13. Calculate the percentage distribution of bookings by booking status
SELECT 
    Booking_Status,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM bookings), 2) AS Percentage
FROM bookings
GROUP BY Booking_Status;

-- 14. Compare total revenue generated on weekends vs weekdays
SELECT 
    CASE 
        WHEN DAYOFWEEK(`Date`) IN (1, 7) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    SUM(Booking_Value) AS Total_Revenue_Generated
FROM bookings
WHERE Booking_Status = 'Successfull'
GROUP BY day_type;

-- 15. Analyze total revenue by payment method for successful rides
SELECT 
    Payment_Method,
    SUM(Booking_Value) AS total_revenue_by_payment_method
FROM bookings
WHERE Booking_Status = 'Successfull'
GROUP BY Payment_Method;

-- 16. Find the average driver rating by vehicle type for completed rides
SELECT 
    Vehicle_Type,
    ROUND(AVG(Driver_Ratings), 2) AS Average_Driver_Rating
FROM bookings
WHERE Booking_Status = 'Successfull'
GROUP BY Vehicle_Type;

-- 17. Identify the most common reasons for driver cancellations
SELECT 
    Driver_Cancel_Reason,
    COUNT(*) AS occurrence_of_reason
FROM bookings
GROUP BY Driver_Cancel_Reason
ORDER BY occurrence_of_reason DESC;

-- 18. Identify the most common reasons for customer cancellations
SELECT 
    Reason_for_cancelling_by_Customer,
    COUNT(*) AS occurrence_of_reason
FROM bookings
GROUP BY Reason_for_cancelling_by_Customer
ORDER BY occurrence_of_reason DESC;

-- 19. Determine which vehicle type has the highest average ride distance
SELECT 
    Vehicle_Type,
    ROUND(AVG(Ride_Distance), 2) AS Average_Ride_Distance
FROM bookings
GROUP BY Vehicle_Type
ORDER BY Average_Ride_Distance DESC
LIMIT 1;

-- 20. Find customers with repeated cancellations (customer behavior risk analysis)
SELECT
    Customer_ID,
    COUNT(*) AS cancellation_count
FROM bookings
WHERE Cancelled_Rides_by_Customer = 1
GROUP BY Customer_ID
HAVING COUNT(*) > 1
ORDER BY cancellation_count DESC;

-- booking status percentages in
SELECT 
    booking_status,
    round(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM bookings),2) AS booking_status_Percentage
FROM bookings
GROUP BY booking_Status
order by booking_status_Percentage desc;

 -- total revenue calculated
 select 
	sum(booking_value) as total_Revenue
from 
	bookings;