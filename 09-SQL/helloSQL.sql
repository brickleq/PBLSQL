/* # Homework Assignment

## Installation Instructions

* Refer to the [installation guide](Installation.md) to install the necessary files.

## Instructions */

USE sakila;

/* 1a. Display the first and last names of all actors from the table `actor`. */
SELECT first_name, last_name
FROM actor;

/*1b. Display the first and last name of each actor in a single column in upper case 
letters. Name the column `Actor Name`.*/
SELECT CONCAT(first_name,' ',last_name) AS 'Actor Name'
FROM actor;

/*2a. You need to find the ID number, first name, and last name of an actor, of whom 
you know only the first name, "Joe." What is one query would you use to obtain this 
information?*/
SELECT actor_id, first_name, last_name
FROM actor
WHERE first_name = 'JOE';

/*2b. Find all actors whose last name contain the letters `GEN`:*/
SELECT * FROM actor
WHERE last_name 
LIKE '%GEN%';

/*2c. Find all actors whose last names contain the letters `LI`. This time, order the 
rows by last name and first name, in that order:*/
SELECT * FROM actor
WHERE last_name 
LIKE '%LI%'
ORDER BY last_name, first_name ASC;

/*2d. Using `IN`, display the `country_id` and `country` columns of the following countries: 
Afghanistan, Bangladesh, and China:*/
SELECT country, country_id
FROM country
WHERE country
IN ('Afghanistan','Bangladesh','China');

/*3a. You want to keep a description of each actor. You don't think you will be performing 
queries on a description, so create a column in the table `actor` named `description` and 
use the data type `BLOB` (Make sure to research the type `BLOB`, as the difference between 
it and `VARCHAR` are significant).*/
ALTER TABLE actor
ADD description BLOB;

/* 3b. Very quickly you realize that entering descriptions for each actor is too much effort. 
Delete the `description` column.*/
ALTER TABLE actor
DROP description;

/* 4a. List the last names of actors, as well as how many actors have that last name.*/
SELECT DISTINCT last_name,
COUNT(last_name) as 'total'
FROM actor
GROUP BY last_name DESC
ORDER BY total DESC;

/* 4b. List last names of actors and the number of actors who have that last name, but only 
for names that are shared by at least two actors*/
SELECT DISTINCT last_name,
COUNT(last_name) as 'total'
FROM actor
GROUP BY last_name
HAVING total >= 2
ORDER BY total DESC;

/* 4c. The actor `HARPO WILLIAMS` was accidentally entered in the `actor` table as `GROUCHO WILLIAMS`. Write a query to fix the record.*/
UPDATE actor
SET first_name = 'HARPO'
WHERE first_name = 'GROUCHO' AND last_name = 'WILLIAMS';

/* 4d. Perhaps we were too hasty in changing `GROUCHO` to `HARPO`. It turns out that `GROUCHO` was the correct name after all! In a single query,
 if the first name of the actor is currently `HARPO`, change it to `GROUCHO`.*/
 UPDATE actor
 SET first_name = 'GROUCHO'
 WHERE first_name = 'HARPO';
 
/* 5a. You cannot locate the schema of the `address` table. Which query would you use to re-create it?
  * Hint: [https://dev.mysql.com/doc/refman/5.7/en/show-create-table.html](https://dev.mysql.com/doc/refman/5.7/en/show-create-table.html)*/
SHOW CREATE TABLE address;

