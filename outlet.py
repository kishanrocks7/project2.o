#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
#universal unique ID package
import uuid,pybase64,os
from random import randint
#secure Filename
from werkzeug.utils import secure_filename
#importing mail
from flask_mail import Mail, Message
########importing database lib##########
from databaselibrary import getoutletcur
##############endlib ###############

def outletregister():
    if request.method =='POST':
        fullkey = uuid.uuid4()
        uid = fullkey.time
        em = request.form['email']
        passwd = request.form['password']
        cpasswd = request.form['confirmpassword']
        longitude = request.form['longitude']
        latitude =  request.form['latitude']
        if(not latitude or not longitude):
            flash('You denied the location access !!')
            return redirect(url_for('warehouse_register'))
        if(passwd!=cpasswd):
            #flash msg
            flash('Password and Confirm Password does not match')
            return redirect(url_for('outlet_register'))
        otype = str(pybase64.b64encode((request.form['type'].lower()).encode("utf-8")),"utf-8")
        mname = str(pybase64.b64encode((request.form['managername'].lower()).encode("utf-8")),"utf-8")
        email = str(pybase64.b64encode((request.form['email'].lower()).encode("utf-8")),"utf-8")
        cinno = str(pybase64.b64encode((request.form['cinno']).encode("utf-8")),"utf-8")
        pno = str(pybase64.b64encode((request.form['phoneNumber'].lower()).encode("utf-8")),"utf-8")
        address = str(pybase64.b64encode((request.form['address'].lower()).encode("utf-8")),"utf-8")
        password  = str(pybase64.b64encode((request.form['password']).encode("utf-8")),"utf-8")
        cur = getoutletcur()
        checkusersql = "select * from outlet where (email = %s OR contactNumber = %s )"
        cur.execute(checkusersql,(email,pno))
        checkusercount = cur.rowcount
        if checkusercount == 0 :
            insertusersql = 'insert into outlet(id,type,managerName,contactNumber,email,address,CINnumber,password,longitude,latitude) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '
            cur.execute(insertusersql,(uid,otype,mname,pno,email,address,cinno,password,longitude,latitude))
            insertcount = cur.rowcount
            if insertcount >= 1 :
                #getting mail app with app
                app = current_app._get_current_object()
                mail = Mail(app)
                subject = "Your registration successful !"
                msg = Message(subject, sender = 'codewithash99@gmail.com', recipients = [str(em)])
                msg.body = "Hey ! you are registered with us. \n Your unique id to access the Outlet dashboard is " + str(uid) + "\n Save this key for your future reference !!\n Thank you for choosing our services."
                mail.send(msg) 
                flash('You have succesfully register, You can now login as Oulet user !')
                return redirect(url_for('outlet_login'))
            else:
                return render_template('Outlet/outletregister.html',failuremsg = "There is error!")
        else:
            return render_template('Outlet/outletregister.html',failuremsg = "User is already registered with same Email or Phone Number!")
    return render_template('Outlet/outletregister.html')


def outletdash():
    if request.method == "POST":
        user_id = request.form['userid']
        em_or_num = str(pybase64.b64encode((request.form['em_or_num'].lower()).encode("utf-8")),"utf-8")
        manager_name = request.form['manager_name']
        mname = str(pybase64.b64encode((request.form['manager_name'].lower()).encode("utf-8")),"utf-8")
        passwd = str(pybase64.b64encode((request.form['password']).encode("utf-8")),"utf-8")
        cur = getoutletcur()
        sql = "select type from outlet where (id = %s  AND (email = %s OR contactNumber = %s ) AND managerName=%s AND password= %s ) "
        cur.execute(sql,(user_id, em_or_num, em_or_num , mname, passwd))
        sqlres = cur.rowcount
        details = cur.fetchone()
        if sqlres == 1 :
            outletId = session['outlet_id']
            sql = 'select * from outletnotification where outletId=%s'
            cur = getoutletcur()
            cur.execute(sql,(outletId))
            n = cur.rowcount
            outlettype = str(pybase64.b64decode(details[0]),"utf-8")
            if n > 0:
                session['notifcountoutlet'] = n
            session['outlet_id'] = user_id 
            session['user_name'] = manager_name
            session['outlet_type'] = outlettype
            return redirect(url_for('outlet_dashboard'))
        else:
            flash("Incorrect credentials!")
            return redirect(url_for('outlet_login'))
    if 'outlet_id' in session:
        return render_template('Outlet/outlet_home.html')
    else:
        flash('You have to Login First to view Dashboard !!')
        return redirect(url_for('outlet_login'))

def outletforget():
    if request.method == 'POST':
        user_id =  request.form['id']
        em = request.form['email']
        email = str(pybase64.b64encode((em).encode("utf-8")),"utf-8")
        randcode = randint(100000,999999)   #Generating 6 digit random int
        sql = ' update outlet set resetcode = %s where (id = %s  AND email = %s) '
        cur = getoutletcur()
        cur.execute(sql,(randcode, user_id, email))
        n = cur.rowcount
        if n == 1 :
        #getting mail app with app
            app = current_app._get_current_object()
            mail = Mail(app)
            subject = "verification code for account"
            msg = Message(subject, sender = 'codewithash99@gmail.com', recipients = [str(em)])
            msg.body = "Your verification code  is " + str(randcode) +" after input you have to change your password!!" 
            mail.send(msg) 
            flash('Check your verification code in your email')
            return  redirect(url_for('reset_outlet_password'))
        else:
            return render_template('Outlet/forgot_outlet_password.html', fmsg ="Either unique Id or email is incorrect..try again!")
    return render_template('Outlet/forgot_outlet_password.html')

