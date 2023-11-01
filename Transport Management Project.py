import pandas as pd
import sqlalchemy as sqa1
import mysql.connector as mysq
import matplotlib.pyplot as py
import tkinter as t
import numpy as np
from PIL import ImageTk, Image

mycon=mysq.connect(host="localhost",user="root",passwd="1234",charset="utf8")
cursor=mycon.cursor()

cursor.execute("create database if not exists Transport")
cursor.execute("use Transport")

cursor.execute("""create table if not exists stud_master
                    (Reg_no integer primary key,
                     Sname varchar(30) not null,
                     Class integer not null,
                     Sec char(1) check(sec in ("A","B","C","D")),
                     Mob_no integer ,
                     Pickup_Point varchar(30) not null,
                     Bus_no integer(1) )""")

cursor.execute("""create table if not exists pickup_master
                    (id char(5) primary key,
                    Pickup_Point varchar(30) not null,
                    Bus_no integer(1) not null)""")

cursor.execute("""create table if not exists bus_master
                    (bus_reg_no char(4) primary key,
                    Bus_no int(1) not null,
                    Dname varchar(20) ,
                    Dmob_no int(10) not null,
                    Pickup_point1 varchar(10) not null,
                    T1 decimal(4) not null,
                    Pickup_point2 varchar(10) not null,
                    T2 decimal(4) not null,
                    Pickup_point3 varchar(10) ,
                    T3 decimal(4) ,
                    Pickup_point4 varchar(10) ,
                    T4 decimal(4) ,
                    Pickup_point5 varchar(10) ,
                    T5 decimal(4) )""")

cursor.execute("""create table if not exists login_master
                    (user_id char(5) primary key,
                    pwd char(4) not null,
                    name varchar(20) )""")

sqa2=sqa1.create_engine("mysql+mysqlconnector://root:1234@localhost/transport?charset=utf8")
sqa=sqa2.connect()

if pd.read_sql("select * from login_master",sqa).empty:
    dfstart=pd.DataFrame({"user_id":["admin"],"pwd":["abcd"],"name":["Aditi"]})
    dfstart.to_sql("login_master",index=False,con=sqa)
    
