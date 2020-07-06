#importing neccessary libraries
from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
#universal unique ID package
import uuid,pybase64,os
from random import randint
#secure Filename
from werkzeug.utils import secure_filename
#importing mail
from flask_mail import Mail, Message
from geopy.distance import geodesic 
from databaselibrary import getdbcur , getoutletcur

def accept_order():
    if 'user_id' in session:
        if  request.method == 'POST':
            requestid = request.form['requestid']
            sql = 'select outletId,productName from warehousenotification where requestId=%s'
            cur = getdbcur()
            cur.execute(sql,(requestid))
            n=cur.rowcount
            if n==1:
                data = cur.fetchone()
                outletId = str(data[0])
                productName = str(data[1])
                warehouseId = session['user_id']
                fullkey = uuid.uuid4()
                responseId = fullkey.time
                result='accept'
                sql = 'insert into outletnotification values (%s,%s,%s,%s,%s,%s)'
                cur = getoutletcur()
                cur.execute(sql,(responseId,requestid,outletId,warehouseId,result,productName))
                n = cur.rowcount
                if n==1:
                    sql = 'delete from warehousenotification where requestId=%s'
                    cur = getdbcur()
                    cur.execute(sql,(requestid))
                    n = cur.rowcount
                    if n==1:
                        flash('Your order accept answer is send to the outlet manager')
                        return redirect(url_for('warehouse_notification'))
                    flash('There is some error in sending the response to the outlet manager')
                    return redirect(url_for('warehouse_notification'))
                flash('There is some error in sending the response to the outlet manager')
                return redirect(url_for('warehouse_notification'))
            flash('there is some server error for processing your response. Try again Later !!')
            return redirect(url_for('warehouse_notification'))
        return redirect(url_for('warehouse_notification'))
    flash('You are not logged in...')
    return redirect(url_for('warehouse_login'))

def reject_order():
    if 'user_id' in session:
        if  request.method == 'POST':
            requestid = request.form['requestid']
            sql = 'select outletId,productName from warehousenotification where requestId=%s'
            cur = getdbcur()
            cur.execute(sql,(requestid))
            n=cur.rowcount
            if n==1:
                data = cur.fetchone()
                outletId = str(data[0])
                productName = str(data[1])
                print(productName)
                warehouseId = session['user_id']
                fullkey = uuid.uuid4()
                responseId = fullkey.time
                result=request.form['reason']
                sql = 'insert into outletnotification values (%s,%s,%s,%s,%s,%s)'
                cur = getoutletcur()
                cur.execute(sql,(responseId,requestid,outletId,warehouseId,result,productName))
                n = cur.rowcount
                if n==1:
                    sql = 'delete from warehousenotification where requestId=%s'
                    cur = getdbcur()
                    cur.execute(sql,(requestid))
                    n = cur.rowcount
                    if n==1:
                        flash('Your order accept answer is send to the outlet manager')
                        return redirect(url_for('warehouse_notification'))
                    flash('There is some error in sending the response to the outlet manager')
                    return redirect(url_for('warehouse_notification'))
                flash('There is some error in sending the response to the outlet manager')
                return redirect(url_for('warehouse_notification'))
            flash('there is some server error for processing your response. Try again Later !!')
            return redirect(url_for('warehouse_notification'))
        return redirect(url_for('warehouse_notification'))
    flash('You are not logged in...')
    return redirect(url_for('warehouse_login'))


def outletnotification():
    if 'outlet_id' in session:
        outletId = session['outlet_id']
        if 'notifcountoutlet' in session:
            session.pop('notifcountoutlet',None)
        sql = 'select * from outletnotification where outletId=%s'
        cur = getoutletcur()
        cur.execute(sql,(outletId))
        n = cur.rowcount
        if n >= 1:
            notifications = cur.fetchall()
            return render_template('Outlet/outlet_notification.html',notifdata = notifications)
        flash('There is no notification for now')
        return render_template('Outlet/outlet_notification.html')
    flash('You are not logged in...')
    return redirect(url_for('outlet_login')) 


def deleteaccepted():
    if 'outlet_id' in session:
        if request.method == 'POST':
            respid = request.form['responseid']
            sql = 'delete from outletnotification where responseId=%s'
            cur = getoutletcur()
            cur.execute(sql,(respid))
            n = cur.rowcount
            if n==1:
                return redirect('outlet_notification')
            flash('Deletion Failed !!')
            return redirect('outlet_notification')
    flash('You are not logged in...')
    return redirect(url_for('outlet_login')) 

def deleterejected():
    if 'outlet_id' in session:
        if request.method == 'POST':
            respid = request.form['responseid']
            sql = 'delete from outletnotification where responseId=%s'
            cur = getoutletcur()
            cur.execute(sql,(respid))
            n = cur.rowcount
            if n==1:
                return redirect('outlet_notification')
            flash('Deletion Failed !!')
            return redirect('outlet_notification')
    flash('You are not logged in...')
    return redirect(url_for('outlet_login')) 
    
