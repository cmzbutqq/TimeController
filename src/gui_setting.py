
"""
这个文件是用户与json交互的gui
"""
import tkinter as tk
import json
from tkinter import ttk
from tkinter import messagebox
import user_json_path
def setting():
    with open(user_json_path.user_json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    combobox_lockers_values=[]
    combobox_count_tasks_values=[]
    combobox_timer_tasks_values=[]

    def make_values():
        if len(data["lockers"])!=0:
            for i in range(0,len(data["lockers"])):
                combobox_lockers_values.append(data["lockers"][i]["name"])
        if len(data["count_tasks"])!=0:
            for i in range(0,len(data["count_tasks"])):
                combobox_count_tasks_values.append(f"id:{data["count_tasks"][i]["id"]} {data["count_tasks"][i]["name"]}")
        if len(data["timer_tasks"])!=0:
            for i in range(0,len(data["timer_tasks"])):
                combobox_timer_tasks_values.append(f"id:{data["timer_tasks"][i]["id"]} {data["timer_tasks"][i]["name"]}")
        combobox_lockers_values.append("新建")
        combobox_count_tasks_values.append("新建")
        combobox_timer_tasks_values.append("新建")
    make_values()


    """
    命名规则
    窗口： window_xx   如果yy是在xx上的window命名为window_xx_yy
    组件： 组件名_作用
    
    希望从edit_xx函数中保留的值如果使用StringVar(),统一使用get_aa这种形势命名
    """


    #lockers_button函数
    def edit_lockers():
        ##一级小窗创建
        window_lockers=tk.Toplevel()
        window_lockers.title("lockers")
        window_lockers.geometry("500x500")

        ##框内文字引用与预设列表
        get_time_rules=[]
        get_list=[]
        if lockers_state.get()=="新建":
            get_lockers_ifon=tk.StringVar(value="off")
            get_lockers_name=tk.StringVar(value="")
            get_lockers_punish=tk.StringVar(value="DEBUG")
            get_lockers_type=tk.StringVar(value="WHITELIST")
            get_list=["WHITE","BLACK"]
        else:
            for i in range(0,len(data["lockers"])):
                if data["lockers"][i]["name"]==lockers_state.get():              ###特别注意：不同lockers之间不能重名，sure_locker前需要检查并且错误弹窗
                    index=i
            if data["lockers"][index]["on"]:
                ifon="on"
            else:
                ifon="off"
            get_lockers_ifon = tk.StringVar(value=ifon)
            get_lockers_name = tk.StringVar(value=data["lockers"][index]["name"])
            get_lockers_punish = tk.StringVar(value=data["lockers"][index]["punish"])
            get_lockers_type = tk.StringVar(value=data["lockers"][index]["list_type"])
            for i in data["lockers"][index]["list"]:
                get_list.append(i)
            for i in data["lockers"][index]["time_rules"]:
                get_time_rules.append(i)

        ##ifon函数
        def ifon():
            if get_lockers_ifon.get()=="on":
                get_lockers_ifon.set("off")
            else:
                get_lockers_ifon.set("on")

        ##edit_list函数(完工)
        def edit_list():
            ###新建二级小窗
            counter=1

            window_lockers_list=tk.Toplevel()
            window_lockers_list.title("lockers_编辑名单(最多18条)")
            window_lockers_list.geometry("700x750")
            frame=tk.Frame(window_lockers_list)
            frame2=tk.Frame(window_lockers_list)
            frame3=tk.Frame(window_lockers_list)
            frame.place(x=0,y=50)#待调数值
            frame2.place(x=200,y=50)
            frame3.place(x=400,y=50)
            get_lockers_list_list=[]

            def add_list(i=""):
                nonlocal counter
                f=get_frame(counter)
                new_entry_text=tk.StringVar(value=i)
                new_entry=tk.Entry(f,textvariable=new_entry_text)
                new_entry.pack(side="top",fill="x",padx=10,pady=5)
                new_button_sure=tk.Button(f,text="确认",command=lambda:sure_this_list(new_entry_text))
                new_button=tk.Button(f,text="删除",command=lambda:remove_entry_and_button(new_entry,new_button,new_button_sure,new_entry_text))
                new_button.pack(side="top", fill="x", padx=10, pady=5)
                new_button_sure.pack(side="top", fill="x", padx=10, pady=5)
                if i!="":
                    sure_this_list(new_entry_text)
                counter+=1
            def get_frame(counter):
                if counter<=6:
                    return frame
                elif counter>6 and counter<=12:
                    return frame2
                elif counter>12 and counter<=18:
                    return frame3
            def sure_this_list(new_entry_text):
                get_lockers_list_list.append(new_entry_text.get())
            def remove_entry_and_button(entry,button,button_sure,new_entry_text):
                nonlocal counter
                counter-=1
                if new_entry_text.get() in get_lockers_list_list:
                    get_lockers_list_list.remove(new_entry_text.get())
                entry.destroy()
                button.destroy()
                button_sure.destroy()


            for i in get_list:
                add_list(i)

            def sure_lockers_list():
                for i in get_lockers_list_list:
                    if i not in get_list and i!='':
                        get_list.append(i)
                remove_list=[]
                for i in get_list:
                    if i not in get_lockers_list_list:
                        remove_list.append(i)
                for i in remove_list:
                    get_list.remove(i)
                print(get_list)
                window_lockers_list.destroy()
            button_add=tk.Button(window_lockers_list,text="新增",command=add_list)
            button_add.place(x=0,y=0)
            button_sure_lockers_list=tk.Button(window_lockers_list,text="确定",command=sure_lockers_list)
            button_sure_lockers_list.place(x=50,y=0)


        ##edit_timer_rules函数(完工)
        def edit_time_rulers():
            counter=1
            window_lockers_time_rules=tk.Toplevel()
            window_lockers_time_rules.title("lockers_设置时间(最多两条)")
            window_lockers_time_rules.geometry("700x750")
            frame=tk.Frame(window_lockers_time_rules)
            frame.place(x=0,y=50)
            get_time_rules_m=[]

            def add_rules(i=None):
                if i==None:
                    i = {"start_time": "", "end_time": "", "days": [""]}
                nonlocal counter
                start_time=tk.StringVar(value=i["start_time"])
                end_time=tk.StringVar(value=i["end_time"])
                days=tk.StringVar(value=i["days"][0])
                label_start_time=tk.Label(frame,text="开始时间")
                combobox_start_time=ttk.Combobox(frame,values=["示范： 06：00（24小时计时法）"],textvariable=start_time)
                label_end_time=tk.Label(frame,text="结束时间")
                combobox_end_time=ttk.Combobox(frame,values=["示范： 23：30"],textvariable=end_time)
                label_days=tk.Label(frame,text="日期")
                combobox_days=ttk.Combobox(frame,values=["说明：","请输入预设的时间集","可以在presets中预设时间集"],textvariable=days)
                button_sure_this_rule=tk.Button(frame,text="确认",command=lambda:sure_this_rule(start_time,end_time,days))
                button_delete_this_rule=tk.Button(frame,text="删除",command=lambda:remove_object(label_start_time,label_end_time,label_days,combobox_start_time,combobox_end_time,combobox_days,button_sure_this_rule,button_delete_this_rule,start_time,end_time,days))

                if i!={"start_time": "", "end_time": "", "days": [""]}:
                    sure_this_rule(start_time, end_time, days)

                label_start_time.pack(side="top",fill="x",padx=10,pady=5)
                combobox_start_time.pack(side="top",fill="x",padx=10,pady=5)
                label_end_time.pack(side="top",fill="x",padx=10,pady=5)
                combobox_end_time.pack(side="top",fill="x",padx=10,pady=5)
                label_days.pack(side="top",fill="x",padx=10,pady=5)
                combobox_days.pack(side="top",fill="x",padx=10,pady=5)
                button_sure_this_rule.pack(side="top", fill="x", padx=10, pady=5)
                button_delete_this_rule.pack(side="top", fill="x", padx=10, pady=5)

            def sure_this_rule(start_time,end_time,days):
                get_time_rules_m.append({"start_time":f"{start_time.get()}","end_time": f"{end_time.get()}","days":[f"{days.get()}"]})

            def remove_object(label1,label2,label3,box1,box2,box3,button1,button2,start,end,d):
                nonlocal counter
                counter-=1
                if {"start_time":f"{start.get()}","end_time": f"{end.get()}","days":[f"{d.get()}"]} in get_time_rules_m:
                    get_time_rules_m.remove({"start_time":f"{start.get()}","end_time": f"{end.get()}","days":[f"{d.get()}"]})
                label1.destroy()
                label2.destroy()
                box1.destroy()
                box2.destroy()
                box3.destroy()
                button1.destroy()
                button2.destroy()
                label3.destroy()
            for i in get_time_rules:
                add_rules(i)

            def sure_time_rules():
                for i in get_time_rules_m:
                    if i not in get_time_rules and i!={"start_time":"","end_time": "","days":[""]}:
                        get_time_rules.append(i)
                remove_list=[]
                for i in get_time_rules:
                    if i not in get_time_rules_m:
                        remove_list.append(i)
                for i in remove_list:
                    get_time_rules.remove(i)
                print(get_time_rules)
                window_lockers_time_rules.destroy()
            button_add=tk.Button(window_lockers_time_rules,text="新增",command=add_rules)
            button_add.place(x=0,y=0)
            button_sure_time_rules=tk.Button(window_lockers_time_rules,text="完成",command=sure_time_rules)
            button_sure_time_rules.place(x=50,y=0)


        ##sure_lockers函数
        def sure_lockers():
            locker_data = {
                "name": get_lockers_name.get(),
                "on": get_lockers_ifon.get() == "on",
                "punish": get_lockers_punish.get(),
                "list_type": get_lockers_type.get(),
                "list": get_list,
                "time_rules": get_time_rules
            }
            rename=False
            if lockers_state.get()=="新建":
                for i in data["lockers"]:
                    if i["name"]==get_lockers_name.get():
                        rename=True
            else:
                for i in data["lockers"]:
                    if i["name"]==get_lockers_name.get() and i!=data["lockers"][index]:
                        rename=True
            if rename:
                messagebox.showerror('错误', '项目重名，请更改名字')
                return

            noname=(locker_data["name"]=="")
            if noname:
                messagebox.showerror('错误', '不可无名，请为项目取名')
                return

            # 如果是“新建”，添加新项目；否则更新现有项目
            if lockers_state.get() == "新建":
                data["lockers"].append(locker_data)                        ##写进data
                combobox_lockers_values.remove("新建")
                combobox_lockers_values.append(locker_data["name"])
                combobox_lockers_values.append("新建")
                combobox_lockers.config(values=combobox_lockers_values)     ##更新下拉列表
            else:
                combobox_lockers_values.remove("新建")
                combobox_lockers_values.remove(data["lockers"][index]["name"])
                data["lockers"][index] = locker_data
                combobox_lockers_values.append(data["lockers"][index]["name"])
                combobox_lockers_values.append("新建")
                combobox_lockers.config(values=combobox_lockers_values)
            # 将更新后的数据写入 JSON 文件
            with open(user_json_path.user_json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            window_lockers.destroy()

        def delete_lockers():
            if lockers_state.get()=="新建":
                messagebox.showerror('错误', '新建项目不可以删除')
            else:
                make_sure=messagebox.askokcancel('删除', '确认删除吗')
                if make_sure:
                    combobox_lockers_values.remove(data["lockers"][index]["name"])
                    combobox_lockers.config(values=combobox_lockers_values)
                    data["lockers"].remove(data["lockers"][index])
                    window_lockers.destroy()
                    with open(user_json_path.user_json_path, "w", encoding="utf-8") as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)



        ##一级小窗设置与布局
        label_name=tk.Label(window_lockers,text="名字： ")
        label_ifon=tk.Label(window_lockers,text="状态： ")
        label_punish=tk.Label(window_lockers,text="惩罚： ")
        label_type=tk.Label(window_lockers,text="名单类型： ")

        label_name.place(x=0,y=0)
        label_ifon.place(x=0,y=100)
        label_punish.place(x=0,y=200)
        label_type.place(x=0,y=300)

        entry_name=tk.Entry(window_lockers,textvariable=get_lockers_name ,width=50)
        button_ifon=tk.Button(window_lockers,width=50,command=ifon,textvariable=get_lockers_ifon)
        combobox_punish = ttk.Combobox(window_lockers, textvariable=get_lockers_punish, width=50,values=["MINIMIZE","CLOSE","DEBUG","LAG"])
        combobox_type=ttk.Combobox(window_lockers,values=["BLACKLIST","WHITELIST"],textvariable=get_lockers_type,width=47)
        button_list=tk.Button(window_lockers,text="管理名单",width=15,command=edit_list)
        button_time_rules=tk.Button(window_lockers,text="时间设置",width=15,command=edit_time_rulers)
        button_sure_lockers=tk.Button(window_lockers,text="确定",width=15,command=sure_lockers)
        button_delete_lockers=tk.Button(window_lockers,text="删除",width=15,command=delete_lockers)

        entry_name.place(x=75,y=0)
        button_ifon.place(x=75,y=100)
        combobox_punish.place(x=75,y=200)
        combobox_type.place(x=75,y=300)
        button_list.place(x=75,y=350)
        button_time_rules.place(x=275,y=350)
        button_sure_lockers.place(x=75,y=400)
        button_delete_lockers.place(x=275,y=400)

    #count_tasks_button函数
    def edit_count_tasks():
        ##获取index,也就是所选项在data["count_tasks"]中的位置

        if count_tasks_state.get()!="新建":
            s=count_tasks_state.get().split(" ")[0]
            id=(s.split(":")[1])
            for i in range(0,len(data["count_tasks"])):
                if data["count_tasks"][i]["id"]==int(id):
                    index=i


        ##小窗创建
        window_count_tasks = tk.Toplevel()
        window_count_tasks.title("count_tasks")
        window_count_tasks.geometry("270x370")

        ##StringVar()方法保留的值
        get_id=tk.StringVar()
        get_tasks_name=tk.StringVar()
        get_note=tk.StringVar()
        get_ifon=tk.StringVar()
        get_daily_aim=tk.StringVar()
        get_weekly_aim=tk.StringVar()
        get_monthly_aim=tk.StringVar()
        get_deadline=tk.StringVar(value="null")
        get_deadline_aim=tk.StringVar(value="null")

        if count_tasks_state.get()=="新建":
            get_id.set("")
            get_tasks_name.set("")
            get_note.set("")
            get_ifon.set("off")
            get_daily_aim.set("null")
            get_weekly_aim.set("null")
            get_monthly_aim.set("null")
        else:
            count_tasks=data["count_tasks"][index]
            get_id.set(count_tasks["id"])
            get_tasks_name.set(count_tasks["name"])
            get_note.set(count_tasks["note"])
            if count_tasks["activate"]:
                state="on"
            else:
                state="off"
            get_ifon.set(state)
            if count_tasks["daily_aim"]==None:
                get_daily_aim.set("null")
            else:
                get_daily_aim.set(count_tasks["daily_aim"])
            if count_tasks["weekly_aim"]==None:
                get_weekly_aim.set("null")
            else:
                get_weekly_aim.set(count_tasks["weekly_aim"])
            if count_tasks["monthly_aim"]==None:
                get_monthly_aim.set("null")
            else:
                get_monthly_aim.set(count_tasks["monthly_aim"])
            if count_tasks["deadline_aim"]==None:
                pass
            else:
                if "date" in count_tasks["deadline_aim"]:
                    get_deadline.set(count_tasks["deadline_aim"]["date"])
                if "aim"  in count_tasks["deadline_aim"]:
                    get_deadline_aim.set(count_tasks["deadline_aim"]["aim"])
            #初始化StringVar的值这部分的逻辑有点冗余，但是懒得改了
        ##label组件的创建与布局
        label_id=tk.Label(window_count_tasks,text="id ",width=15)
        label_name=tk.Label(window_count_tasks,text="名字 ",width=15)
        label_note=tk.Label(window_count_tasks,text="附注 ",width=15)
        label_activate=tk.Label(window_count_tasks,text="启用 ",width=15)
        label_daily_aim=tk.Label(window_count_tasks,text="每日目标 ",width=15)
        label_weekly_aim=tk.Label(window_count_tasks,text="每周目标 ",width=15)
        label_monthly_aim=tk.Label(window_count_tasks,text="每月目标 ",width=15)
        label_deadline=tk.Label(window_count_tasks,text="截止日期 ",width=15)
        label_deadline_aim=tk.Label(window_count_tasks,text="截止前目标 ",width=15)

        label_id.place(x=0,y=0)
        label_name.place(x=0,y=30)
        label_note.place(x=0,y=60)
        label_activate.place(x=0,y=90)
        label_daily_aim.place(x=0,y=120)
        label_weekly_aim.place(x=0,y=150)
        label_monthly_aim.place(x=0,y=180)
        label_deadline.place(x=0,y=210)
        label_deadline_aim.place(x=0,y=240)

        def sure_count_tasks():
            if get_daily_aim.get()=="null":
                daily_aim=None
            else:
                daily_aim=int(get_daily_aim.get())
            if get_weekly_aim.get() == "null":
                weekly_aim = None
            else:
                weekly_aim = int(get_weekly_aim.get())
            if get_monthly_aim.get() == "null":
                monthly_aim = None
            else:
                monthly_aim = int(get_monthly_aim.get())

            if get_deadline.get()=="null":
                deadline=None
            else:
                deadline=get_deadline.get()
            if get_deadline_aim.get()=="null":
                aim=None
            else:
                aim=int(get_deadline_aim.get())
            if aim==None and deadline==None:
                deadline_aim=None
            elif aim==None and deadline!=None:
                deadline_aim={"aim":aim}
            elif aim!=None and deadline==None:
                deadline_aim={"date":deadline}
            else:
                deadline_aim={"aim":aim,"date":deadline}

            noid=(get_id.get()=="")
            if noid:
                messagebox.showerror('错误', '不可无id,请设置id')
                return

            id_notnum=not str.isdigit(get_id.get())
            if id_notnum:
                messagebox.showerror('错误', 'id必须是数字')
                return

            reid=False
            if count_tasks_state.get()=='新建':
                for i in data["count_tasks"]:
                    if i["id"]==int(get_id.get()):
                        reid=True
            else:
                for i in data["count_tasks"]:
                    if i["id"] == int(get_id.get()) and data["count_tasks"][index]!=i:
                        reid = True

            if reid:
                messagebox.showerror('错误', 'id重复，请更改id')
                return

            data_count_tasks={
                "id": int(get_id.get()),
                "name": get_tasks_name.get(),
                "note": get_note.get(),
                "activate": get_ifon.get()=="on",
                "daily_aim": daily_aim,
                "weekly_aim": weekly_aim,
                "monthly_aim": monthly_aim,
                "deadline_aim": deadline_aim
            }

            if count_tasks_state.get()=="新建":
                data["count_tasks"].append(data_count_tasks)
                i=len(combobox_count_tasks_values)-1
                combobox_count_tasks_values.remove("新建")
                combobox_count_tasks_values.append(f"id:{data["count_tasks"][i]["id"]} {data["count_tasks"][i]["name"]}")
                combobox_count_tasks_values.append("新建")
                combobox_count_tasks.config(values=combobox_count_tasks_values)         ###修改主窗口的下拉
            else:
                combobox_count_tasks_values.remove(f"id:{data["count_tasks"][index]["id"]} {data["count_tasks"][index]["name"]}")
                combobox_count_tasks_values.remove("新建")
                data["count_tasks"][index]=data_count_tasks
                combobox_count_tasks_values.append(f"id:{data["count_tasks"][index]["id"]} {data["count_tasks"][index]["name"]}")
                combobox_count_tasks_values.append("新建")
                combobox_count_tasks.config(values=combobox_count_tasks_values)

            with open(user_json_path.user_json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            window_count_tasks.destroy()


        def delete_sure_tasks():
            if count_tasks_state.get()=="新建":
                messagebox.showerror('错误', '新建项目不可以删除')
            else:
                make_sure=messagebox.askokcancel('删除', '确认删除吗')
                if make_sure:
                    combobox_count_tasks_values.remove(f"id:{data["count_tasks"][index]["id"]} {data["count_tasks"][index]["name"]}")
                    combobox_count_tasks.config(values=combobox_count_tasks_values)
                    data["count_tasks"].remove(data["count_tasks"][index])
                    window_count_tasks.destroy()
                    with open(user_json_path.user_json_path, "w", encoding="utf-8") as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

        def click_ifon():
            if get_ifon.get()=="on":
                get_ifon.set("off")
            else:
                get_ifon.set("on")
        ##其余组件的创建与布局
        entry_id=tk.Entry(window_count_tasks,textvariable=get_id,width=20)
        entry_name=tk.Entry(window_count_tasks,textvariable=get_tasks_name,width=20)
        entry_note=tk.Entry(window_count_tasks,textvariable=get_note,width=20)
        button_ifon=tk.Button(window_count_tasks,textvariable=get_ifon,width=20,command=click_ifon)
        combobox_daily_aim=ttk.Combobox(window_count_tasks,values=["null","请输入次数"],textvariable=get_daily_aim,width=17)
        combobox_weekly_aim=ttk.Combobox(window_count_tasks,values=["null","请输入次数"],textvariable=get_weekly_aim,width=17)
        combobox_monthly_aim=ttk.Combobox(window_count_tasks,values=["null","请输入次数"],textvariable=get_monthly_aim,width=17)
        combobox_deadline_aim=ttk.Combobox(window_count_tasks,values=["null","请输入次数"],textvariable=get_deadline_aim,width=17)
        combobox_deadline=ttk.Combobox(window_count_tasks,values=["null","请输入日期","示范：2024-12-31"],width=17,textvariable=get_deadline)
        button_sure=tk.Button(window_count_tasks,text="确认",width=10,command=sure_count_tasks)
        button_delete=tk.Button(window_count_tasks,text="删除",width=10,command=delete_sure_tasks)

        entry_id.place(x=100,y=0)
        entry_name.place(x=100,y=30)
        entry_note.place(x=100,y=60)
        button_ifon.place(x=100,y=90)
        combobox_daily_aim.place(x=100,y=120)
        combobox_weekly_aim.place(x=100,y=150)
        combobox_monthly_aim.place(x=100,y=180)
        combobox_deadline_aim.place(x=100,y=240)
        combobox_deadline.place(x=100,y=210)
        button_sure.place(x=50,y=300)
        button_delete.place(x=175,y=300)

    #timer_tasks函数
    def edit_timer_tasks():
        #找到index
        if timer_tasks_state.get()!="新建":
            s=timer_tasks_state.get().split(" ")[0]
            id=(s.split(":")[1])
            for i in range(0,len(data["timer_tasks"])):
                if data["timer_tasks"][i]["id"]==int(id):
                    index=i

        # 一级小窗创建
        window_timer_tasks = tk.Toplevel()
        window_timer_tasks.title("timer_tasks")
        window_timer_tasks.geometry("270x400")


        #StringVar()方法保留的值
        get_timer_list=[]

        get_id=tk.StringVar()
        get_timer_name=tk.StringVar()
        get_note=tk.StringVar()
        get_ifon=tk.StringVar()
        get_daily_aim=tk.StringVar()
        get_weekly_aim=tk.StringVar()
        get_monthly_aim=tk.StringVar()
        get_date=tk.StringVar()
        get_aim=tk.StringVar()    #deadline_aim中的aim

        #初始化StringVar()的值
        if timer_tasks_state.get()=="新建":
            get_id.set("")
            get_note.set("")
            get_timer_name.set("")
            get_ifon.set("off")
            get_daily_aim.set("null")
            get_weekly_aim.set("null")
            get_monthly_aim.set("null")
            get_aim.set("null")
            get_date.set("null")
            get_timer_list.append("TIMERS")
        else:
            ifon_dict={True:"on",False:"off"}
            if data["timer_tasks"][index]["daily_aim"]==None:
                daily_aim="null"
            else:
                daily_aim=str(data["timer_tasks"][index]["daily_aim"])
            if data["timer_tasks"][index]["weekly_aim"] == None:
                weekly_aim = "null"
            else:
                weekly_aim = str(data["timer_tasks"][index]["weekly_aim"])
            if data["timer_tasks"][index]["monthly_aim"] == None:
                monthly_aim = "null"
            else:
                monthly_aim = str(data["timer_tasks"][index]["monthly_aim"])
            if data["timer_tasks"][index]["deadline_aim"]==None:
                date="null"
                aim="null"
            else:
                if ("data" in data["timer_tasks"][index]["deadline_aim"]) and ("aim" in data["timer_tasks"][index]["deadline_aim"]):
                    date=data["timer_tasks"][index]["deadline_aim"]["date"]
                    aim=data["timer_tasks"][index]["deadline_aim"]["aim"]
                elif "data" in data["timer_tasks"][index]["deadline_aim"]:
                    date = data["timer_tasks"][index]["deadline_aim"]["date"]
                    aim="null"
                else:
                    date="null"
                    aim=data["timer_tasks"][index]["deadline_aim"]["aim"]

            get_id.set(data["timer_tasks"][index]["id"])
            get_note.set(data["timer_tasks"][index]["note"])
            get_timer_name.set(data["timer_tasks"][index]["name"])
            get_ifon.set(ifon_dict[data["timer_tasks"][index]["activate"]])
            get_daily_aim.set(daily_aim)
            get_weekly_aim.set(weekly_aim)
            get_monthly_aim.set(monthly_aim)
            get_aim.set(aim)
            get_date.set(date)
            for i in data["timer_tasks"][index]["timers"]:
                get_timer_list.append(i)


        #button中的函数
        def ifon():
            if get_ifon.get()=="on":
                get_ifon.set("off")
            else:
                get_ifon.set("on")
        def sure():
            #防御性检测 :不可无id,id必须是数字,不可使用重复的id
            noid=(get_id.get()=="")
            if noid:
                messagebox.showerror("错误","不可无id")
                return

            notnum=not str.isdigit(get_id.get())
            if notnum:
                messagebox.showerror("错误","id必须是数字")

            reid = False
            if timer_tasks_state.get() == '新建':
                for i in data["timer_tasks"]:
                    if i["id"] == int(get_id.get()):
                        reid = True
            else:
                for i in data["timer_tasks"]:
                    if i["id"] == int(get_id.get()) and data["timer_tasks"][index] != i:
                        reid = True
            if reid:
                messagebox.showerror('错误', 'id重复，请更改id')
                return

            #判断aim的情况并且确定反回值
            dict_ifon={"on":True,"off":False}

            if get_daily_aim.get()=="null":
                daily_aim=None
            else:
                daily_aim=int(get_daily_aim.get())
            if get_weekly_aim.get()=="null":
                weekly_aim=None
            else:
                weekly_aim=int(get_weekly_aim.get())
            if get_monthly_aim.get()=="null":
                monthly_aim=None
            else:
                monthly_aim=int(get_monthly_aim.get())
            if get_aim.get()=="null" and get_date.get()=="null":
                deadline_aim=None
            elif get_aim.get()=="null":
                deadline_aim={"date":get_date.get()}
            elif get_date.get()=="null":
                deadline_aim={"aim":int(get_aim.get())}
            else:
                deadline_aim={"date":get_date.get(),"aim":int(get_aim.get())}

            data_timer_tasks={"id":int(get_id.get()),
                              "name":get_timer_name.get(),
                              "note":get_note.get(),
                              "activate":dict_ifon[get_ifon.get()],
                              "timers":get_timer_list,
                              "daily_aim":daily_aim,
                              "weekly_aim":weekly_aim,
                              "monthly_aim":monthly_aim,
                              "deadline_aim":deadline_aim}

            if timer_tasks_state.get()=="新建":
                data["timer_tasks"].append(data_timer_tasks)
                i = len(combobox_timer_tasks_values) - 1
                combobox_timer_tasks_values.remove("新建")
                combobox_timer_tasks_values.append(f"id:{data["timer_tasks"][i]["id"]} {data["timer_tasks"][i]["name"]}")
                combobox_timer_tasks_values.append("新建")
                combobox_timer_tasks.config(values=combobox_timer_tasks_values)  ###修改主窗口的下拉
            else:
                combobox_timer_tasks_values.remove(f"id:{data["timer_tasks"][index]["id"]} {data["timer_tasks"][index]["name"]}")
                combobox_timer_tasks_values.remove("新建")
                data["timer_tasks"][index] = data_timer_tasks
                combobox_timer_tasks_values.append(f"id:{data["timer_tasks"][index]["id"]} {data["timer_tasks"][index]["name"]}")
                combobox_timer_tasks_values.append("新建")
                combobox_timer_tasks.config(values=combobox_timer_tasks_values)

            with open(user_json_path.user_json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            window_timer_tasks.destroy()

        def delete():
            if timer_tasks_state.get() == "新建":
                messagebox.showerror('错误', '新建项目不可以删除')
            else:
                make_sure = messagebox.askokcancel('删除', '确认删除吗')
                if make_sure:
                    combobox_timer_tasks_values.remove(f"id:{data["timer_tasks"][index]["id"]} {data["timer_tasks"][index]["name"]}")
                    combobox_timer_tasks.config(values=combobox_timer_tasks_values)
                    data["timer_tasks"].remove(data["timer_tasks"][index])
                    window_timer_tasks.destroy()
                    with open(user_json_path.user_json_path, "w", encoding="utf-8") as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
        def edit_timer():
            window_edit_timer=tk.Toplevel()
            window_edit_timer.geometry("300x800")
            window_edit_timer.title("edit_timer")
            frame=tk.Frame(window_edit_timer)
            frame.place(x=0,y=50)
            get_timer_list_m=[]

            def add_rules(i=None):
                if i==None:
                    i=""
                get_timer_ruler=tk.StringVar(value=i)
                label_timer_ruler=tk.Label(frame,text="可选计时")
                combobox_timer_rules=ttk.Combobox(frame,values=["请输入分钟数","或者预设的时间集","可以再preset中预设时间集"],textvariable=get_timer_ruler)
                button_delete_this_rule=tk.Button(frame,text="删除",command=lambda:delete_this_rule(get_timer_ruler.get(),label_timer_ruler,combobox_timer_rules,button_sure_this_rule,button_delete_this_rule))
                button_sure_this_rule=tk.Button(frame,text="确认",command=lambda:sure_this_rule(get_timer_ruler.get()))

                label_timer_ruler.pack(side="top",fill="x",padx=10,pady=5)
                combobox_timer_rules.pack(side="top",fill="x",padx=10,pady=5)
                button_sure_this_rule.pack(side="top",fill="x",padx=10,pady=5)
                button_delete_this_rule.pack(side="top",fill="x",padx=10,pady=5)

                if i!="":
                    sure_this_rule(i)



            def sure_this_rule(x):
                if x!="" and (x not in get_timer_list_m):
                    get_timer_list_m.append(x)
            def delete_this_rule(x,label,combobox,button1,button2):
                if x in get_timer_list_m:
                    get_timer_list_m.remove(x)
                label.destroy()
                combobox.destroy()
                button1.destroy()
                button2.destroy()

            def sure_all_rule():
                for i in get_timer_list_m:
                    if i not in get_timer_list:
                        get_timer_list.append(i)
                remove_list=[]
                for i in get_timer_list:
                    if i not in get_timer_list_m:
                        remove_list.append(i)
                for i in remove_list:
                    get_timer_list.remove(i)
                window_edit_timer.destroy()


            for i in get_timer_list:
                add_rules(i)
            button_sure_all_rules=tk.Button(window_edit_timer,text="完成",command=sure_all_rule)
            button_add_timer=tk.Button(window_edit_timer,text="新增",command=add_rules)
            button_add_timer.place(x=0,y=0)
            button_sure_all_rules.place(x=50,y=0)


        #label的创建和布局
        label_id=tk.Label(window_timer_tasks,text="id",width=15)
        label_name=tk.Label(window_timer_tasks,text="名字",width=15)
        label_note=tk.Label(window_timer_tasks,text="附注",width=15)
        label_ifon=tk.Label(window_timer_tasks,text="启用",width=15)
        label_timers=tk.Label(window_timer_tasks,text="可选计时",width=15)
        label_daily_aim=tk.Label(window_timer_tasks,text="每日目标",width=15)
        label_weekly_aim=tk.Label(window_timer_tasks,text="每周目标",width=15)
        label_monthly_aim=tk.Label(window_timer_tasks,text="每月目标",width=15)
        label_aim=tk.Label(window_timer_tasks,text="截止日期前目标",width=15)
        label_deadline=tk.Label(window_timer_tasks,text="截止日期",width=15)

        label_id.place(x=0,y=0)
        label_name.place(x=0,y=30)
        label_note.place(x=0, y=60)
        label_ifon.place(x=0,y=90)
        label_timers.place(x=0,y=120)
        label_daily_aim.place(x=0,y=150)
        label_weekly_aim.place(x=0,y=180)
        label_monthly_aim.place(x=0,y=210)
        label_aim.place(x=0,y=240)
        label_deadline.place(x=0,y=270)

        #其余组件的创建与布局
        entry_id=tk.Entry(window_timer_tasks,textvariable=get_id,width=20)
        entry_name=tk.Entry(window_timer_tasks,textvariable=get_timer_name,width=20)
        entry_note=tk.Entry(window_timer_tasks,textvariable=get_note,width=20)
        button_ifon=tk.Button(window_timer_tasks,textvariable=get_ifon,width=20,command=ifon)
        button_timers=tk.Button(window_timer_tasks,text="编辑",width=20,command=edit_timer)
        combobox_daily_aim=ttk.Combobox(window_timer_tasks,values=["null","请输入目标时长"],textvariable=get_daily_aim,width=17)
        combobox_weekly_aim=ttk.Combobox(window_timer_tasks,values=["null","请输入目标时长"],textvariable=get_weekly_aim,width=17)
        combobox_monthly_aim=ttk.Combobox(window_timer_tasks,values=["null","请输入目标时长"],textvariable=get_monthly_aim,width=17)
        combobox_aim=ttk.Combobox(window_timer_tasks,values=["null","请输入目标时长"],textvariable=get_aim,width=17)
        combobox_deadline=ttk.Combobox(window_timer_tasks,values=["null","请输入请输入日期,","示范：2024-12-31"],textvariable=get_date,width=17)
        button_sure=tk.Button(window_timer_tasks,text="确认",width=10,command=sure)
        button_delete=tk.Button(window_timer_tasks,text="删除",width=10,command=delete)

        entry_id.place(x=100,y=0)
        entry_name.place(x=100, y=30)
        entry_note.place(x=100, y=60)
        button_ifon.place(x=100, y=90)
        button_timers.place(x=100,y=120)
        combobox_daily_aim.place(x=100, y=150)
        combobox_weekly_aim.place(x=100, y=180)
        combobox_monthly_aim.place(x=100, y=210)
        combobox_aim.place(x=100, y=240)
        combobox_deadline.place(x=100, y=270)
        button_sure.place(x=50,y=330)
        button_delete.place(x=175,y=330)

    #preset函数
    def edit_preset():
        # 一级小窗创建
        window_preset = tk.Toplevel()
        window_preset.title("preset")
        window_preset.geometry("400x250")

        #辅助函数
        def str_to_list(s):
            l= [int(num_str) for num_str in s.split(',')]
            return l
        def list_to_str(l):
            s= ','.join(map(str, l))
            return s


        #初始值
        get_black=data["presets"]["BLACK"]
        get_white=data["presets"]["WHITE"]
        get_timer=tk.StringVar(value=list_to_str(data["presets"]["TIMERS"]))
        get_days={}
        for i in data["presets"]:
            if i!="BLACK" and i!="WHITE" and i!="TIMERS":
                get_days[i]=data["presets"][i]



        #button函数的布局
        def edit_black():

            counter=1 #计数器，用于换列
            get_black_m=[]
            window_black=tk.Toplevel()
            window_black.geometry("700x750")
            window_black.title("black   最多27条")
            frame1=tk.Frame(window_black)
            frame2=tk.Frame(window_black)
            frame3=tk.Frame(window_black)
            frame1.place(x=0,y=30)
            frame2.place(x=200,y=30)
            frame3.place(x=400,y=30)

            def get_frame():
                if counter<=9:
                    return frame1
                elif counter>9 and counter<=18:
                    return frame2
                elif counter>18 and counter<=27:
                    return frame3

            def sure_this(str):
                if str not in get_black_m and str!="":
                    get_black_m.append(str)

            def delete(str,entry,button1,button2):
                nonlocal counter
                if str in get_black_m:
                    get_black_m.remove(str)
                counter-=1
                entry.destroy()
                button1.destroy()
                button2.destroy()


            def sure_all_black():
                nonlocal get_black
                get_black=get_black_m
                print(get_black)
                window_black.destroy()

            def add(i=None):
                if i==None:
                    i=""
                nonlocal  counter
                black=tk.StringVar(value=i)
                f=get_frame()
                entry_black=tk.Entry(f,textvariable=black,width=20)
                button_sure_this=tk.Button(f,text="确认",width=20,height=1,command=lambda:sure_this(black.get()))
                button_delete=tk.Button(f,text="删除",width=20,height=1,command=lambda:delete(black.get(),entry_black,button_sure_this,button_delete))
                entry_black.pack()
                button_sure_this.pack()
                button_delete.pack()
                counter+=1
                if i!="":
                    sure_this(i)

            for i in get_black:
                add(i)
            button_add=tk.Button(window_black,text="新增",width=10,command=add)
            button_sure_all_black=tk.Button(window_black,text="完成",width=10,command=sure_all_black)
            button_sure_all_black.place(x=100,y=0)
            button_add.place(x=0,y=0)
        def edit_white():
            counter = 1  # 计数器，用于换列
            get_white_m = []
            window_white = tk.Toplevel()
            window_white.geometry("700x750")
            window_white.title("white   最多27条")
            frame1 = tk.Frame(window_white)
            frame2 = tk.Frame(window_white)
            frame3 = tk.Frame(window_white)
            frame1.place(x=0, y=30)
            frame2.place(x=200, y=30)
            frame3.place(x=400, y=30)

            def get_frame():
                if counter <= 9:
                    return frame1
                elif counter > 9 and counter <= 18:
                    return frame2
                elif counter > 18 and counter <= 27:
                    return frame3

            def sure_this(str):
                if str not in get_white_m and str != "":
                    get_white_m.append(str)

            def delete(str, entry, button1, button2):
                nonlocal counter
                if str in get_white_m:
                    get_white_m.remove(str)
                counter -= 1
                entry.destroy()
                button1.destroy()
                button2.destroy()

            def sure_all_white():
                nonlocal get_white
                get_white = get_white_m
                print(get_white)
                window_white.destroy()

            def add(i=None):
                if i == None:
                    i = ""
                nonlocal counter
                white = tk.StringVar(value=i)
                f = get_frame()
                entry_white = tk.Entry(f, textvariable=white, width=20)
                button_sure_this = tk.Button(f, text="确认", width=20, height=1, command=lambda: sure_this(white.get()))
                button_delete = tk.Button(f, text="删除", width=20, height=1,command=lambda: delete(white.get(), entry_white, button_sure_this, button_delete))
                entry_white.pack()
                button_sure_this.pack()
                button_delete.pack()
                counter += 1
                if i != "":
                    sure_this(i)

            for i in get_white:
                add(i)
            button_add = tk.Button(window_white, text="新增", width=10, command=add)
            button_sure_all_white = tk.Button(window_white, text="完成", width=10, command=sure_all_white)
            button_sure_all_white.place(x=100, y=0)
            button_add.place(x=0, y=0)
        def edit_days():
            get_days_m={}
            window_days=tk.Toplevel()
            window_days.geometry("300x700")
            window_days.title("days")
            frame1=tk.Frame(window_days)
            frame1.place(x=0,y=30)


            def sure_this_day(name,value):
                if name not in get_days_m and name!="" and value!="":
                    get_days_m[name]=str_to_list(value)

            def delete(name,entry1,entry2,button1,button2):
                if name in get_days_m:
                    del get_days_m[name]
                entry1.destroy()
                entry2.destroy()
                button1.destroy()
                button2.destroy()


            def add(i=None):
                if i==None:
                    i={"":[]}
                for ii in i:
                    days_name=tk.StringVar(value=ii)
                    days_value=tk.StringVar(value=list_to_str(i[ii]))
                    entry_name=tk.Entry(frame1,width=20,textvariable=days_name)
                    entry_value=tk.Entry(frame1,width=20,textvariable=days_value)
                    button_sure_this_day=tk.Button(frame1,text="确定",width=20,command=lambda:sure_this_day(days_name.get(),days_value.get()))
                    button_delete=tk.Button(frame1,text="删除",width=20,command=lambda:delete(days_name.get(),entry_name,entry_value,button_sure_this_day,button_delete))
                    entry_name.pack()
                    entry_value.pack()
                    button_sure_this_day.pack()
                    button_delete.pack()
                    if i!={"":[]}:
                        sure_this_day(days_name.get(),days_value.get())

            def sure_all_days():
                nonlocal  get_days
                get_days=get_days_m
                print(get_days)
                window_days.destroy()

            add(get_days)

            button_add=tk.Button(window_days,text="新增",width=10,command=add)
            button_sure_all_days=tk.Button(window_days,text="完成",width=10,command=sure_all_days)
            button_add.place(x=0,y=0)
            button_sure_all_days.place(x=100,y=0)

        def sure():
            data_presets={
                "BLACK":get_black,
                "WHITE":get_white,
                "TIMERS":str_to_list(get_timer.get()),
            }
            for i in get_days:
                data_presets[i]=get_days[i]
            data["presets"]=data_presets
            with open(user_json_path.user_json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            window_preset.destroy()



        #label的创建和布局
        label_black=tk.Label(window_preset,text="BLACK:",width=10)
        label_white=tk.Label(window_preset,text="WHITE:",width=10)
        label_timers=tk.Label(window_preset,text="TIMERS:",width=10)
        label_days=tk.Label(window_preset,text="DAYS",width=10)

        label_black.place(x=0,y=10)
        label_white.place(x=0,y=60)
        label_timers.place(x=0,y=110)
        label_days.place(x=0,y=160)

        #其它组件的创建与布局
        button_black=tk.Button(window_preset,text="编辑",width=40,command=edit_black)
        button_white=tk.Button(window_preset,text="编辑",width=40,command=edit_white)
        entry_timers=tk.Entry(window_preset,width=40,textvariable=get_timer)
        button_days=tk.Button(window_preset,text="编辑",width=40,command=edit_days)
        button_sure=tk.Button(window_preset,text="确定",width=20,command=sure)

        button_black.place(x=100,y=10)
        button_white.place(x=100,y=60)
        entry_timers.place(x=100,y=110)
        button_days.place(x=100,y=160)
        button_sure.place(x=130,y=210)

    window=tk.Toplevel()
    window.title("setting")
    window.geometry("400x500")

    #主界面label的创建与布局
    label_lockers=tk.Label(window,text="lockers")
    label_count_tasks=tk.Label(window,text="count_tasks")
    label_timer_tasks=tk.Label(window,text="timer_tasks")
    label_presets=tk.Label(window,text="presets")


    label_lockers.place(x=0,y=100)
    label_count_tasks.place(x=0,y=200)
    label_timer_tasks.place(x=0,y=300)
    label_presets.place(x=0,y=400)


    #主界面选择框的创建与布局
    lockers_state=tk.StringVar(value="新建")
    count_tasks_state=tk.StringVar(value="新建")
    timer_tasks_state=tk.StringVar(value="新建")

    combobox_lockers=ttk.Combobox(window,textvariable=lockers_state,values=combobox_lockers_values)
    combobox_count_tasks=ttk.Combobox(window,textvariable=count_tasks_state,values=combobox_count_tasks_values)
    combobox_timer_tasks=ttk.Combobox(window,textvariable=timer_tasks_state,values=combobox_timer_tasks_values)
    label_presets=tk.Label(window,text="     ")


    combobox_lockers.place(x=100,y=100)
    combobox_count_tasks.place(x=100,y=200)
    combobox_timer_tasks.place(x=100,y=300)
    label_presets.place(x=100,y=400)


    #主界面按钮的创建和布局
    button_lockers=tk.Button(window,text="编辑",command=edit_lockers)
    button_count_tasks=tk.Button(window,text="编辑",command=edit_count_tasks)
    button_timer_tasks=tk.Button(window,text="编辑",command=edit_timer_tasks)
    button_presets=tk.Button(window,text="编辑",command=edit_preset)


    button_lockers.place(x=300,y=100)
    button_count_tasks.place(x=300,y=200)
    button_timer_tasks.place(x=300,y=300)
    button_presets.place(x=300,y=400)


