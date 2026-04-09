import tkinter as tk
from tkinter import ttk
# 分子量
NaCl = 58.44
KCl = 74.55
MgSO4_7H2O = 246.48

def ExtraNUM(str):
    new_str = ""
    for i in str:
        if i.isdecimal() or i == ',' or i == '.':
            new_str += i

    return new_str
class ENC(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttk.Label(self, text="病人体重(kg):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.weight = tk.IntVar()
        self.weight.set(50)
        ttk.Entry(self, textvariable=self.weight).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="目标热卡(kcal/kg/d):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.tkcal = tk.IntVar()
        self.tkcal.set(25)
        ttk.Entry(self, textvariable=self.tkcal).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="丢失液体量(ml):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.fluidloss = tk.IntVar()
        self.fluidloss.set(500)   # 设置变量
        ttk.Entry(self, textvariable=self.fluidloss).grid(row=2, column=1, padx=5, pady=5)

        
        self.result = tk.StringVar()
        ttk.Label(self, textvariable=self.result).grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(self, text="计算", 
                  command=self.calculate).grid(row=4, column=0, columnspan=2, pady=5)
    
    def calculate(self):
        try:
            weight = self.weight.get()
            fluidloss = self.fluidloss.get()
            dkr = weight * self.tkcal.get() # 每日热卡总量
            cbh = dkr/6.8
            fat = dkr/18
            cbh60 = dkr*0.6/3.4
            fat40 = dkr*0.4/9
            nn = dkr/100
            nn150 = dkr/150
            aa = nn*6.25
            aa150 = dkr/150*6.2
            aai = weight*1.2
            ln30 = weight*30
            ln40 = weight*40
            frv30 = fluidloss + ln30
            frv40 = fluidloss + ln40

            text = (f"每日热卡总量：{dkr:.3f}\n——三大营养素——\n碳水化合物(按50%算): {cbh:.3f}g\n碳水化合物(按60%算，推荐): {cbh60:.3f}g\n脂肪(按50%算): {fat:.3f}g\n脂肪(按40%算，推荐，高脂血症者可降更低): {fat40:.3f}g\n"
            f"氮(按1:100算): {nn:.3f}   (按1:150算): {nn150:.3f}\n氨基酸(按1:100算): {aa:.3f}   (按1:150算): {aa150:.3f}\n氨基酸(按理想体重算1.2g/kg/d(1.2-1.5)): {aai:.3f}\n——液体——\n"
            f"生理需要液体量(30ml/kg): {ln30:.3f}ml\n生理需要液体量(40ml/kg): {ln40:.3f}ml\n补液量(30ml/kg): {frv30:.3f}ml\n补液量(40ml/kg): {frv40:.3f}ml\n")
            self.result.set(text)
        except Exception:
            self.result.set("请输入有效数字")

def ExtraBGHT():
    data = "二氧化碳总量26.80 mmol/L,胆红素34.00 umol/L,血液酸碱度7.350 ,氧分压120.00↑mmHg,二氧化碳分压46.00↑mmHg,实际碳酸氢盐25.400 mmol/L,标准碳酸氢盐24.400 mmol/L,细胞外液剩余碱-0.200 mmol/L,血液剩余碱-0.60 mmol/L,氧容量17.80 ml/μL,氧含量18.00 mL/dL,氧饱和度98.90↑%,钾4.80 mmol/L,钠136.0 mmol/L,氯110.0↑mmol/L,钙（Ca++）POCT:Ca2+1.42↑mmol/L,阴离子间隙(血气)5.00↓mmol/L,血红蛋白131 g/L,红细胞比积测定(HCT)0.340↓,高铁血红蛋白1.10 %,还原血红蛋白1.10 %,碳氧血红蛋白1.20 %,氧合血红蛋白96.70 %,乳酸（Lac）POCT:乳酸0.80 mmol/L,葡萄糖（Glu）测定POCT:葡萄糖4.80 mmol/L"
    data = ExtraNUM(data)
    bga = data.split(',')
    # 测试用
    bgv = bga
    text = ''

    # 分析肺氧供
    i = float(bga[3]) / float(bga[11])
    
    # 分析通气
    i = float(bga[4])
    if (i > 35):
        text += "二氧化碳潴留\n"
    elif(i<35):
        text += "过度通气\n"

    flag = 0 # 正常 1呼碱 2呼酸 3代碱 4代酸

    # 动脉PH
    ia = float(bga[2])

    if(ia < 7.35):
        # 酸中毒
        if(float(bga[4]) > 45):# 判断co2分压趋势
            text += "呼吸性酸中毒" 
            flag = 2
        elif(float(bga[6]) < 22):
            text += "代谢性酸中毒"
            flag = 4
    elif(ia > 7.45):
        # 碱中毒
        if (float(bga[4]) < 35): # 判断co2分压趋势
            text += "呼吸性碱中毒"
            flag = 1
        elif(float(bga[6]) > 27):
            text += "代谢性碱中毒"
            flag = 3
    
    # 检查剩余碱BE
    ia = float(bga[7])
    if(ia >3):
        if(flag != 0):
            match(flag):
                case 0: text += "代谢性碱中毒"
                case 1: text += ""

    elif(ia < -3):
        if(flag != 0):
            text += "合并代谢性酸中毒"
        


    # 中心静脉氧饱和度ScvO2 二氧化碳分压PvCO2




    

    print(text)
    
    
    

    
# 计算结束

if __name__ == "__main__":
    ExtraBGHT()