def subadmin():
    #ADMIN - ENTER USER-ID, PASSWORD
    who=1
    while who==1:
        us=input("Enter Your User_id - ")
        pwd=input("Enter Your Password - ")
        dfLe=pd.read_sql("select * from login_master where user_id = '%s'; " %(us,),sqa)
        if ( dfLe.empty or pwd != dfLe.pwd[0] ) :
            print("Wrong user-id/ password, Please Enter Again..!!")
            continue                                                             #asks to renter user_id and pwd as they are wrong 
        else:
            print("Welcome "+dfLe.name[0])
        temp6=input("Do you want to add admin? (y/n) - ")
        while temp6=="y":
            ui=input("New User-id - ")
            dfLae=pd.read_sql("select * from login_master where user_id='%s'; "%(ui,),sqa)
            if dfLae.empty:
                pwd=input("New Password - ")
                nm=input("New Name - ")
                dflog=pd.DataFrame({"user_id":[ui],"pwd":[pwd],"name":[nm]})
                dflog.to_sql("login_master",if_exists="append",index=False,con=sqa)
                break
            else:
                print("This user-id already exists !")
                continue
        bb=input("Do you want to go back ? (y/n) ")
        if bb=="yes" or bb=="y" :
            break                                                                 #asks admin or user as want to go back from admin
        
        #STUDENT OR BUS
        condn2="y"
        while condn2=="y" and who==1:
            print("1.Student Store \n2.Bus Store \n3.Back ")
            ch=int(input("What do you want to change (1 or 2) ? "))
            
            #BACK - ADMIN WANTS TO CHANGE USER-ID
            if ch==3:
                break                                                           #asks to renter user_id and pwd as want to go back as admin

            #NEITHER OF THREE - CHOOSE AGAIN - STUDENT OR BUS
            elif ch not in [1,2]:
                print("Invalid Choice selected, Try Again...!!")
                continue                                                        #asks for admin, user..

            #ADMIN CHANGES IN STUDENT STORE
            elif ch==1:
                while condn2=="y" and ch==1:
                    
                    #ADD/UPDATE/DELETE/VIEW
                    print("1.Add \n2.Update \n3.Delete \n4.View \n5.Back")
                    op=int(input("What do you want to do ? "))
                    
                    #BACK - ADMIN WANTS TO MAKE CHANGES IN BUS INSTEAD OF STUDENT OR ADMIN WANTS TO GO BACK
                    if op==5:
                        break

                    #NEITHER OF FIVE - CHOOSE AGAIN - ADD/UPDATE/DELETE/VIEW
                    elif op not in [1,2,3,4]:
                        print("Invalid Choice selected, Try Again...!!")
                        continue                                                    #asks for add, update..

                    #ADD A STUDENT BY ADMIN (as)
                    condn8="y"
                    while op==1 and condn8=="y":
                        asr=int(input("Reg_no. - "))
                        dftemp2=pd.read_sql("select reg_no from stud_master where reg_no = %s;"%(asr,),sqa)
                        if dftemp2.empty:
                            asn=input("Student Name - ")
                            asc=int(input("Class - "))   # class bw 0 n 12
                            ass=input("Section - ")
                            condn13="y"
                            count1=0
                            while condn13=="y" :
                                if count1<1:
                                    asm=input("Mobile No. - ")
                                    if len(asm)==10:
                                        condn14="y"
                                        while condn14=="y":
                                            asp=input("Pickup Point - ")                                    
                                            dfPas = pd.read_sql("select * from pickup_master where pickup_point ='%s' ;" %(asp,) ,sqa)
                                            if dfPas.empty :
                                                print("Pickup Point ",asp," is not available")
                                                continue
                                            else:
                                                var=0
                                                for i in dfPas.Bus_no:
                                                    dftemp7=pd.read_sql("select count(*) from stud_master where Bus_no=%s;"%(i,),sqa).iat[0,0]
                                                    if dftemp7<pd.read_sql("select Capacity from bus_master where Bus_no=%s;"%(i,),sqa).iat[0,0]:
                                                        var=1
                                                        varb=i
                                                if var==0:
                                                    print("For this Pickup Point all buses are full")
                                                    condn16=input("Do you want to add more student(m) or same student(s) or go back(b)")
                                                    if condn16=="s":
                                                        continue
                                                    elif condn16=="m":
                                                        condn13="n"
                                                        break
                                                    elif condn16=="b":
                                                        condn13="n"
                                                        condn8="n"
                                                        break
                                                else:
                                                    asb=varb
                                                    dfas=pd.DataFrame({"Reg_no":[asr],"Sname":[asn],"Class":[asc],"Sec":[ass],"Mob_no":[asm],"Pickup_Point":[asp],"Bus_no":[asb]})
                                                    dfas.to_sql("stud_master",if_exists="append",index=False,con=sqa)
                                                    print("Reg. no. ",asr," is successfully added !")
                                                    condn8=input("Do you want to add more student? (y/n)")
                                                    count1=1
                                                    break
                                    else:
                                        print(asm," Mobile No. is Incorrect")
                                        continue
                                else:
                                    break
                        else:
                            print("Registeration Number ",asr," already exists !!")
                            condn15=input("Do you want to add more student? (y/n)")
                            if condn15!="y":
                                break
                            
                    #UPDATE A STUDENT BY ADMIN (us)                    
                    while op==2 :
                        usr=int(input("Reg_no. - "))
                        dfSus = pd.read_sql("select * from stud_master where reg_no=%s ;"%(usr,) ,sqa)
                        if dfSus.empty :
                            print("Registration Number ",usr," is not available")
                            continue
                        else:
                            print("Name - ", dfSus.Sname[0])
                            print("Class - ", dfSus.Class[0])
                            print("Section - ", dfSus.Sec[0])
                            print("Old Pickup_Point - ", dfSus.Pickup_Point[0])
                            print("Available Pickup Points :-")
                            print(pd.read_sql("select Pickup_Point from pickup_master",sqa))
                            condn6="s"
                            while op==2 and condn6=="s":
                                usp=input("New Pickup Point - ")                                 
                                usqry1="select * from pickup_master where pickup_point ='%s' ;" %(usp,)
                                dfPus = pd.read_sql(usqry1,sqa)
                                if dfPus.empty :
                                    print("New Pickup Point ",usp," is not available")
                                    continue
                                else:
                                    usb=dfPus.Bus_no[0]                                                   
                                    if pd.read_sql("select capacity from bus_master where bus_no = %s ;" %(usb,),sqa).iat[0,0] == pd.read_sql("select count(*) from stud_master where bus_no = %s ;" %(usb,),sqa).iat[0,0]:
                                        print("This bus has no capacity")
                                        continue
                                    else:                       
                                        df2us=pd.DataFrame({"Reg_no":[usr],"Sname":dfSus.Sname[0],"Class":dfSus.Class[0],"Sec":dfSus.Sec[0],"Mob_no":dfSus.Mob_no[0],"Pickup_Point":[usp],"Bus_no":[usb]})
                                        dfS1us = pd.read_sql("select * from stud_master ;" ,sqa)
                                        usc=0
                                        for i in range (len(dfS1us)) :
                                            if dfS1us.Reg_no[usc]==usr:
                                                break
                                            usc=usc+1                                                       #c is row no. which is needed to be changed
                                        df1us=dfS1us[0:usc]
                                        df3us=dfS1us[usc+1:]
                                        dfSnewus=pd.concat([df1us,df2us,df3us],ignore_index=True)
                                        dfSnewus.to_sql("stud_master",if_exists="replace",index=False,con=sqa)
                                        print("Reg. no. ",usr," is successfully updated !")
                                        print("Your new bus no. is ",usb)
                                        condn7=input("Do you want to go continue? (y/n)")
                                        if condn7 =="y":
                                            condn6=input("Do you want to update pickup point of more students(m) or same student(s) - ")
                                        else:
                                            op=0
                                            break
                                        
                    #REMOVE A STUDENT BY ADMIN (rs)
                    condn9="y"
                    while op==3 and condn9=="y":
                        rsr=int(input("Reg_no of student who left the school - "))
                        dftempor=pd.read_sql("Select * from stud_master where reg_no=%s;"%(rsr,),sqa)
                        if dftempor.empty:
                            print("Registeration no. ",rsr," is not available")
                            continue
                        else:
                            print("Name - ",dftempor.Sname[0])
                            print("Class - ",dftempor.Class[0])
                            print("Section- ",dftempor.Sec[0])
                            condn10=input("Are you sure want to delete? (y/n)")
                            if condn10 =="n":
                                break
                            else:
                                dfS1rs = pd.read_sql("select * from stud_master ;" ,sqa)
                                rsc=0
                                for i in range(len(dfS1rs)) :
                                    if dfS1rs.Reg_no[rsc]==rsr:
                                        break
                                    rsc=rsc+1                                                               #c is row no. which is needed to be deleted
                                df1rs=dfS1rs[0:rsc]
                                df3rs=dfS1rs[rsc+1:]
                                dfSnewrs=pd.concat([df1rs,df3rs],ignore_index=True)
                                print(dfSnewrs)
                                dfSnewrs.to_sql("stud_master",if_exists="replace",index=False,con=sqa)
                                print("Reg. no. ",rsr," successfully removed !")
                                condn9=input("Do you want to remove more student? (y/n)")
                                
                    #VIEW STUDENT BY ADMIN (vs)
                    while op==4:
                        dfS1vs1 = pd.read_sql("select * from stud_master ;" ,sqa)
                        dfS1vs=pd.DataFrame(dfS1vs1.sort_values(by="Reg_no"))
                        dfS1vs.index=np.arange(len(dfS1vs1))
                        print(dfS1vs)
                        break       
        
            #ADMIN CHANGES IN BUS STORE     
            elif ch==2:
                while condn2=="y" and who==1:                           
                    print("1.Add \n2.Update \n3.Delete \n4.View \n5.Back")
                    op=int(input("What do you want to do ? "))

                    #ADMIN WANTS TO MAKE CHANGES IN STUDENT OR WANTS TO GO BACK
                    if op==5:
                        break                                                                       #asks for user-id,pwd

                    #NEITHER OF FIVE - CHOOSE AGAIN - ADD/UPDATE/DELETE/VIEW
                    elif op not in [1,2,3,4]:
                        print("Invalid Choice selected, Try Again...!!")
                        continue                                                                    #asks for add, update..

                    #ADD A BUS BY ADMIN (ab)
                    while op==1:
                        br=input("bus reg_no. - ")
                        dftemp5 = pd.read_sql("select * from bus_master ",sqa)
                        if br in dftemp5.bus_reg_no:
                            print("Bus Reg. no. ",br," already exists")
                            continue
                        else:
                            condn20="y"
                            while op==1 and condn20=="y":
                                bn=input("bus no - ")
                                if bn in dftemp5.Bus_no:
                                    print("Bus no. ",bn," already exists")
                                    continue
                                else:
                                    dn=input("Driver name - ")
                                    condn21="y"
                                    while op==1 and condn21=="y":
                                        dm=int(input("Driver mobile no. - "))
                                        if len(str(dm))!=10:
                                            print("Please enter correct mobile no.")
                                            continue
                                        else:
                                            cap=int(input("Capacity - "))
                                            p1=input("Pickup Point 1 - ")
                                            t1=float(input("Time 1 - "))
                                            p2=input("Pickup Point 2 - ")
                                            t2=float(input("Time 2 - "))
                                            p3=input("Pickup Point 3- ")
                                            t3=float(input("Time 3 - "))
                                            p4=input("Pickup Point 4- ")
                                            t4=float(input("Time 4 - "))
                                            p5=input("Pickup Point 5- ")
                                            t5=float(input("Time 5 - "))
                                            abl=[p1,p2,p3,p4,p5]
                                            for i in range(len(abl)):
                                                if abl[i]=='':
                                                    abl[i]=np.NaN
                                            dfab=pd.DataFrame({"bus_reg_no":[br],"Bus_no":[bn],"Dname":[dn],"Dmob_no":[dm],\
                                                             "pickup_point1":[p1],"T1":[t1],"pickup_point2":[p2],\
                                                             "T2":[t2],"pickup_point3":[p3],"T3":[t3],"pickup_point4":[p4],\
                                                             "T4":[t4],"pickup_point5":[p5],"T5":[t5],"Capacity":[cap]})                                                                                                                                    
                                            print(dfab)                                                                               
                                            dfab.to_sql("bus_master",if_exists="append",index=False,con=sqa)
                                            op=0
                                            print("Bus with reg. no. ",br," is successfully added")
                                            break
                                        

                    #UPDATE A BUS BY ADMIN (ub)
                    condn11="y"
                    while op==2 and condn11=="y":
                        actcap=[]
                        dftemp3=pd.read_sql("select * from bus_master",sqa)
                        for i in range (len(dftemp3)):
                            dftemp4=pd.read_sql("select count(*) from stud_master where Bus_no=%s"%(dftemp3.Bus_no[i],),sqa)
                            if dftemp4.iat[0,0]==0:
                                actcap.append(0)
                        if 0 in actcap:
                            br=input("Bus Reg no. - ")
                            dfSub = pd.read_sql("select * from bus_master where bus_reg_no='%s' ;"%(br,) ,sqa)
                            if dfSub.empty:
                                print("Bus Registeration Number ",br," is not available")
                                continue
                            else:
                                print("Bus no. - ",dfSub.Bus_no[0])
                                print("Name of Driver - ",dfSub.Dname[0])
                                tempP=pd.read_sql("select Pickup_Point from pickup_master where Bus_no=%s;"%(dfSub.Bus_no[0],),sqa)
                                print("Old Pickup Points-")
                                for i in tempP.Pickup_Point:
                                    print(i)
                                tempub=(pd.read_sql("select count(*) from stud_master where Bus_no=%s"%(dfSub.Bus_no[0],),sqa)).iat[0,0]
                                while tempub==0:
                                    nn=int(input("how many pickup points you want to change? (max=5)"))
                                    if 0<=nn<=5:
                                        l,tt=[],[]
                                        for i in range (nn):
                                            npub=input("New Pickup Point - ")
                                            nt=float(input("New timings - "))
                                            l.append(npub)
                                            tt.append(nt)
                                        c=len(l)-5
                                        
                                        dfPub=pd.read_sql("select * from pickup_master;",sqa)
                                        for i in range(len(dfPub)):
                                            if dfPub.Bus_no[i]==dfSub.Bus_no[0]:
                                                dfPub.Pickup_Point=dfPub.Pickup_Point.replace([dfPub.Pickup_Point[i]],np.NaN)
                                        dfPub=dfPub.dropna()
                                        ltemp1,ltemp2,ltemp3=[],[],[]
                                        for i in range(nn):
                                            ltemp1.append(int(dfPub.id[len(dfPub)-1])+i+1)
                                            ltemp2.append(l[i])
                                            ltemp3.append(dfSub.Bus_no[0])
                                        
                                        dfP1ub=pd.DataFrame({"id":ltemp1,"Pickup_Point":ltemp2,"Bus_no":ltemp3})
                                        dfPnewub=pd.concat([dfPub,dfP1ub])                                                
                                        dfPnewub.to_sql("pickup_master",if_exists="replace",index=False,con=sqa)
        
                                        for i in range(c,0):
                                            tt.append(np.NaN)
                                            l.append(np.NaN)
                                        dfS1ub = pd.read_sql("select * from bus_master ;" ,sqa)
                                        df2ub=pd.DataFrame({"bus_reg_no":dfSub.bus_reg_no[0],"Bus_no":dfSub.Bus_no[0],"Dname":dfSub.Dname[0],\
                                                          "Dmob_no":dfSub.Dmob_no[0],"pickup_point1":[l[0]],"T1":[tt[0]],"pickup_point2":[l[1]],\
                                                          "T2":[tt[1]],"pickup_point3":[l[2]],"T3":[tt[2]],"pickup_point4":[l[3]],\
                                                          "T4":[tt[3]],"pickup_point5":[l[4]],"T5":[tt[4]],"Capacity":dfSub.Capacity[0]})
                                        cub=0
                                        for i in range (len(dfS1ub)) :
                                            if dfS1ub.bus_reg_no[i]==br :
                                                break
                                            cub=cub+1                                                                           
                                        df1ub=dfS1ub[0:cub]
                                        df3ub=dfS1ub[cub+1:]
                                        dfSnewub=pd.concat([df1ub,df2ub,df3ub],ignore_index=True)
                                        
                                        dfSnewub.to_sql("bus_master",if_exists="replace",index=False,con=sqa)
                                        condn11=input("Do you want to continue? (y/n)")
                                        break
                                    else:
                                        print(nn," Pickup points are not available")
                                        continue
                                if tempub!=0:
                                    print("You can't change Pickup Points of Bus no. ",dfSub.Bus_no[0]," as there are already students in this bus")
                                    continue
                        else:
                            print("All the buses already have students so you can't update a bus")
                            break

                    #REMOVE A BUS BY ADMIN (rb)
                    condn12="y"
                    while op==3 and condn12=="y":
                        actcap=[]
                        dfS1rb = pd.read_sql("select * from bus_master ;" ,sqa)
                        for i in range (len(dfS1rb)):
                            dftemp4=pd.read_sql("select count(*) from stud_master where Bus_no=%s"%(dfS1rb.Bus_no[i],),sqa)
                            if dftemp4.iat[0,0]==0:
                                actcap.append(0)
                        if 0 in actcap:
                            brrb=input("Bus Reg no. of bus which is to be removed - ")
                            
                            crb=0
                            for i in range(len(dfS1rb)) :
                                if dfS1rb.bus_reg_no[crb]==brrb :
                                    break
                                crb=crb+1                                                                           #c is row no. which is needed to be deleted
                            if crb==len(dfS1rb):
                                print("Bus Registeration Number ",brrb," is not available")
                                continue
                            else:
                                temprb=(pd.read_sql("select count(*) from stud_master where Bus_no=%s"%(dfS1rb.Bus_no[crb],),sqa)).iat[0,0]
                                if temprb==0:
                                    print("Bus no. - ",dfS1rb.Bus_no[crb])
                                    print("Name of Driver - ",dfS1rb.Dname[crb])
                                    df1rb=dfS1rb[0:crb]
                                    df3rb=dfS1rb[crb+1:]
                                    dfSnewrb=pd.concat([df1rb,df3rb],ignore_index=True)
                                    print(dfSnewrb)
                                    dfSnewrb.to_sql("bus_master",if_exists="replace",index=False,con=sqa)
                                    print("Bus with reg. no. ",brrb," has been removed successfully")
                                    condn12=input("Do you want to continue? (y/n) - ")
                                else:
                                    print("You can't delete Bus no. ",dfS1rb.Bus_no[crb]," as there are already students in this bus")
                                    continue
                        else:
                            print("All the buses already have students so you can't delete a bus")
                            break

                    #VIEW BUS TABLE BY ADMIN (vb)
                    while op==4:
                        dfS1vb = pd.read_sql("select * from bus_master ;" ,sqa)
                        print(dfS1vb)
                        break
        


