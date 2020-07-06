####################NECCESSARY IMPORTS ################
import uuid,pybase64
from random import randint
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
from flask_mail import Mail, Message

############databaselib###################
from databaselibrary import getdbcur


def countbar(warehouseid):
    sql = 'SELECT commodityType , commodityUnits FROM producer where warehouseid = %s'
    cur = getdbcur()
    cur.execute(sql,warehouseid)
    n = cur.rowcount
    cbar=[0,0,0,0,0,0,0,0]
    if n >= 1:
        data = cur.fetchall()
        cd = [list(i) for i in data]
        for i in range(0,len(cd)):
            for j in range(0,len(cd[i])):
                cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
        td = list(list(i) for i in cd)
        for i in td:
            if i[0] == 'black Pepper':
                cbar[0] = cbar[0]+ int(i[1])
            elif i[0] == 'turmeric':
                cbar[1] = cbar[1]+int(i[1])
            elif i[0] == 'cinnamon':
                cbar[2] = cbar[2]+int(i[1])
            elif i[0] == 'red chilly':
                cbar[3] = cbar[3]+int(i[1])
            elif i[0] == 'mustard':
                cbar[4] = cbar[4]+int(i[1])
            elif i[0] == 'clove':
                cbar[5] = cbar[5]+int(i[1])
            elif i[0] == 'cumin':
                cbar[6] = cbar[6]+int(i[1])
            elif i[0] == 'chick Pea':
                cbar[7] = cbar[7]+int(i[1])
            else:
                continue
    return cbar


def producerhome():
    if 'user_id' in session:
        warehouseid = str(session['user_id'])
        cbar = countbar(warehouseid)
        sql = 'select * from producer where warehouseid =  %s'
        cur = getdbcur()
        cur.execute(sql,warehouseid)
        n = cur.rowcount
        if n >= 1:
            data = cur.fetchall()
            cd = [list(i) for i in data]
            for i in range(0,len(cd)):
                for j in range(1,len(cd[i])-1):
                    cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
            td = tuple(tuple(i) for i in cd)
            return render_template('producers.html',pdata = td,cbar = cbar)
        else:
            return render_template('producers.html', pmsg = "currently there is NO Producer information !",cbar = cbar)
    flash('You must login first to view Producers!')
    return redirect(url_for('warehouse_login'))


def addproducer():
    if 'user_id' in session:
        warehouseid = str(session['user_id'])
        cbar = countbar(warehouseid)
        if request.method == 'POST':
            fullkey = uuid.uuid4()
            uid = fullkey.time
            name = str(pybase64.b64encode((request.form['name'].lower()).encode("utf-8")),"utf-8")
            phoneNumber = str(pybase64.b64encode((request.form['phoneNumber'].lower()).encode("utf-8")),"utf-8")
            email = str(pybase64.b64encode((request.form['email'].lower()).encode("utf-8")),"utf-8")
            gender = str(pybase64.b64encode((request.form['gender'].lower()).encode("utf-8")),"utf-8")
            age = str(pybase64.b64encode((request.form['age'].lower()).encode("utf-8")),"utf-8")
            address = str(pybase64.b64encode((request.form['address'].lower()).encode("utf-8")),"utf-8")
            commodityType = str(pybase64.b64encode((request.form['commodityType'].lower()).encode("utf-8")),"utf-8")
            commodityUnits = str(pybase64.b64encode((request.form['commodityUnits'].lower()).encode("utf-8")),"utf-8")
            aadharNumber = str(pybase64.b64encode((request.form['aadharNumber'].lower()).encode("utf-8")),"utf-8")
            addquery ='insert into producer values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cur = getdbcur()
            cur.execute(addquery,( uid,name,age,gender,phoneNumber,email,address,commodityType,commodityUnits,aadharNumber,warehouseid))
            n = cur.rowcount
            if (n == 1):
                flash(' New Producer details added!')
                return redirect(url_for('producer'))
            else:
                return render_template('producers.html', pmsg = 'Adding new producer details failed!',cbar = cbar)
        return render_template('producers.html',cbar = cbar)
    flash('Direct access to this page is Not allowed !')
    return redirect(url_for('warehouse_login'))
    

