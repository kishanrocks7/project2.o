########## NECCESSARY IMPORTS###########
import uuid,pybase64,os
from random import randint
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from datetime import date
##################database libraries ##########
from databaselibrary import getblogcur,getfaqcur
############Lib end ###########

def bloggerregister():
    if request.method  == "POST":
        fullkey = uuid.uuid4()
        uid = fullkey.time
        em = request.form['email'].lower()
        passwd = request.form['password']
        cpasswd = request.form['confirmpassword']
        if(passwd!=cpasswd):
            #flash msg
            flash('Password and Confirm Password does not match')
            return redirect(url_for('blogger_register'))
        name = str(pybase64.b64encode((request.form['bloggerName']).encode("utf-8")),"utf-8")
        email = (request.form['email'].lower())
        pno = str(pybase64.b64encode((request.form['phoneNumber']).encode("utf-8")),"utf-8")
        dob = str(pybase64.b64encode((request.form['dob']).encode("utf-8")),"utf-8")
        gender = str(pybase64.b64encode((request.form['gender']).encode("utf-8")),"utf-8")
        profession = str(pybase64.b64encode((request.form['profession']).encode("utf-8")),"utf-8")
        address = str(pybase64.b64encode((request.form['address']).encode("utf-8")),"utf-8")
        password  = str(pybase64.b64encode((request.form['password']).encode("utf-8")),"utf-8")
        cur = getblogcur()
        checkusersql = "select * from blogger where (email = %s)"
        cur.execute(checkusersql,(em))
        checkusercount = cur.rowcount
        if checkusercount == 0 :
            insertusersql = 'insert into blogger(id,name,email,phone,dob,gender,address,profession,password) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) '
            cur.execute(insertusersql,(uid,name,email,pno,dob,gender,profession,address,password))
            insertcount = cur.rowcount
            if insertcount >= 1 :
                #getting mail app with app
                app = current_app._get_current_object()
                mail = Mail(app)
                subject = "Your registration successful !"
                msg = Message(subject, sender = 'codewithash99@gmail.com', recipients = [str(em)])
                msg.body = "Hey ! you are registered with us as a Blogger !!!"
                mail.send(msg) 
                flash('You have succesfully register, You can now login!')
                return redirect(url_for('blogger_login'))
            else:
                return render_template('Blog/bloggerregister.html',failuremsg = "There is error!")
        else:
            return render_template('Blog/bloggerregister.html',failuremsg = "User is already registered with same Email !")
    return render_template('Blog/bloggerregister.html')


def bloggerlogin():
    if request.method == "POST":
        email = request.form['email'].lower()
        passwd = str(pybase64.b64encode((request.form['password']).encode("utf-8")),"utf-8")
        cur = getblogcur()
        sql = "select id,name from blogger where (email = %s   AND password= %s ) "
        cur.execute(sql,(email, passwd))
        sqlres = cur.rowcount
        logindata= cur.fetchone()
        print(logindata)
        if sqlres == 1 :
            session['blogger_id'] = logindata[0]
            session['blogger_name'] = str(pybase64.b64decode(logindata[1]),"utf-8")
            return redirect(url_for('blogs'))
        else:
            flash("Incorrect credentials!")
            return redirect(url_for('blogger_login'))
    return render_template('Blog/bloggerlogin.html')


def sendforgotpassmail(email):
    fullkey = uuid.uuid4()
    password = (fullkey.time)//10000000000
    passwd = str(pybase64.b64encode((str(password)).encode("utf-8")),"utf-8")
    cur = getblogcur()
    sql = "update blogger set password = %s where email = %s"
    cur.execute(sql,(passwd,email))
    n = cur.rowcount
    if n == 1:
        app = current_app._get_current_object()
        mail = Mail(app)
        subject = "Password Reset !"
        msg = Message(subject, sender = 'codewithash99@gmail.com', recipients = [str(email)])
        msg.body = "Hey ! you are requested to reset your password for your Login Account !!!" + "\n We are sending you a temporary Password . \n Change this after your first login under the profile section ." + "\n\n\n\n Password - "+str(password) 
        mail.send(msg) 
    else:
        flash("There is a problem with mail server !!")
        return redirect(url_for('blogger_forgot_password'))


def bloggerforgot():
    if request.method == "POST":
        email = request.form['email'].lower()
        cur = getblogcur()
        sql = "select * from blogger where (email = %s) "
        cur.execute(sql,(email))
        sqlres = cur.rowcount
        logindata= cur.fetchone()
        if sqlres == 1:
            sendforgotpassmail(email)
            flash("A Mail has been sent to you with further instructions !!")
            return redirect(url_for('blogger_login'))
        else:
            flash("You are not Registered with us as a Blogger !!")
            return redirect(url_for('blogger_forgot_password'))
    return render_template('Blog/bloggerforgotpass.html')


