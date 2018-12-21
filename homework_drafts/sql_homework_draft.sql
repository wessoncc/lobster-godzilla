-- 1a
USE Sakila;
SELECT first_name, last_name 
FROM actor;

-- 1b
SELECT CONCAT( UPPER(first_name), " ", UPPER(last_name) ) AS "Actor Name"
FROM actor;

-- 2a
SELECT actor_id, first_name, last_name
FROM actor
WHERE first_name = "JOE";

-- 2b
SELECT actor_id, first_name, last_name
FROM actor
WHERE last_name LIKE "%GEN%";

-- 2c
SELECT actor_id, last_name, first_name
FROM actor
WHERE last_name LIKE "%LI%"
ORDER BY last_name, first_name ASC;

-- 2d
SELECT country_id, country
FROM country
WHERE country IN ("Afghanistan", "Bangladesh", "China");

-- 3a
ALTER TABLE actor
ADD COLUMN description blob AFTER last_name;

-- 3b
ALTER TABLE actor
DROP COLUMN description;

-- 4a
SELECT last_name, COUNT(*)
FROM actor
GROUP BY last_name;

-- 4b
SELECT last_name, COUNT(*)
FROM actor
GROUP BY last_name
HAVING COUNT(*) >= 2;

-- 4c
SELECT actor_id, first_name, last_name
FROM actor
WHERE first_name = "GROUCHO" AND last_name = "WILLIAMS";
UPDATE actor
SET 
    first_name = "HARPO"
WHERE
    actor_id = 172;
SELECT actor_id, first_name, last_name
FROM actor
WHERE first_name = "HARPO" AND last_name = "WILLIAMS";

-- 4d
UPDATE actor
SET 
    first_name = "GROUCHO"
WHERE
    first_name = "HARPO";
    
-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
SHOW CREATE TABLE address;

-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
SELECT staff.first_name, staff.last_name, address.address
FROM staff INNER JOIN address ON staff.address_id = address.address_id;

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.
SELECT staff.first_name, staff.last_name, payment.staff_id, SUM(amount) 
FROM payment
INNER JOIN staff ON staff.staff_id = payment.staff_id
WHERE payment.payment_date BETWEEN '2005-08-01 00:00:01' AND '2005-08-31 23:59:59'
GROUP BY staff.staff_id;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.
SELECT film.film_id, film.title, COUNT(film_actor.actor_id)
FROM film
INNER JOIN film_actor ON film_actor.film_id = film.film_id
GROUP BY film.film_id;

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
SELECT film.film_id, film.title, COUNT(inventory.inventory_id)
FROM film
INNER JOIN inventory ON inventory.film_id = film.film_id
WHERE title = "Hunchback Impossible"
GROUP BY film.film_id;

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:
SELECT customer.customer_id, customer.first_name, customer.last_name, SUM(payment.amount) 
FROM customer
INNER JOIN payment ON payment.customer_id = customer.customer_id
GROUP BY customer.customer_id
ORDER BY customer.last_name ASC;

-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.


-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.


-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.
SELECT customer.customer_id, customer.first_name, customer.last_name, customer.email, address.address, city.city, country.country
FROM customer
	LEFT JOIN address 
		ON address.address_id = customer.address_id
	LEFT JOIN city
		ON city.city_id = address.city_id
	LEFT JOIN country
		ON country.country_id = city.country_id
WHERE country.country = "Canada";

-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as family films.
SELECT film.film_id, film.title, category.name
FROM film
	LEFT JOIN film_category
		ON film.film_id = film_category.film_id
	LEFT JOIN category
		ON film_category.category_id = category.category_id
WHERE category.name = "Family";

-- 7e. Display the most frequently rented movies in descending order.


-- 7f. Write a query to display how much business, in dollars, each store brought in.


-- 7g. Write a query to display for each store its store ID, city, and country.


-- 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)


-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.


-- 8b. How would you display the view that you created in 8a?


-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.