def changeproducer():
    if 'user_id' in session:
        if request.method == 'POST':
            id =request.form['id']
            name = str(pybase64.b64encode((request.form['name'].lower()).encode("utf-8")),"utf-8")
            email = str(pybase64.b64encode((request.form['email'].lower()).encode("utf-8")),"utf-8")
            number = str(pybase64.b64encode((request.form['phoneNumber'].lower()).encode("utf-8")),"utf-8")
            gender = str(pybase64.b64encode((request.form['gender'].lower()).encode("utf-8")),"utf-8")
            age = str(pybase64.b64encode((request.form['age'].lower()).encode("utf-8")),"utf-8")
            address = str(pybase64.b64encode((request.form['address'].lower()).encode("utf-8")),"utf-8")
            commoditytype = str(pybase64.b64encode((request.form['commodityType'].lower()).encode("utf-8")),"utf-8")
            commodityunits = str(pybase64.b64encode((request.form['commodityUnits'].lower()).encode("utf-8")),"utf-8")
            aadharNumber = str(pybase64.b64encode((request.form['aadharNumber'].lower()).encode("utf-8")),"utf-8")
            editquery = 'update producer set name =%s,emailId=%s,contactNumber=%s,commodityType=%s,commodityUnits=%s, age=%s, gender=%s, address=%s,aadharNumber=%s where unique_key=%s '
            cur =getdbcur()
            cur.execute(editquery,(name,email,number,commoditytype,commodityunits,age,gender,address,aadharNumber,id))
            n =cur.rowcount
            if n == 1:
                flash('producers Details changed Successfully !')
                return redirect(url_for('producer'))
            else:
                flash('Nothing will be changed in producers details !')
                return redirect(url_for('producer'))
        return redirect(url_for('producer'))
    flash('Direct access to this page is Not Alloed Login first To view this page!')
    return redirect(url_for('warehouse_login'))


def deleteproducer():
    if 'user_id' in session:
        if request.method == 'POST':
            id = request.form['id']
            delquery = 'delete from producer where unique_key="'+id+'"   '
            cur =getdbcur()
            cur.execute(delquery)
            n =cur.rowcount
            if n == 1:
                flash('producers Details deleted Successfully !')
                return redirect(url_for('producer'))
            else:
                flash('There is error in deleting producers details !')
                return redirect(url_for('producer'))
        return redirect(url_for('producer'))
    flash('Direct access to this page is Not Alloed Login first To view this page!')
    return redirect(url_for('warehouse_login'))


def searchproducer():
    if 'user_id' in session:
        warehouseid = str(session['user_id'])
        cbar = countbar(warehouseid)
        if request.method == 'POST':
            si = str(pybase64.b64encode((request.form['searchinp'].lower()).encode("utf-8")),"utf-8")
            searchquery = "select * from producer where (name like  '%"+si+"%'  OR commodityType like   '%"+si+"%' )  and warehouseid = '"+warehouseid+"' "
            cur =getdbcur()
            cur.execute(searchquery)
            n =cur.rowcount
            if n >= 1:
                data = cur.fetchall()
                cd = [list(i) for i in data]
                for i in range(0,len(cd)):
                    for j in range(1,len(cd[i])-1):
                        cd[i][j] = str(pybase64.b64decode(cd[i][j]),"utf-8")
                td = tuple(tuple(i) for i in cd)
                return render_template('producers.html',pdata = td,pmsg="Search Results!",cbar = cbar)
            else:
                return render_template('producers.html', pmsg = "No results for search..try different key!",cbar = cbar)
        else:
            return render_template('producers.html', pmsg = "Enter something to search!",cbar = cbar)
    flash('You must login first to view Producers!')
    return redirect(url_for('warehouse_login'))