def bloggerprofile():
    if 'blogger_id' in session:
        id = session['blogger_id']
        cur = getblogcur()
        if request.method == 'POST':
            bloggerimg = request.files['bloggerimg']
            if bloggerimg:
                    checkphoto = "select image from blogger where id='"+id+"'"
                    cur.execute(checkphoto)
                    n=cur.rowcount
                    if n == 1:
                        prevphoto=cur.fetchone()
                        photo=prevphoto[0]
                        if photo != None:
                            os.remove("./static/photos/"+photo)
                    path=os.path.basename(bloggerimg.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    imgfilename=str(uuid.uuid4())+'.'+file_ext
                    bloggerimgname = secure_filename(imgfilename)
                    app = current_app._get_current_object()
                    bloggerimg.save(os.path.join(app.config['UPLOAD_FOLDER'],bloggerimgname))
            name = str(pybase64.b64encode((request.form['name']).encode("utf-8")),"utf-8")
            phone = str(pybase64.b64encode((request.form['phone']).encode("utf-8")),"utf-8")
            dob = str(pybase64.b64encode((request.form['dob']).encode("utf-8")),"utf-8")
            profession = str(pybase64.b64encode((request.form['profession']).encode("utf-8")),"utf-8")
            address = str(pybase64.b64encode((request.form['address']).encode("utf-8")),"utf-8")
            editprofsql = ' update blogger set name = %s,  phone = %s, dob = %s,  address = %s, profession = %s,   image = %s  where id = %s '
            viewprofsql = 'select * from blogger where id ="'+id+'"  '
            try:
                cur.execute(editprofsql,(name,phone,dob,address,profession,bloggerimgname,id))
            except:
                editprofsql = ' update blogger set name = %s,  phone = %s, dob = %s,  address = %s, profession = %s where id = %s '
                cur.execute(editprofsql,(name,phone,dob,address,profession,id))
            n = cur.rowcount
            cur.execute(viewprofsql)
            m = cur.rowcount
            if m==1:
                data = cur.fetchall()
                cd = [list(i) for i in data]
                for i in range(0,len(cd)):
                    for j in range(1,len(cd[i])-1):
                        if(j!=2):
                            cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
                td = tuple(tuple(i) for i in cd)
                return render_template('Blog/blogger_profile.html',profmsg = "Profile Updated !",pdata = td)
            return render_template('Blog/blogger_profile.html',profmsg = "There is error while changing data !",pdata = td) 
            #########GET##############################
        viewprofsql = 'select * from blogger where id ="'+id+'"  '
        cur.execute(viewprofsql)
        n = cur.rowcount
        if n == 1:
            data = cur.fetchall()
            cd = [list(i) for i in data]
            for i in range(0,len(cd)):
                for j in range(1,len(cd[i])-1):
                    if(j!=2):
                        cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
            td = tuple(tuple(i) for i in cd)
            return render_template('Blog/blogger_profile.html',pdata = td)
        return render_template('Blog/blogger_profile.html',profmsg = "There is error in displaying profile msg")
    flash('Direct access to this page is Not allowed !! Login First!')
    return redirect(url_for('blogger_login'))


def changebloggerpass():
    if 'blogger_id' in session:
        usid = session['blogger_id']
        if request.method == 'POST':
            oldpass = str(pybase64.b64encode((request.form['oldPassword']).encode("utf-8")),"utf-8")
            newpass = str(pybase64.b64encode((request.form['newPassword']).encode("utf-8")),"utf-8")
            cpass = str(pybase64.b64encode((request.form['confirmPassword']).encode("utf-8")),"utf-8")
            if(newpass != cpass):
                return render_template('Blog/changebloggerpassword.html',passmsg = "new password and confirm password doesn't match..")
            cur = getblogcur()
            cpasssql = "update blogger set password='"+newpass+"' where id = '"+usid+"' "
            cur.execute(cpasssql)
            n = cur.rowcount
            if n == 1:
                flash("password changed successfully !")
                session.pop('blogger_id',None)
                session.pop('blogger_name',None)
                return redirect(url_for('blogger_login'))
            return render_template('Blog/changebloggerpassword.html',passmsg = "New password is same as Old password")
        return render_template('Blog/changebloggerpassword.html')
    flash('Direct access to this page is Not allowed ..Login First!')
    return redirect(url_for('blogger_login'))


def addblog():
    if 'blogger_id' in session:
        ownerid = session['blogger_id']
        if request.method == 'POST': 
            ownername = str(pybase64.b64encode((session['blogger_name']).encode("utf-8")),"utf-8")
            d = str(pybase64.b64encode((str(date.today())).encode("utf-8")),"utf-8")
            fullkey = uuid.uuid4()
            blogId = fullkey.time
            title = str(pybase64.b64encode((request.form['title'].replace('\r\n','<br>')).encode("utf-8")),"utf-8")
            content = str(pybase64.b64encode((request.form['content'].replace('\r\n','<br>')).encode("utf-8")),"utf-8")
            img = request.files['blogimg']
            path=os.path.basename(img.filename)
            file_ext=os.path.splitext(path)[1][1:]
            imgfilename=str(uuid.uuid4())+'.'+file_ext
            blogimg = secure_filename(imgfilename)
            cur = getblogcur()
            insertblogsql = 'insert into blogs(blogId,ownerId,blogImage,title,content,ownerName,date) values (%s,%s,%s,%s,%s,%s,%s) '
            cur.execute(insertblogsql,(blogId,ownerid,blogimg,title,content,ownername,d))
            n = cur.rowcount
            if n == 1:
                app = current_app._get_current_object()
                img.save(os.path.join(app.config['UPLOAD_FOLDER'],blogimg))
                flash('Blog Added Successully !')
                return redirect(url_for('blogs'))
            flash('There is a problem while adding the Blog. Try again Later !!')
            return redirect(url_for('blogs'))
        return redirect(url_for('blogs'))
    flash('Direct access to this page is Not allowed ..Login First!')
    return redirect(url_for('blogger_login'))


def displayallblogs():
    cur = getblogcur()
    sql = 'select * from blogs'
    cur.execute(sql)
    n = cur.rowcount
    if n >= 1:
        data = cur.fetchall()
        cd = [list(i) for i in data]
        for i in range(0,len(cd)):
            countcomments = 'select blogId from comments where blogId = "'+cd[i][0]+'"  '
            cur.execute(countcomments)
            k = cur.rowcount
            cd[i].append(k)
            for j in range(3,len(cd[i])-1):
                cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
        td = tuple(tuple(i) for i in cd)
        print(td)
        return render_template('Blog/blog.html',bdata = td)

    flash('There is no blogs . Add some blogs here !!')
    return render_template('Blog/blog.html')    


def viewblog(blogid):
    cur = getblogcur()
    sql = 'select * from blogs where blogId = %s'
    cur.execute(sql,str(blogid))
    n = cur.rowcount
    if n == 1:
        data = cur.fetchall()
        cd = [list(i) for i in data]
        for i in range(0,len(cd)):
            for j in range(3,len(cd[i])):
                cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
        td = tuple(tuple(i) for i in cd)
        sql = 'select * from comments where blogId = %s'
        cur.execute(sql,str(blogid))
        data = cur.fetchall()
        cd = [list(i) for i in data]
        for i in range(0,len(cd)):
            for j in range(3,len(cd[i])):
                cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
        cod = tuple(tuple(i) for i in cd)
        return render_template('Blog/blog_post.html',bdata = td,cdata = cod)
    flash('There is no such blog !!')
    return render_template('Blog/blog.html')


def addcomment(blogid):
    if 'blogger_id' in session:
        userId = session['blogger_id']
        if request.method == 'POST':
            blogId = str(blogid)
            fullkey = uuid.uuid4()
            commentId = fullkey.time
            userName = str(pybase64.b64encode((session['blogger_name']).encode("utf-8")),"utf-8") 
            comment = str(pybase64.b64encode((request.form['comment']).encode("utf-8")),"utf-8")
            cur = getblogcur()
            sql = 'insert into comments(blogId,commentId,userId,userName,comment) values(%s,%s,%s,%s,%s)'
            cur.execute(sql,(blogId,commentId,userId,userName,comment))
            n = cur.rowcount
            if n == 1:
                flash('Thanks for commenting !!!')
                return redirect(url_for('blog_post',blogid=blogId))
            flash('There is a error in adding new comment !!!')
            return redirect(url_for('blog_post',blogid=blogId))
        return redirect(url_for('blog_post',blogid=blogId))
    flash('You need to first login to add a comment !!')
    return redirect(url_for('blogger_login'))


def deletecomment(blogid,commentid):
    cur = getblogcur()
    sql = 'delete from comments where commentId = %s'
    cur.execute(sql,str(commentid))
    flash('Your comment is deleted')
    return redirect(url_for('blog_post',blogid=str(blogid))) 


def deleteblog(blogid):
    cur = getblogcur()
    sql = 'delete from blogs where blogid = %s'  
    cur.execute(sql,str(blogid))
    n = cur.rowcount
    if n == 1:
        sql = 'delete from comments where blogid = %s'
        cur.execute(sql,str(blogid))
        flash('Your blog is deleted !!')
        return redirect(url_for('blogs')) 
    flash('There is a problem . Try again Later !!')
    return redirect(url_for('blogs'))


def editblog(blogid):
    if request.method == 'POST':
        cur = getblogcur()
        blogimg = request.files['blogimg']
        if blogimg:
            checkphoto = "select blogImage from blogs where blogId='"+str(blogid)+"'"
            cur.execute(checkphoto)
            n=cur.rowcount
            if n == 1:
                prevphoto=cur.fetchone()
                photo=prevphoto[0]
                if photo != None:
                    os.remove("./static/photos/"+photo)
            path=os.path.basename(blogimg.filename)
            file_ext=os.path.splitext(path)[1][1:]
            imgfilename=str(uuid.uuid4())+'.'+file_ext
            blogimgname = secure_filename(imgfilename)
            app = current_app._get_current_object()
            blogimg.save(os.path.join(app.config['UPLOAD_FOLDER'],blogimgname))
            title = str(pybase64.b64encode((request.form['title'].replace('\r\n','<br>')).encode("utf-8")),"utf-8")
            content = str(pybase64.b64encode((request.form['content'].replace('\r\n','<br>')).encode("utf-8")),"utf-8")
            sql = 'update blogs set blogImage = %s , title = %s , content = %s where blogId = %s'
            cur.execute(sql,(blogimgname,title,content,str(blogid)))
            n = cur.rowcount
            if n == 1:
                flash('Your blog is successfully edited !!')
                return redirect(url_for('blog_post',blogid=str(blogid)))
            flash('There is some problem. Try again Later !!')
            return redirect(url_for('blog_post',blogid=str(blogid)))
        else :
            title = str(pybase64.b64encode((request.form['title'].replace('\r\n','<br>')).encode("utf-8")),"utf-8")
            content = str(pybase64.b64encode((request.form['content'].replace('\r\n','<br>')).encode("utf-8")),"utf-8")
            sql = 'update blogs set  title = %s , content = %s where blogId = %s'
            cur.execute(sql,(title,content,str(blogid)))
            n = cur.rowcount
            if n == 1:
                flash('Your blog is successfully edited !!')
                return redirect(url_for('blog_post',blogid=str(blogid)))
            flash('There is some problem. Try again Later !!')
            return redirect(url_for('blog_post',blogid=str(blogid)))
    return redirect(url_for('blog_post',blogid=str(blogid)))

def faq():
    sql = 'select * from questions'
    cur = getfaqcur()
    cur.execute(sql)
    n =cur.rowcount
    if n>= 1:
        data = cur.fetchall()
        return render_template('faq.html', quesdata = data)
    flash('There is no questions Posted Yet !')
    return render_template('faq.html')

def addques():
    if 'blogger_id' in session:
        userId = session['blogger_id']
        if request.method == 'POST': 
            userName = session['blogger_name']
            d = str(date.today())
            fullkey = uuid.uuid4()
            quesId = fullkey.time
            question = request.form['question'].replace('\r\n','<br>')
            cur = getfaqcur()
            sql = 'insert into questions(quesId,userId,date,userName,question) values(%s,%s,%s,%s,%s) '
            cur.execute(sql,(quesId,userId,d,userName,question))
            n = cur.rowcount
            if n == 1:
                flash("Your question is successfully Posted..wait for It's answer ! ")
                return redirect(url_for('faqs'))
            flash('There is error in Posting question !')
            return redirect(url_for('faqs'))
        return redirect(url_for('faqs'))
    flash("You must login to  Post a question Or register if you don't have an account !")
    return redirect(url_for('blogger_login'))

def postans():
    if 'blogger_id' in session:
        userId = session['blogger_id']
        if request.method == 'POST': 
            quesId = request.form['quesid']
            userName = session['blogger_name']
            d = str(date.today())
            fullkey = uuid.uuid4()
            ansId = fullkey.time
            answer = request.form['answer'].replace('\r\n','<br>')
            cur = getfaqcur()
            sql = 'update questions set ansuserId =%s,ansId =%s,ansuserName =%s,ansdate=%s,answer =%s where quesId = %s'
            cur.execute(sql,(userId,ansId,userName,d,answer,quesId))
            n = cur.rowcount
            if n == 1:
                flash("Your answer is successfully take for the question ! ")
                return redirect(url_for('faqs'))
            flash('There is error in Posting answer !')
            return redirect(url_for('faqs'))
        return redirect(url_for('faqs'))
    flash("You must login to  Post a answer Or register if you don't have an account !")
    return redirect(url_for('blogger_login'))
