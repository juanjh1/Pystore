from flask import Flask
from flask import render_template,request,redirect
from flask import session

from database import  User
from database import Product

app = Flask(__name__)
app.secret_key = '123456789'




@app.route('/')
def index ():

    
    product1 = 0
    products = Product.select()
    for product in  products:
        product1 += 1
        
    return render_template('index.html', products = product1)

@app.route('/register', methods=['GET', 'POST'])
def register():
         
        
        if request.method == 'POST':
            #print(request.form) # dict
            email  = request.form.get('email')
            password = request.form.get('password')
            username = request.form.get('username')

            

            if email and password :
                
                    user = User.create_user(username= username, email = email, password=password) #insert into
                    if user is not None:
                        session['user'] = user.id
                        session['status'] = 'login'
                        print(user)
                        if user:
                            return redirect('/products')
                    else:
                        return redirect('/')
                
        users = User.select()
        num_user = 0
        for i in users:
            num_user += 1
            
        if num_user != 0:
            if session.get('status') == 'login':
                return redirect('/products')
            else:
                return render_template('register.html') 
        else:
             return render_template('register.html') 

@app.route('/login', methods=['GET', 'POST'])
def login():
    
        if request.method == 'POST':
            #print(request.form) # dict

            email  = request.form.get('email')
            password = request.form.get('password')
            if email and password:
                user = User.get(User.email == email)
                
                if password == user.password:
                #User.select( User.id).where(User.email == email and User.password==password)   
                    
                    session['user'] = user.id
                    session['status'] = 'login'
                    return redirect('/products')
                else: 
        
                  return redirect('/')

    
        if session.get('status') == 'login':
                return redirect('/products')
        else:
            return render_template('login.html')
                
        
   
        

@app.route('/products')
def products ():
    if session != {}:
        _user  = User.select().where(User.id == session['user'] ) 
        
        #get(session['user'])

        #print(user.show_user)
        products = Product.select().where(Product.user == _user)
        user = User.get(session['user'])
        a= user.email
        return render_template('products/index.html', products= products, user = user)
    else:
        return redirect('/')

@app.route('/products/create', methods=['GET', 'POST'])
def product_create ():
    if session != {}:
        if request.method == 'POST':
            name = request.form.get('name')
            price = request.form.get('price')

            if name and price:
                user = User.get(session['user'])
                product = Product.create(name=name, price=price, user=user)
                return redirect('/products')
        return render_template('products/create.html')
    else:
        return redirect('/')
        


@app.route('/products/update/<id>', methods=['GET', 'POST'] )
def products_upadate (id):
        _user  = User.select().where(User.id == session['user'] ) 

        products = Product.select().where(Product.user == _user)
        
        
        ids = []
        for product in products:
            ids.append(product.id)
            print(type(product.id))
            
        if int(id) in ids:
    
            if session != {}:
                product = Product.select().where(Product.id == id).first()
                
                if request.method == 'POST':
                    product.name = request.form.get('name')
                    product.price = request.form.get('price')
                    product.save() # UPDATE products SET name='' 
                    
                    return redirect('/products')
                
                return render_template('products/update.html', product=product)
            else:
                return redirect('/products')
        else:

            return redirect('/products')
    

@app.route('/products/delete/<id>', methods=['GET', 'POST'] )
def products_delete (id):

        _user  = User.select().where(User.id == session['user'] ) 

        products = Product.select().where(Product.user == _user)
        
        ids = []
        for product in products:
            ids.append(product.id)
    
        if int(id) in ids:

                if session != {}:
                    product = Product.select().where(Product.id == id).first()
                    
                    if request.method == 'POST':
                        product.delete_instance()
                        product.save()
                    
                        return redirect('/products')
                    
                    return render_template('products/delete.html', product=product)
                else:
                    return redirect('/products')
        else:
            return redirect('/products')


@app.route('/logout' )
def logout ():
   
    session.clear()
    return render_template('out/index.html')


   

if __name__ == '__main__':

    app.run(debug=True)