/* Returns: 'address', 'CREATE TABLE `address` (\n  `address_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,\n  `address` varchar(50) NOT NULL,\n  `address2` varchar(50) DEFAULT NULL,\n  `district` varchar(20) NOT NULL,\n  `city_id` smallint(5) unsigned NOT NULL,\n  `postal_code` varchar(10) DEFAULT NULL,\n  `phone` varchar(20) NOT NULL,\n  `location` geometry NOT NULL,\n  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n  PRIMARY KEY (`address_id`),\n  KEY `idx_fk_city_id` (`city_id`),\n  SPATIAL KEY `idx_location` (`location`),\n  CONSTRAINT `fk_address_city` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`) ON UPDATE CASCADE\n) ENGINE=InnoDB AUTO_INCREMENT=606 DEFAULT CHARSET=utf8'*/
CREATE TABLE IF NOT EXISTS address(
address_id smallint(5) unsigned NOT NULL AUTO_INCREMENT,
address varchar(50) NOT NULL,
address2 varchar(50) DEFAULT NULL,
district varchar(20) NOT NULL,
city_id smallint(5) unsigned NOT NULL,
postal_code varchar(10) DEFAULT NULL,
phone varchar(20) NOT NULL,
location geometry NOT NULL,
last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (address_id),
KEY idx_fk_city_id (city_id),
SPATIAL KEY idx_location (location),
CONSTRAINT fk_address_city
FOREIGN KEY (city_id)
REFERENCES city (city_id)
ON UPDATE CASCADE) 
ENGINE=InnoDB AUTO_INCREMENT=606 
DEFAULT CHARSET=utf8;

/* 6a. Use `JOIN` to display the first and last names, as well as the address, of each staff member. Use the tables `staff` and `address`:*/
SELECT staff.first_name,staff.last_name,address.address_id,address.address,address.address2
FROM staff
JOIN address
ON staff.address_id = address.address_id;

/* 6b. Use `JOIN` to display the total amount rung up by each staff member in August of 2005. Use tables `staff` and `payment`.*/
SELECT staff.staff_id, SUM(payment.amount)
FROM staff
LEFT JOIN payment
ON staff.staff_id = payment.staff_id
WHERE payment.payment_date LIKE '2005-08%'
GROUP BY staff.staff_id;

/* 6c. List each film and the number of actors who are listed for that film. Use tables `film_actor` and `film`. Use inner join.*/
SELECT film.title, count(*) as 'Actor Count'
FROM film
JOIN film_actor
ON film.film_id = film_actor.film_id
GROUP BY film.film_id
ORDER BY count(*) DESC;

/* 6d. How many copies of the film `Hunchback Impossible` exist in the inventory system?*/
SELECT COUNT(inventory.film_id) as 'Copies of "Hunchback Impossible"'
FROM inventory
WHERE inventory.film_id = (SELECT film_id
FROM film
WHERE film.title = 'Hunchback Impossible');

/* 6e. Using the tables `payment` and `customer` and the `JOIN` command, list the total paid 
by each customer. List the customers alphabetically by last name:

  ![Total amount paid](Images/total_payment.png)*/
SELECT payment.customer_id, SUM(payment.amount), customer.last_name, customer.first_name
FROM payment
LEFT JOIN customer
ON payment.customer_id = customer.customer_id
GROUP BY customer_id
ORDER BY last_name;

/* 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an 
unintended consequence, films starting with the letters `K` and `Q` have also soared in 
popularity. Use subqueries to display the titles of movies starting with the letters `K` 
and `Q` whose language is English.*/
SELECT film.title
FROM film
WHERE film.language_id = 
(SELECT language.language_id FROM language WHERE language.name = 'English')
AND film.title LIKE 'K%'
OR film.title LIKE 'Q%';

/* 7b. Use subqueries to display all actors who appear in the film `Alone Trip`.*/
SELECT actor.first_name, actor.last_name
FROM actor
WHERE actor.actor_id IN
(SELECT film_actor.actor_id FROM film_actor WHERE film_actor.film_id =
(SELECT film.film_id from film WHERE film.title = 'Alone Trip'));

/* 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all 
Canadian customers. Use joins to retrieve this information.*/
DROP TABLE IF EXISTS canadians;
CREATE TABLE IF NOT EXISTS canadians(
canuck_id SMALLINT(5) NOT NULL AUTO_INCREMENT,
customer_id INT,
first_name VARCHAR(50),
last_name VARCHAR(50),
email VARCHAR(50),
PRIMARY KEY (canuck_id));