def subuser():
    #USER - CHOOSE REPORT OR GO BACK
    cu=0
    who=2
    while condn5=="u":
        cu=cu+1
        if cu>1:
            print("Welcome Again User")
        else:
            print("Welcome User")
        print("1. Route wise report")
        print("2. Student wise report")
        print("3. Bus_no. v/s active capacity")
        print("4. Back")
        opt=int(input("Enter Choice :- "))

        #USER WANTS TO GO BACK AND CHOOSE ADMIN INSTEAD OF USER OR USER WANTS TO EXIT
        if opt == 4:
            condn2="n"
            break

        #USER CHOOSE NEITHER OF THREE - CHOOSE AGAIN - REPORTS
        elif opt not in [1,2,3,4]:
            print("Invalid Choice selected, Try Again...!!")
            continue

        #USER WANTS TO SEE ROUTES OF BUSES
        while opt==1:
            print("1.Route of one bus \n2.Route of selective buses \n3.Back")
            rchoice=int(input("Route display choice - "))

            #USER WANTS TO GO BACK AND DISPLAY DIFFERENT REPORT OR WANT TO GO BACK
            if rchoice == 3:
                break

            #USER CHOOSE NEITHER OF TWO - CHOOSE AGAIN - SINGLE OR MULTIPLE BUSES
            elif rchoice not in [1,2]:
                print("Invalid Choice selected, Try Again...!!")
                continue
            condn3="yes"
            ss1,x,y=[],[],[]
            while condn3=="yes" or condn3=='y':          # 5th while
                ss=input("Which bus's route you want to see? Enter its Bus Reg. no.- ")
                qx1="select ifnull(pickup_point1,'') as 'PP1',ifnull(pickup_point2,'') as 'PP2',ifnull(pickup_point3,'') as 'PP3',ifnull(pickup_point4,'') as 'PP4',ifnull(pickup_point5,'') as 'PP5' from bus_master where bus_reg_no=%s;"
                dfx1=pd.read_sql(qx1,sqa,params=[ss])
                if dfx1.empty:  
                    print("Bus Registeration Number ",ss," is not available")
                    continue
                else:
                    qy1="select ifnull(T1,0) as 'T1',ifnull(T2,0) AS 'T2',ifnull(T3,0) AS 'T3',ifnull(T4,0) AS 'T4',ifnull(T5,0) AS 'T5' from bus_master where bus_reg_no =%s ;"
                    dfy1=pd.read_sql(qy1,sqa,params=[ss])
                    ss1.append((pd.read_sql("select bus_no from bus_master where bus_reg_no='%s';"%(ss,),sqa)).iat[0,0])
                    ssx=list(dfx1.values[0])
                    ssy=list(dfy1.values[0])
                    c=0
                    for i in ssx:
                        if i=='':
                            c=c+1
                    if c>0:
                        for i in range(c):
                            ssx.remove('')
                            ssy.remove(0)
                    ssx.append("St. Anne's School")
                    ssy.append(7.45)
                    x.append(ssx)
                    y.append(ssy)
                    if rchoice==1:
                        condn3="no"
                    elif rchoice==2:
                        condn3=input("Do you want to continue? ")
            xtick1=[]
            for i in range (len(ss1)):
                py.plot(y[i],x[i],label=ss1[i],marker="o")
                py.legend()
                py.title("Route-wise Report")
                py.xlabel("Pickup Points")
                py.ylabel("Timings")
                for j in y[i]:
                    xtick1.append(j)
            py.xticks(xtick1)    
            py.show()

        #USER WANTS TO SEE NO. OF STUDENTS BOARDING AT PARTICULAR PICKUP POINT
        while opt==2:
            print("1.class wise no. of students verses pickup points")
            print("2.Bus wise pickup points verses no. of students")
            print("3.No. of students verses all pickiup points")
            print("4.Back")
            choice=int(input("Display Choice - "))

            #USER WANTS TO GO BACK AND DISPLAY DIFFERENT REPORT OR WANT TO GO BACK
            if choice == 4:
                break

            #USER CHOOSE NEITHER OF FOUR - CHOOSE AGAIN 
            elif choice not in [1,2,3]:
                print("Invalid Choice selected, Try Again...!!")
                continue
            labe,x,y=[],[],[]
            condn4="y"
            while condn4=="y" and choice==1:  #6th while
                ss=[]
                clas=int(input("Class - "))
                dftemp=pd.read_sql( "select count(*) from stud_master where class=%s;"%(clas,), sqa)
                if dftemp.iat[0,0]==0:
                    print("Class ",clas," is not available")
                    continue
                else:
                    df1=pd.read_sql( "select Pickup_Point from pickup_master", sqa)
                    condn4=input("Do you want to continue? (y/n) ")
                    x.append(df1.T.values[0])
                    labe.append(clas)
                for i in df1.Pickup_Point:
                    df2=pd.read_sql( "select count(*) from stud_master where Pickup_Point = '%s' and class=%s;"%(i,clas), sqa)
                    ss.append(df2.iat[0,0])
                y.append(ss)
            while condn4=="y" and choice==2:
                ss=[]
                busn=int(input("Bus no.- "))
                df1=pd.read_sql( "select Pickup_Point from pickup_master where bus_no = %s"%(busn,), sqa)
                if df1.empty:
                    print("Bus Number ",busn," is not available")
                    continue
                else:
                    condn4=input("Do you want to continue? (y/n) ")
                    x.append(list(df1.T.values[0]))
                    labe.append(busn)
                for i in df1.Pickup_Point:
                    df2=pd.read_sql( "select count(*) from stud_master where Pickup_Point = '%s';"%(i,), sqa)
                    ss.append(df2.iat[0,0])
                y.append(ss)
            while condn4=="y" and choice==3:
                ss=[]
                df1=pd.read_sql( "select Pickup_Point from pickup_master", sqa)
                condn4="n"
                x=list(df1.T.values[0])
                for i in df1.Pickup_Point:
                    df2=pd.read_sql( "select count(*) from stud_master where Pickup_Point = '%s';"%(i,), sqa)
                    y.append(df2.iat[0,0])
            if choice in [1,2]:
                for i in range (len(labe)):
                    py.barh(x[i],y[i],label=labe[i])
                    py.legend()
                    py.title("Student-wise Report")
                    py.ylabel("Pickup Points")
                    py.xlabel("No. of students ")
                    py.xticks(y[i])
                py.show()
            elif choice==3:
                py.barh(x,y)
                py.title("Student-wise Report")
                py.ylabel("Pickup Points")
                py.xlabel("No. of students ")
                py.xticks(y)
                py.show()

        #USER WANTS TO CHECK HOW MUCH CAPACITY IS THERE IN EACH BUS
        x,y=[],[]
        ucapch="y"
        while opt==3 and ucapch=="y":
            bncap=int(input("Bus no. - "))
            dfScap=pd.read_sql("select count(*) from stud_master where bus_no=%s;"%(bncap,),sqa)
            dfBcap=pd.read_sql("select Capacity from bus_master where bus_no=%s;"%(bncap,),sqa)
            if dfBcap.empty:
                print("Invalid Choice Chosen, Enter Again !!...")
                continue
            elif "Bus no. "+str(bncap) in y:
                print("Bus no. ",bncap," is repeated, Enter Again !!..")
                continue
            else:
                temp7=dfBcap.iat[0,0]-dfScap.iat[0,0]
                x.append(temp7)
                y.append("Bus no. "+str(bncap))
                ucapch=input("Do you want to continue? (y/n) - ")
        if ucapch=="n":
            py.pie(x,labels=y,autopct="%5.2f%%")
            py.title("Bus no. verses Active Capacity")
            py.show()
            

condn1="y"
condn5="u"
    
start=t.Tk()
start.title("Transport Management System")

img=Image.open("school bus transport pic.jpg")
img=img.resize((1350,450),Image.ANTIALIAS)
img=ImageTk.PhotoImage(img)

t.Label(start,text="Welcome to Transport Management",font=("Arial",40)).pack()
t.Label(start,image=img).pack()

badmin=t.Button(start,text="Admin",command=subadmin,height=1,width=20,font=("Arial",20))
buser=t.Button(start,text="User",command=subuser,height=1,width=20,font=("Arial",20))
bexit=t.Button(start,text="Exit",command=lambda start=start:quit(start),height=1,width=20,font=("Arial",20))
badmin.pack()
buser.pack()
bexit.pack()

start.geometry('1400x1100')
start.mainloop()
