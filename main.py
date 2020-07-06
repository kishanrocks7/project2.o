#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
#universal unique ID package
import uuid,pybase64,os
#secure Filename
from werkzeug.utils import secure_filename
#importing mail library
from flask_mail import Mail, Message
# This is main app point
app = Flask(__name__)
#upload Folder config

app.config['UPLOAD_FOLDER']='./static/photos'
# mail configs
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'codewithash99@gmail.com'
app.config['MAIL_PASSWORD'] = '12345@aB'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#warehouse functions
from warehouse import wdashboard,wreg,wareforget,respass,wareprofile,lgout,changepass,warenotif
# producer functions
from producer import producerhome,addproducer,changeproducer,deleteproducer,searchproducer
#blogger Functions
from blog import bloggerlogin,bloggerregister,bloggerforgot,bloggerprofile,changebloggerpass,addblog,displayallblogs,viewblog,addcomment,deletecomment,deleteblog,editblog,addques,faq,postans
#Outlet Functions 
from outlet import outletregister,outletforget,resoutletpass,outletdash,outletprofile
#Client Functions
from clients import addclient,outletclients,changeclient,deleteclient,searchclient
#Staff functions
from staff import staffhome,addstaff,searchstaff,deletestaff,changestaff
#Other Funcions
from others import getthreeblogs,homedata,addmember,addflex,clientreview
#nearest warehouse functions
from nearestwarehouse import nearestone,reqware
#notifications
from notification import accept_order,reject_order,outletnotification,deleteaccepted,deleterejected
##################### SECRET KEY USED AT THE TIME OF PAYMENT GATEWAYS ##########################
app.secret_key= 'secret4key'

######################################## ALL ROUTES IN SITE ###############################

@app.route('/')
def home():
    return homedata()
    
@app.route('/warehouse_login')
def warehouse_login():
    return  render_template('warehouselogin.html')

@app.route('/warehouse_dashboard', methods = ['GET','POST'] )
def warehouse_dashboard():
    return wdashboard()


@app.route('/warehouse_register',methods = ['GET','POST'])
def warehouse_register():
    return wreg()

@app.route('/forgot_password',methods = ['GET','POST'])
def forgot_password():
    
    return wareforget()

@app.route('/reset_password',methods = ['GET','POST'])
def reset_password():
    return respass()

@app.route('/producer')
def producer():
    return producerhome()

@app.route('/change_producer_details',methods = ['GET','POST'])
def change_producer_details():
    return changeproducer()

@app.route('/delete_producer_details',methods = ['GET','POST'])
def delete_producer_details():
    return deleteproducer()

@app.route('/search_producer',methods = ['GET','POST'])
def search_producer():
    return searchproducer()

@app.route('/add_producer', methods = ['GET','POST'])
def add_producer():
    return addproducer()

@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')

@app.route('/warehouse_profile', methods = ['GET','POST'])
def warehouse_profile():
    return wareprofile()

@app.route('/faqs')
def faqs():
    return faq()


@app.route('/database_crud')
def database_crud():
    return render_template('databasecrud.html')



@app.route('/change_password',methods = ['GET','POST'])
def change_password():
    return changepass()

@app.route('/logout')
def logout():
    return lgout()

@app.route('/add_member',methods = ['GET','POST'])
def add_member():
    return addmember()

@app.route('/add_flex',methods = ['GET','POST'])
def add_flex():
    return addflex()

@app.route('/client_review',methods = ['GET','POST'])
def client_review():
    return clientreview() 

#######################################BLOGGER PART #######################################
@app.route('/blogs')
def blogs():
    return displayallblogs()

@app.route('/blog_post/<blogid>')
def blog_post(blogid):
    return viewblog(blogid)

@app.route('/blogger_register',methods=['GET','POST'])
def blogger_register():
    return bloggerregister() 

@app.route('/blogger_login',methods=['GET','POST'])
def blogger_login():
    return bloggerlogin()

@app.route('/blogger_forgot_password',methods=['GET','POST'])
def blogger_forgot_password():
    return bloggerforgot()
    
