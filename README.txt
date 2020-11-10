This was my final project for advanced python programming at https://maktabkhooneh.org/



TLDR  if u just want to see the prediction run 'database.py' and then 'ml.py' otherwise, read on.	:)


These scripts scrape laptop data from digikala.com and tries to learn a machine learning model to predict laptop price base on specs.

Each scipt will produce a file as output and the next script uses that file. so u can run each script independently of others.
But if u want to run all of them, they have to be ran in this order:

1. getId.py     -> this program grabs all laptop id data from digikala and saves them in id.txt
2. getData.py   -> this program uses id.txt to grab laptop data from digikala and stores them in products.json
3. dataProcess.py   -> uses products.json and cleans up the data and stores them in processed.csv
4. database.py      -> uses processed.csv and writes all data to mysql
5. ml.py        -> reads data from mysql and creates a machine learning model and makes a price prediction


P.S.  Don't forget to change MYSQL_PASSWORD to your root mysql password (files : database.py , ml.py)

P.S.  all the steps before database.py are already ran. if you want to rerun them make sure to delete the corresponding outputfile
      e.g.  if u want to run getID.py , delete id.txt first

P.S.  Some Plots are available in /plots



In case any network Issues, i have provided a copy of all output files in /datafiles/v2 you can just copy its contents to /

Dependency list is provided in requirements.txt


thanks for reading !