INSERT INTO canadians (customer_id)
SELECT customer.customer_id from customer;

SELECT customer.first_name, customer.last_name, customer.customer_id, customer.email
FROM customer
RIGHT JOIN canadians
ON customer.customer_id = canadians.customer_id
WHERE customer.address_id IN
(SELECT address.address_id FROM address WHERE address.city_id IN
(SELECT city.city_id FROM city WHERE city.country_id =
(SELECT country.country_id FROM country WHERE country.country = 'Canada')));

/* 7d. Sales have been lagging among young families, and you wish to target all family movies 
for a promotion. Identify all movies categorized as _family_ films.*/
SELECT film.title
FROM film
WHERE film.film_id IN
(SELECT film_category.film_id FROM film_category WHERE film_category.category_id = 
(SELECT category.category_id FROM category WHERE category.name = 'Family'));

/* 7e. Display the most frequently rented movies in descending order.*/
SELECT film.title, COUNT(film.title) as 'Rentals'
FROM film, rental
WHERE film.film_id IN
(SELECT inventory.film_id FROM inventory WHERE inventory.inventory_id = 
(SELECT rental.inventory_id))
GROUP BY film.title
ORDER BY COUNT(film.title) DESC;

/* 7f. Write a query to display how much business, in dollars, each store brought in.*/
SELECT store.store_id, SUM(payment.amount)
FROM store, payment
WHERE payment.staff_id =
(SELECT staff.staff_id FROM staff WHERE staff.store_id = store.store_id)
GROUP BY store.store_id;

/* 7g. Write a query to display for each store its store ID, city, and country.*/
SELECT store.store_id, city.city, country.country
FROM store
LEFT JOIN address ON store.address_id = address.address_id
LEFT JOIN city ON address.city_id = city.city_id
LEFT JOIN country on city.country_id = country.country_id;

/* 7h. List the top five genres in gross revenue in descending order. (**Hint**: you may need to use the following tables: category, 
film_category, inventory, payment, and rental.)*/
SELECT category.name, SUM(payment.amount)
FROM category
LEFT JOIN film_category ON category.category_id = film_category.category_id
LEFT JOIN inventory ON film_category.film_id = inventory.film_id
LEFT JOIN rental ON inventory.inventory_id = rental.inventory_id
LEFT JOIN payment on rental.rental_id = payment.rental_id
GROUP BY category.name
ORDER BY SUM(payment.amount) DESC
LIMIT 5;

/* 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. 
Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.*/
CREATE VIEW top_five_genres AS
SELECT category.name, SUM(payment.amount)
FROM category
LEFT JOIN film_category ON category.category_id = film_category.category_id
LEFT JOIN inventory ON film_category.film_id = inventory.film_id
LEFT JOIN rental ON inventory.inventory_id = rental.inventory_id
LEFT JOIN payment on rental.rental_id = payment.rental_id
GROUP BY category.name
ORDER BY SUM(payment.amount) DESC
LIMIT 5;
/* 8b. How would you display the view that you created in 8a?*/
SELECT * FROM top_five_genres;

/* 8c. You find that you no longer need the view `top_five_genres`. Write a query to delete it.*/
DROP VIEW top_five_genres;

/*## Appendix: List of Tables in the Sakila DB

* A schema is also available as `sakila_schema.svg`. Open it with a browser to view.

```sql
'actor'
'actor_info'
'address'
'category'
'city'
'country'
'customer'
'customer_list'
'film'
'film_actor'
'film_category'
'film_list'
'film_text'
'inventory'
'language'
'nicer_but_slower_film_list'
'payment'
'rental'
'sales_by_film_category'
'sales_by_store'
'staff'
'staff_list'
'store'
```

## Uploading Homework

* To submit this homework using BootCampSpot:

  * Create a GitHub repository.
  * Upload your .sql file with the completed queries.
  * Submit a link to your GitHub repo through BootCampSpot.
  
  
  */