@app.route('/blogger_profile',methods=['GET','POST'])
def blogger_profile():
    return bloggerprofile()

@app.route('/change_blogger_password',methods = ['GET','POST'])
def change_blogger_password():
    return changebloggerpass()

@app.route('/add_new_blog',methods = ['GET','POST'])
def add_new_blog():
    return addblog()

@app.route('/add_new_comment/<blogid>',methods = ['GET','POST'])
def add_new_comment(blogid):
    return addcomment(blogid)

@app.route('/delete_comment/<blogid>/<commentid>',methods = ['GET','POST'])
def delete_comment(blogid,commentid):
    return deletecomment(blogid,commentid)

@app.route('/delete_blog/<blogid>',methods = ['GET','POST'])
def delete_blog(blogid):
    return deleteblog(blogid)

@app.route('/edit_blog/<blogid>',methods = ['GET','POST'])
def edit_blog(blogid):
    return editblog(blogid)

########### OUTLET PART #################

@app.route('/outlet_dashboard',methods=['GET','POST'])
def outlet_dashboard():
    return outletdash()

@app.route('/outlet_login')
def outlet_login():
    return  render_template('Outlet/outletlogin.html')

@app.route('/outlet_register',methods=['GET','POST'])
def outlet_register():
    return outletregister()

@app.route('/forgot_outlet_password',methods = ['GET','POST'])
def forgot_outlet_password():
    return outletforget()

@app.route('/reset_outlet_password',methods = ['GET','POST'])
def reset_outlet_password():
    return resoutletpass()

@app.route('/outlet_profile',methods = ['GET','POST'])
def outlet_profile():
    return outletprofile()

@app.route('/outlet_clients',methods = ['GET','POST'])
def outlet_clients():
    return outletclients()

@app.route('/add_client',methods = ['GET','POST'])
def add_client():
    return addclient()

@app.route('/change_client_details',methods = ['GET','POST'])
def change_client_details():
    return changeclient()

@app.route('/delete_client_details',methods = ['GET','POST'])
def delete_client_details():
    return deleteclient()

@app.route('/search_client',methods = ['GET','POST'])
def search_client():
    return searchclient()

@app.route('/staff_crud')
def staff_crud():
    return staffhome()

@app.route('/add_staff',methods = ['GET','POST'])
def add_staff():
    return addstaff()

@app.route('/search_staff',methods = ['GET','POST'])
def search_staff():
    return searchstaff()

@app.route('/delete_staff_details',methods = ['GET','POST'])
def delete_staff_details():
    return deletestaff()

@app.route('/change_staff_details',methods = ['GET','POST'])
def change_staff_details():
    return changestaff()

@app.route('/nearest_warehouses')
def nearest_warehouses():
    return nearestone()

@app.route('/send_request_warehouse',methods=['GET','POST'])
def  send_request_warehouse():
    return reqware()

@app.route('/warehouse_notification',methods = ['GET','POST'])
def warehouse_notification():
    return warenotif()

@app.route('/acceptorder',methods = ['GET','POST'])
def acceptorder():
    return accept_order()

@app.route('/rejectorder',methods = ['GET','POST'])
def rejectorder():
    return reject_order()

@app.route('/outlet_notification',methods = ['GET','POST'])
def outlet_notification():
    return outletnotification()

@app.route('/deleterejectedorder',methods= ['GET','POST'])
def deleterejectedorder():
    return deleterejected()

@app.route('/deleteacceptedorder',methods= ['GET','POST'])
def deleteacceptedorder():
    return deleteaccepted()

@app.route('/post_question',methods= ['GET','POST'])
def post_question():
    return addques()

@app.route('/post_answer',methods= ['GET','POST'])
def post_answer():
    return postans()
# ###################ROUTES END HERE #########################

####################MAIN APP IS RUN FROM HERE #######################

#  At the time of deployment make sure that debug is not enabled 
if __name__ == "__main__":
    app.run(debug=True)