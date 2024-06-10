serverName = "KDR"  # server name
userName = 'KDR\dell'  # user name
password = ''  # password if it requires
dbName = 'fabricAirDb'  # your db name

# db connection string
SQLALCHEMY_DATABASE_URI = (
    "mssql+pyodbc://@"
    f"{serverName}/{dbName}?"
    "driver=ODBC+Driver+18+for+SQL+Server&"
    "Trusted_Connection=yes&"
    "MARS_Connection=Yes&"
    "Encrypt=no&"
    "TrustServerCertificate=yes"
)
