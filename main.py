import tkinter as tk
from tkinter import ttk
from calculate import math_operations

option_index = 1

class MedicalCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("规培计算器")
        self.root.geometry("800x480")
        
        # 左侧主选项列表（列表A）
        self.main_frame = ttk.LabelFrame(root, text="主选项")
        self.main_frame.place(x=20, y=20, width=180, height=350)
        
        # 创建带滚动条的主选项列表
        self.main_list_frame = ttk.Frame(self.main_frame)
        self.main_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.main_canvas = tk.Canvas(self.main_list_frame)
        self.main_scrollbar = ttk.Scrollbar(self.main_list_frame, orient="vertical", command=self.main_canvas.yview)
        self.main_scrollable_frame = ttk.Frame(self.main_canvas)
        
        self.main_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.main_scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)
        
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_scrollbar.pack(side="right", fill="y")
        
        # 主选项
        self.main_options = ["常用", "肾脏"]
        self.main_listbox = tk.Listbox(self.main_scrollable_frame)
        for option in self.main_options:
            self.main_listbox.insert(tk.END, option)
        self.main_listbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.main_listbox.bind('<<ListboxSelect>>', self.on_main_option_select)
        
        # 右侧子选项列表
        self.sub_frame = ttk.LabelFrame(root, text="计算选项")
        self.sub_frame.place(x=220, y=20, width=180, height=350)
        
        # 创建带滚动条的子选项列表
        self.sub_list_frame = ttk.Frame(self.sub_frame)
        self.sub_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.sub_canvas = tk.Canvas(self.sub_list_frame)
        self.sub_scrollbar = ttk.Scrollbar(self.sub_list_frame, orient="vertical", command=self.sub_canvas.yview)
        self.sub_scrollable_frame = ttk.Frame(self.sub_canvas)
        
        self.sub_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.sub_canvas.configure(scrollregion=self.sub_canvas.bbox("all"))
        )
        
        self.sub_canvas.create_window((0, 0), window=self.sub_scrollable_frame, anchor="nw")
        self.sub_canvas.configure(yscrollcommand=self.sub_scrollbar.set)
        
        self.sub_canvas.pack(side="left", fill="both", expand=True)
        self.sub_scrollbar.pack(side="right", fill="y")
        
        # 初始显示空白
        self.sub_option_listbox = None
        self.current_sub_options = []
        
        # 参数输入区域
        self.input_frame = ttk.LabelFrame(root, text="参数输入")
        self.input_frame.place(x=420, y=20, width=360, height=450)
        
        # 初始显示空白
        self.current_input_frame = None
        
    def on_main_option_select(self, event):
        if self.sub_option_listbox:
            self.sub_option_listbox.destroy()
            
        selection = self.main_listbox.curselection()
        if not selection:
            return
            
        global option_index
        option_index = selection[0]
        
        # 更新子选项
        if option_index == 0:  # 
            self.current_sub_options = ["血气分析", "平均脉压计算","补液公式计算","鼻导管氧浓度","肠外营养计算"]
        elif option_index == 1:  # 
            self.current_sub_options = ["肌酐清除率"]
            
        # 创建新的子选项列表
        self.sub_option_listbox = tk.Listbox(self.sub_scrollable_frame)
        for option in self.current_sub_options:
            self.sub_option_listbox.insert(tk.END, option)
        self.sub_option_listbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.sub_option_listbox.bind('<<ListboxSelect>>', self.on_sub_option_select)
        
        # 清除参数输入区域
        if self.current_input_frame:
            self.current_input_frame.destroy()
            self.current_input_frame = None

    def on_sub_option_select(self, event):
        if self.current_input_frame:
            self.current_input_frame.destroy()
            
        selection = self.sub_option_listbox.curselection()
        if not selection:
            return

        match option_index: 
            case(0): #常用计算  
                match selection[0]:
                    case(0): # "血气分析"
                        self.current_input_frame = BloodGasFrame(self.input_frame)
                    case(1): # "平均脉压计算"
                        self.current_input_frame = PulsePressureFrame(self.input_frame)
                    case(2): # "补液公式计算"
                        self.current_input_frame = FluidReplacementFrame(self.input_frame)
                    case(3): # "氧浓度计算"
                        self.current_input_frame = FiO2C(self.input_frame)
                    case(4): # 肠外营养
                        self.current_input_frame = math_operations.ENC(self.input_frame)
            case(1): #常用计算  
                match selection[0]:
                    case(0): # "肌酐清除率"
                        self.current_input_frame = CcrFrame(self.input_frame)
                        

        if self.current_input_frame:
            self.current_input_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# 计算功能框架
class BloodGasFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        
        ttk.Label(self, text="人工诊断:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        # 修正诊断
        self.diagnosis = ["未明确", "呼吸性碱中毒", "呼吸性酸中毒", "代谢性碱中毒", "代谢性酸中毒"]
        self.cb = ttk.Combobox(self, values=self.diagnosis, state="readonly")
        self.cb.current(0)
        self.cb.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="血液酸碱度:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.ph = tk.IntVar()
        ttk.Entry(self, textvariable=self.ph).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="动脉二氧化碳分压(mmHg):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.paco2 = tk.StringVar() # PaCO₂正常值为35-45mmHg，均值为40mmHg
        ttk.Entry(self, textvariable=self.paco2).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="实际碳酸氢盐(mmol/L):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.ab = tk.IntVar()
        ttk.Entry(self, textvariable=self.ab).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text="标准碳酸氢盐(mmol/L):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.sb = tk.IntVar()
        ttk.Entry(self, textvariable=self.sb).grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="钠离子:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.na = tk.StringVar()
        ttk.Entry(self, textvariable=self.na).grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self, text="氯离子:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.cl = tk.StringVar()
        ttk.Entry(self, textvariable=self.cl).grid(row=6, column=1, padx=5, pady=5)
        
        self.result = tk.StringVar()
        ttk.Label(self, textvariable=self.result).grid(row=7, column=0, columnspan=2, pady=10)
        
        ttk.Button(self, text="计算", 
                  command=self.calculate).grid(row=8, column=0, columnspan=2, pady=10)
    
    def calculate(self):
        try:
            index = self.cb.current()
            ph = self.ph.get()
            na = self.na.get()
            cl = self.cl.get()
            ab = self.ab.get()
            sb = self.sb.get()
            paco2 = self.paco2
            match index:
                case 0: # 未明确，使用自动处理
                    # 第一步，判断类型
                    if(paco2 < 35): # 判断co2分压趋势
                        trendco2 = -1
                    elif(paco2 > 45):
                        trendco2 = 1
                    else:
                        trendco2 = 0 
                    
                    if(sb < 22): # 判断hco3趋势（使用标准碳酸氢盐）
                        trendHCO3 = -1
                    elif(sb > 27):
                        trendHCO3 = 1
                    else:
                        trendHCO3 = 0 

                    if(ph >7.45):# 碱中毒
                        if(trendco2 == -1):
                            index = 1 # 猜测为原发性呼碱
                        elif(trendHCO3 == 1):
                            index = 3 # 猜测为原发性代碱
                    elif(ph < 7.35): #酸中毒
                        if(trendHCO3 == -1):
                            index = 4 # 猜测为原发性代酸
                        elif(trendco2 == 1):
                            index = 2 # 猜测为原发性呼酸

            
            



            self.result.set("测试")
        except Exception:
            self.result.set("请输入有效数字")
 
class PulsePressureFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttk.Label(self, text="收缩压(mmHg):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.systolic = tk.StringVar()
        ttk.Entry(self, textvariable=self.systolic).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="舒张压(mmHg):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.diastolic = tk.StringVar()
        ttk.Entry(self, textvariable=self.diastolic).grid(row=1, column=1, padx=5, pady=5)
        
        self.result = tk.StringVar()
        ttk.Label(self, textvariable=self.result).grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(self, text="计算", 
                  command=self.calculate).grid(row=3, column=0, columnspan=2, pady=10)
    
    def calculate(self):
        try:
            systolic = float(self.systolic.get())
            diastolic = float(self.diastolic.get())
            pulse_pressure = systolic - diastolic
            self.result.set(f"平均脉压: {pulse_pressure:.3f} mmHg")
        except Exception:
            self.result.set("请输入有效数字")
 
class FluidReplacementFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttk.Label(self, text="体重(kg):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.weight = tk.StringVar()
        ttk.Entry(self, textvariable=self.weight).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="脱水程度(%):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.dehydration = tk.StringVar()
        ttk.Entry(self, textvariable=self.dehydration).grid(row=1, column=1, padx=5, pady=5)
        
        self.result = tk.StringVar()
        ttk.Label(self, textvariable=self.result).grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(self, text="计算", 
                  command=self.calculate).grid(row=3, column=0, columnspan=2, pady=10)
    
    def calculate(self):
        try:
            weight = float(self.weight.get())
            dehydration = float(self.dehydration.get())
            fluid_needed = weight * dehydration / 100 * 1000  # 转换为毫升
            self.result.set(f"补液量: {fluid_needed:.0f} ml")
        except Exception:
            self.result.set("请输入有效数字")

class CcrFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttk.Label(self, text="性别:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.gender = tk.StringVar()
        ttk.Combobox(self, textvariable=self.gender, 
                    values=["男", "女"], state="readonly").grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="年龄:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.age = tk.IntVar()
        ttk.Entry(self, textvariable=self.age).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="体重(kg):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.weight = tk.DoubleVar()
        ttk.Entry(self, textvariable=self.weight).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="身高(cm):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.height = tk.IntVar()
        ttk.Entry(self, textvariable=self.height).grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="血肌酐(umol/L):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.scr = tk.DoubleVar()
        ttk.Entry(self, textvariable=self.scr).grid(row=4, column=1, padx=5, pady=5)
        
        self.result = tk.StringVar()
        ttk.Label(self, textvariable=self.result).grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(self, text="计算", 
                  command=self.calculate).grid(row=6, column=0, columnspan=2, pady=10)
    
    def calculate(self):
        try:
            # 肌酐清除率计算
            weight = self.weight.get()
            height = self.height.get() / 100
            scr = self.scr.get()
            age = self.age.get()
            # 血清肌酐的单位换算：1mg/dL=88.4umol/L。
            # 肌酐清除率计算
            Ccr = (140 - age) * weight / (0.818 * scr) 
            # 如果是女性
            if self.gender.get() == "女":
                Ccr = Ccr * 0.85

                
            self.result.set(f"肌酐清除率(mL/min): {Ccr:.3f}")
        except Exception:
            self.result.set("请输入有效数字")

class FiO2C(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttk.Label(self, text="氧流量(L/min):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.O2float = tk.StringVar()
        ttk.Entry(self, textvariable=self.O2float).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="吸气时间(秒):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.ti = tk.IntVar()
        self.ti.set(1)
        ttk.Entry(self, textvariable=self.ti).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="呼吸频率(次):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.bf = tk.IntVar()
        self.bf.set(20)   # 设置变量
        ttk.Entry(self, textvariable=self.bf).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="潮气量(mL):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.tv = tk.IntVar()
        self.tv.set(500)   # 设置变量
        ttk.Entry(self, textvariable=self.tv).grid(row=3, column=1, padx=5, pady=5)
        
        self.result = tk.StringVar()
        ttk.Label(self, textvariable=self.result).grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(self, text="计算", 
                  command=self.calculate).grid(row=5, column=0, columnspan=2, pady=10)
    
    def calculate(self):
        # 公式：FiO₂ = 21% + (氧流量×吸气时间×呼吸频率)/潮气量 ×100%
        try:
            O2float = float(self.O2float.get())
            if O2float >= 6:
                O2float = 6

            FiO2 = 21 + (O2float * self.ti.get() * self.bf.get())/self.tv.get() * 100

            self.result.set(f"吸入氧浓度: {FiO2:.3f} %")
        except Exception:
            self.result.set("请输入有效数字")
# 计算结束

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalCalculator(root)
    root.mainloop()

# Nuitka
