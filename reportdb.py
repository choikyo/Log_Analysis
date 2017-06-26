# "Database code" for the DB Forum.
import psycopg2
import datetime

# 1 Popular Article Report
def get_popular_articles():
    """Return Popular Articles"""
    row_html = """
        <tr>
            <th>Article Title</th>
            <th>Views</th>
        </tr>    
"""
    # Connecting to news DB
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    # Report query
    query = """
        SELECT a.title, count(1) as views
        FROM public.log l, public.articles a  
        WHERE position(a.slug in l.path)>0
        GROUP BY a.title 
        ORDER BY views DESC
        LIMIT 3
"""
    c.execute(query)
    rows=c.fetchall()
    # Generate report row HTML
    for row in rows:
        row_html = row_html + """
   <tr>
    <td>{0}</td>
    <td>{1}</td>
   </tr>
""".format(row[0],row[1])
    print(row_html)
    db.close()
    
    row_html = """
        <h2>3 Most Popular Articles  </h2>
        <table class="tg">
        {0}
        </table>""".format(row_html)
    return row_html

# 2 Popular Author Report
def get_popular_authors():
    """Return Popular Authors"""
    row_html = """
        <tr>
            <th>Author Name</th>
            <th>Views</th>
        </tr>    
"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    # Report query
    query = """
        SELECT ath.name, count(1) as views
        FROM public.log l, public.articles a , public.authors ath
        WHERE a.author=ath.id
        AND position(a.slug in l.path)>0
        GROUP BY ath.name 
        ORDER BY views DESC
"""
    c.execute(query)
    rows=c.fetchall()
    # Generate report row HTML
    for row in rows:
        row_html = row_html + """
   <tr>
    <td>{0}</td>
    <td>{1}</td>
   </tr>
""".format(row[0],row[1])
    print(row_html)
    db.close()
    
    row_html = """
        <h2>Most Popular Authors</h2>
        <table class="tg">
        {0}
        </table>""".format(row_html)
    return row_html

# 3 Error request rate that exceeds 1%
def get_error_log():
    """Return Errored Requests Exceeding Threshold (1%)"""
    row_html = """
        <tr>
            <th>Error Requests</th>
            <th>Total Requests</th>
            <th>Error Request Rate</th>
            <th>Date</th>
        </tr>    
"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    # Report query
    query = """
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
"""
    c.execute(query)
    rows=c.fetchall()
    # Generate report row HTML
    for row in rows:
        row_html = row_html + """
   <tr>
    <td>{0}</td>
    <td>{1}</td>
    <td>{2}</td>
    <td>{3}</td>
   </tr>
""".format(row[0],row[1],row[2],row[3])
    print(row_html)
    db.close()
    
    row_html = """
        <h2>Errored Requests Exceeding Threshold 1%</h2>
        <table class="tg">
        {0}
        </table>""".format(row_html)
    return row_html