def resoutletpass():
    if request.method == 'POST':
        user_id =  request.form['id']
        verifcode =  request.form['verifcode'] 
        passwd = str(pybase64.b64encode((request.form['pass']).encode("utf-8")),"utf-8")
        if(verifcode == None):
            flash("please fill out the verification code")
            return redirect(url_for('reset_password'))
        cur = getoutletcur()
        idquery = 'select managerName from outlet where id= "'+user_id+'" AND resetcode = "'+verifcode+'"  '
        cur.execute(idquery)
        m =cur.rowcount
        if m == 1:
            resquery = ' update outlet set password = %s  where (id = %s  AND resetcode = %s) '
            cur.execute(resquery,(passwd, user_id, verifcode))
            n = cur.rowcount
            if n ==1 :
                delquery = ' update outlet set resetcode = %s  where id = %s '
                cur.execute(delquery,(uuid.uuid4().hex,user_id))
                flash('Your password is Changed ..You can now Login!')
                return redirect(url_for('outlet_login'))
            else:
                return render_template('Outlet/reset_outlet_password.html', samepassmsg ="You password is same as previous One..login from below")
        else:
                return render_template('Outlet/reset_outlet_password.html', rmsg ="Either unique Id or verification code is incorrect.. please try again!")
    return render_template('Outlet/reset_outlet_password.html')


def outletprofile():
    if 'outlet_id' in session:
        id = session['outlet_id']
        cur = getoutletcur()
        if request.method == 'POST':
            outletimg = request.files['outletimg']
            if outletimg:
                    checkphoto = "select image from outlet where id='"+id+"'"
                    cur.execute(checkphoto)
                    n=cur.rowcount
                    if n == 1:
                        prevphoto=cur.fetchone()
                        photo=prevphoto[0]
                        if photo != None:
                            os.remove("./static/photos/"+photo)
                    path=os.path.basename(outletimg.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    imgfilename=str(uuid.uuid4())+'.'+file_ext
                    oimgname = secure_filename(imgfilename)
                    app = current_app._get_current_object()
                    outletimg.save(os.path.join(app.config['UPLOAD_FOLDER'],oimgname))
            otype = str(pybase64.b64encode((request.form['otype'].lower()).encode("utf-8")),"utf-8")
            manname = str(pybase64.b64encode((request.form['manname'].lower()).encode("utf-8")),"utf-8")
            manemail = str(pybase64.b64encode((request.form['manemail'].lower()).encode("utf-8")),"utf-8")
            manno = str(pybase64.b64encode((request.form['manno'].lower()).encode("utf-8")),"utf-8")
            address = str(pybase64.b64encode((request.form['address'].lower()).encode("utf-8")),"utf-8")
            cinnum = str(pybase64.b64encode((request.form['cinnum']).encode("utf-8")),"utf-8")
            editprofsql = ' update outlet set type = %s,  managerName = %s, contactNumber = %s,  email = %s,  address = %s, image = %s, CINnumber = %s  where id = %s '
            viewprofsql = 'select * from outlet where id ="'+id+'"  '
            try:
                cur.execute(editprofsql,(otype,manname,manno,manemail,address,wimgname,cinnum,id))
            except:
                editprofsql = ' update outlet set type = %s,  managerName = %s, contactNumber = %s,  email = %s,  address = %s, CINnumber = %s  where id = %s '
                cur.execute(editprofsql,(otype,manname,manno,manemail,address,cinnum,id))
            n = cur.rowcount
            cur.execute(viewprofsql)
            m = cur.rowcount
            if m==1:
                data = cur.fetchall()
                cd = [list(i) for i in data]
                for i in range(0,len(cd)):
                    for j in range(3,len(cd[i])-2):
                        cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
                td = tuple(tuple(i) for i in cd)
                return render_template('Outlet/outlet_profile.html',profmsg = "Profile Updated !",pdata = td)
            return render_template('Outlet/outlet_profile.html',profmsg = "There is error while changing data !",pdata = td) 
        viewprofsql = 'select * from outlet where id ="'+id+'"  '
        cur.execute(viewprofsql)
        n = cur.rowcount
        if n == 1:
            data = cur.fetchall()
            cd = [list(i) for i in data]
            for i in range(0,len(cd)):
                for j in range(3,len(cd[i])-2):
                    cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
            td = tuple(tuple(i) for i in cd)
            return render_template('Outlet/outlet_profile.html',pdata = td)
        return render_template('Outlet/outlet_profile.html',profmsg = "There is error in displaying profile msg")
    flash('Direct access to this page is Not allowed ..Login First!')
    return redirect(url_for('outlet_login'))