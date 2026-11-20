
USE ola_analytics;

-- 1. Retrieve all successful bookings
SELECT *
FROM bookings
WHERE booking_status = 'Success';

-- 2. Average ride distance for each vehicle type
SELECT
    vehicle_type,
    ROUND(AVG(ride_distance), 2) AS average_ride_distance
FROM bookings
WHERE booking_status = 'Success'
GROUP BY vehicle_type
ORDER BY average_ride_distance DESC;

-- 3. Count rides cancelled by customers
SELECT
    COUNT(*) AS customer_cancelled_rides
FROM bookings
WHERE booking_status = 'Canceled by Customer';

-- 4. Top 5 customers by number of rides
SELECT
    customer_id,
    COUNT(*) AS total_rides
FROM bookings
GROUP BY customer_id
ORDER BY total_rides DESC
LIMIT 5;

-- 5. Driver cancellations due to personal or car-related issues
SELECT
    COUNT(*) AS personal_car_related_cancellations
FROM bookings
WHERE booking_status = 'Canceled by Driver'
AND canceled_rides_by_driver = 'Personal & Car related issue';

-- 6. Maximum and minimum driver ratings for Prime Sedan
SELECT
    MAX(driver_ratings) AS maximum_driver_rating,
    MIN(driver_ratings) AS minimum_driver_rating
FROM bookings
WHERE vehicle_type = 'Prime Sedan'
AND booking_status = 'Success';

-- 7. All UPI bookings
SELECT *
FROM bookings
WHERE payment_method = 'UPI';

-- 8. Average customer rating for each vehicle type
SELECT
    vehicle_type,
    ROUND(AVG(customer_rating), 2) AS average_customer_rating
FROM bookings
WHERE booking_status = 'Success'
GROUP BY vehicle_type
ORDER BY average_customer_rating DESC;

-- 9. Total booking value of successful rides
SELECT
    SUM(booking_value) AS total_successful_booking_value
FROM bookings
WHERE booking_status = 'Success';

-- 10. Incomplete rides with their reasons
SELECT
    incomplete_rides_reason,
    COUNT(*) AS incomplete_ride_count
FROM bookings
WHERE booking_status = 'Success'
AND incomplete_rides = 'Yes'
GROUP BY incomplete_rides_reason
ORDER BY incomplete_ride_count DESC;