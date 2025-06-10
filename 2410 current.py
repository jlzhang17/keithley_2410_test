import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import time
import os

# 参数设置
gpib_address = 'GPIB0::24::INSTR'
voltages = np.arange(0,-200,-10)  # 电压从0到100V
samples_per_point = 10
compliance_current = 1e-3  # 电流保护
wait_time_after_set = 10  # 设置电压后等待时间
save_dir = 'IV_Measurements'
os.makedirs(save_dir, exist_ok=True)

# 初始化设备
rm = pyvisa.ResourceManager()
keithley = rm.open_resource(gpib_address)
keithley.write("*RST")
keithley.write(":SOUR:FUNC VOLT")
keithley.write(":SENS:FUNC 'CURR'")
keithley.write(f":SENS:CURR:PROT {compliance_current}")
keithley.write(":SENS:CURR:RANGE:AUTO ON")#自动量程
#keithley.write(":SENS:CURR:RANGE:1e-6")#量程200pA
keithley.write(":FORM:ELEM VOLT,CURR")  # 返回电压、电流
keithley.write(":OUTP ON")

# 打开交互式绘图
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], marker='o')
ax.set_xlabel("Sample Index")
ax.set_ylabel("Current (A)")
ax.set_title("Current Sampling")
ax.grid(True)

# 准备保存数据
voltage_list = []
current_mean_list = []
current_std_list = []

txt_output_path = os.path.join(save_dir, "iv_data.txt")
with open(txt_output_path, 'w') as f_txt:
    f_txt.write("Voltage(V)\tCurrent(A)\tStd(A)\n")

    for v in voltages:
        print(f"\n设置电压为 {v} V，等待 {wait_time_after_set} 秒...")
        keithley.write(f":SOUR:VOLT {v}")
        time.sleep(wait_time_after_set)

        # 实时绘图初始化
        currents = []
        line.set_data([], [])
        ax.set_xlim(0, samples_per_point)
        ax.set_ylim(-compliance_current * 1.1, compliance_current * 1.1)
        fig.canvas.draw()
        fig.canvas.flush_events()

        for i in range(samples_per_point):
            data = keithley.query(":READ?")
            try:
                _, current_val = map(float, data.strip().split(','))
                currents.append(current_val)
            except:
                print(f"读取错误: {data}")
                currents.append(0)
            # 更新实时图
            line.set_data(range(len(currents)), currents)
            ax.relim()
            ax.autoscale_view(True, True, True)
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.02)

        currents = np.array(currents)
        current_mean = np.mean(currents)
        current_std = np.std(currents)

        voltage_list.append(v)
        current_mean_list.append(current_mean)
        current_std_list.append(current_std)

        # 保存单点数据
        f_txt.write(f"{v:.2f}\t{current_mean:.5e}\t{current_std:.1e}\n")

        # 保存图像
        plt.ioff()
        plt.figure()
        plt.plot(range(len(currents)), currents, marker='o')
        plt.title(f"V = {v} V\nI_avg = {current_mean:.2e} A ± {current_std:.1e} A")
        plt.xlabel("Sample Index")
        plt.ylabel("Current (A)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{save_dir}/IV_{v}V.png")
        plt.close()
        plt.ion()

        print(f"完成 V={v} V：I = {current_mean:.2e} ± {current_std:.1e} A")

# 总图绘制
plt.ioff()
plt.figure(figsize=(8, 5))
plt.errorbar(voltage_list, current_mean_list, yerr=current_std_list, fmt='o-', capsize=5)
plt.xlabel("Voltage (V)")
plt.ylabel("Current (A)")
plt.title("I-V Curve with Error Bars")
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{save_dir}/IV_total.png")
plt.show()

# 关闭仪器
keithley.write(":OUTP OFF")
keithley.close()
rm.close()




