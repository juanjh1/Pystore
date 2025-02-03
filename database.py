from peewee import *
#from decouple import config
import datetime
import setup 

database = MySQLDatabase(
                       setup.DB_NAME,
                        user= setup.DB_USER_NAME,
                        password =  setup.PASSWORD, 
                        port=3306, 
                        host= setup.HOST
)

class User(Model): #tablas 
    email = TextField( )
    password = TextField()
    username = TextField()
    created_at = DateTimeField(default = datetime.datetime.now())
  
   
    @property
    def show_user(self):return f'Welcome { self.username }'
    class Meta:
        database = database
        db_table= 'users'
    @classmethod
    def create_user (cls, email, username, password):
        #algoritomo de encriptacion
        #validar que el correo sea unico
        emails= []

        usernames =[]

        users = User.select()
        for user in users :
            emails.append(user.email)
            usernames.append(user.username)
        if email not in emails and username not in usernames:
            return User.create(email=email, username=username,password=password)
        else:
            return None
   

class Product (Model): #productos
    name  = TextField( )
    price = IntegerField()
    user = ForeignKeyField(User, backref='products')
    created_at = DateTimeField(default = datetime.datetime.now())

    @property
    def price_format (self):  return f'${ self.price // 100} dolares '

    class Meta:
        database = database
        db_table= 'products'
    
database.create_tables([User, Product])
