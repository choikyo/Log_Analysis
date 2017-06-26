# Log Analysis Reports
This program provides a web UI to represents reports based on "news" database provided by Udacity.
The reports answers three questions: 
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors? 

### Installation
1. Setup vagrant and bring up vagrant 
    ```sh
    vagrant up
    ```
    
2. Make sure PostgreSQL is installed, and news database has correct tables and data.
    ```sh
    psql -d news
    \dt
    \q
    ```
    You should be able to see 3 tables: articles, authors and log
    
3. Place report.py and reportdb.py in the same directory under the vagrant path. Then run report.py in the console to bring up the server:
    ```sh
    python report.py
    ```
    The default port is 8000. 
    If your 8000 port is busy, then edit report.py, and find line: 
    `app.run(host='0.0.0.0', port=8000)`
    You can change the port to 8080 or 5000. 

4. Open your browser, and type:
    `http://localhost:8000/`
    Now you should be able to see a web-based UI with a dropdown list to select reports

### Reporting Queries
The reporting queries are located in reportdb.py. 

#### Most Popular Article Query
    SELECT a.title, count(1) as views
    FROM public.log l, public.articles a  
    WHERE position(a.slug in l.path)>0
    GROUP BY a.title 
    ORDER BY views DESC
    LIMIT 3
        
#### Most Popular Author Query
    SELECT ath.name, count(1) as views
    FROM public.log l, public.articles a , public.authors ath
    WHERE a.author=ath.id
    AND position(a.slug in l.path)>0
    GROUP BY ath.name 
    ORDER BY views DESC
        
#### Error Request Query (threshold 1%)
    SELECT  v2.error_views, 
			v1.total_views, 
			cast( v2.error_views as decimal)/ v1.total_views as error_rate ,
            v1.dates
    FROM
			(SELECT count(1) AS total_views,  date_trunc('day',time) as dates
			FROM public.log
			GROUP BY date_trunc('day',time)
			) v1, 
			(SELECT count(1) as error_views,  date_trunc('day',time) as dates, status
			FROM public.log 
			WHERE status not like '%OK%'
			GROUP BY date_trunc('day',time), status
			)  v2
	WHERE v1.dates=v2.dates
	AND cast( v2.error_views as decimal)/ v1.total_views>0.01

### Reporting Data

#### Most Popular Article Report
Article Title|Views
-------------|-----
Candidate is jerk, alleges rival|342102
Bears love berries, alleges bear|256365
Bad things gone, say good people|171762

#### Most Popular Author Report
Author Name|Views
-----------|------
Ursula La Multa|512805
Rudolf von Treppenwitz|427781
Anonymous Contributor|171762
Markoff Chaney|85387

#### Error Request Report (threshold 1%)
Error Requests|	Total Requests|	Error Request Rate|	Date
--------|-------|------------|------
1265	|55907	|0.02262686246802725956	|2016-07-17 00:00:00+00:00
