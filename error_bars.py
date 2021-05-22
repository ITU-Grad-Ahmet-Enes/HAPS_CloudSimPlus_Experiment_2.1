import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px

outputFile1 = open("smallErrorBarCloudlet.txt", "r")
outputFile2 = open("bigErrorBarCloudlet.txt", "r")

outputFile3 = open("smallErrorBarVm.txt", "r")
outputFile4 = open("bigErrorBarVm.txt", "r")

smallHAPS_Cloudlet = outputFile1.read().split('\n')
smallHAPS_Cloudlet.pop()

bigHAPS_Cloudlet = outputFile2.read().split('\n')
bigHAPS_Cloudlet.pop()

smallHAPS_Vm_Life_Time = outputFile3.read().split('\n')
smallHAPS_Vm_Life_Time.pop()

bigHAPS_Vm_Life_Time = outputFile4.read().split('\n')
bigHAPS_Vm_Life_Time.pop()

std_energy_small_cloudlet = np.array([])
std_energy_small_vm = np.array([])
std_energy_big_cloudlet = np.array([])
std_energy_big_vm = np.array([])

sum_energy_small = 0
sum_energy_big = 0

y_small_cloudlet_energy = []
y_small_vm_energy = []
y_big_cloudlet_energy = []
y_big_vm_energy = []

type_small_cloudlet = []
type_small_vm = []
type_big_cloudlet = []
type_big_vm = []
Number_of_Cloudlets = []
Delays = []
for i in range(10):  # i<5 diger dosyadaki iterasyon cloudlet
    energy_small_cloudlet = np.array([])
    energy_big_cloudlet = np.array([])
    Number_of_Cloudlets.append(25 + i * 250)
    type_small_cloudlet.append('Lower Altitude')
    type_big_cloudlet.append('Higher Altitude')
    for j in range(5):  # (number of test = 10 ) * 3
        energy_small_cloudlet = np.append(energy_small_cloudlet, int(smallHAPS_Cloudlet[i * 5 + j]))
        energy_big_cloudlet = np.append(energy_big_cloudlet, int(bigHAPS_Cloudlet[i * 5 + j]))

    std_energy_small_cloudlet = np.append(std_energy_small_cloudlet, np.std(energy_small_cloudlet[0:9]))
    std_energy_big_cloudlet = np.append(std_energy_big_cloudlet, np.std(energy_big_cloudlet[0:9]))
    y_small_cloudlet_energy.append(np.mean(energy_small_cloudlet))
    y_big_cloudlet_energy.append(np.mean(energy_big_cloudlet))

for i in range(10):  # i<5 diger dosyadaki iterasyon vm
    energy_small_vm = np.array([])
    energy_big_vm = np.array([])
    Delays.append(1000 + i * 2000)
    type_small_vm.append('Lower Altitude')
    type_big_vm.append('Higher Altitude')
    for j in range(5):  # (number of test = 10 ) * 3
        energy_small_vm = np.append(energy_small_vm, int(smallHAPS_Vm_Life_Time[i * 5 + j]))
        energy_big_vm = np.append(energy_big_vm, int(bigHAPS_Vm_Life_Time[i * 5 + j]))

    std_energy_small_vm = np.append(std_energy_small_vm, np.std(energy_small_vm[0:9]))
    std_energy_big_vm = np.append(std_energy_big_vm, np.std(energy_big_vm[0:9]))
    y_small_vm_energy.append(np.mean(energy_small_vm))
    y_big_vm_energy.append(np.mean(energy_big_vm))

data1 = {'Cloudlet': Number_of_Cloudlets + Number_of_Cloudlets,
         'Energy': y_small_cloudlet_energy + y_big_cloudlet_energy,
         'Type': type_small_cloudlet + type_big_cloudlet}

data2 = {'Delay': Delays + Delays,
         'Energy': y_small_vm_energy + y_big_vm_energy,
         'Type': type_small_vm + type_big_vm}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
std_cloudlet = np.append(std_energy_small_cloudlet, std_energy_big_cloudlet)
std_vm = np.append(std_energy_small_vm, std_energy_big_vm)
fig = px.scatter(
    data_frame=df1,
    x='Cloudlet',
    y='Energy',
    error_y=std_cloudlet,
    custom_data=['Energy'], color="Type"
)

fig.update_traces(mode="markers+lines",
                  marker_symbol="circle",
                  marker=dict(color='#121111', size=8),
                  line=dict(color='#45403f', width=2, dash='dash'),
                  hovertemplate="<br>".join([
                      "Cloudlet: %{x}",
                      "Energy: %{y}"
                  ])
                  )

fig.update_layout(
    title_text="x:NumberOfCloudLets y:EnergyConsuptionInKw)",
    width=1200,
    yaxis_title='Energy Consumption (KWatt) ',
    xaxis_title='Number of Cloudlets',
    template="none"
    # xaxis_color='plum'
)

fig.show()
# ####################################################################################
fig = px.scatter(
    data_frame=df2,
    x='Delay',
    y='Energy',
    error_y=std_vm,
    custom_data=['Energy'], color="Type"
)

fig.update_traces(mode="markers+lines", row=1, col=1,
                  marker_symbol="diamond-open",
                  marker=dict(color='#121111', size=8),
                  line=dict(color='#45403f', width=2, dash='dashdot'),
                  hovertemplate="<br>".join([
                      "Delay: %{x}",
                      "Energy: %{y}"
                  ])
                  )

# fig.update_xaxes(autorange="reversed")

fig.update_layout(
    title_text="x:MeanDelay y:EnergyConsumptionInKw, NumberOfCloudlet 2000)",
    width=1200,
    yaxis_title='Energy Consumption (KWatt) ',
    xaxis_title='Mean Delay (second)',
    template="none"
    # xaxis_color='plum'
)

fig.show()
##################################################################################################

fig = go.Figure()

fig.add_trace(go.Scatter(x=Number_of_Cloudlets, y=y_small_cloudlet_energy, name="Lower Altitude",
                         mode="lines+markers", marker_symbol="circle",
                         marker=dict(color='#121111', size=8),
                         line=dict(color='#45403f', width=2, dash='dash'),
                         error_y=dict(
                             type='data',
                             array=std_energy_small_cloudlet,
                             visible=True)

                         ))

fig.add_trace(go.Scatter(x=Number_of_Cloudlets, y=y_big_cloudlet_energy, name="Higher Altitude",
                         mode="lines+markers", marker_symbol="diamond-open-dot",
                         marker=dict(color='#121111', size=8),
                         line=dict(color='#45403f', width=2, dash='dashdot'),
                         error_y=dict(
                             type='data',
                             array=std_energy_big_cloudlet,
                             visible=True)

                         ))

fig.update_layout(
    title_text="x:NumberOfCloudLets y:EnergyConsuptionInKw",
    width=1200,
    yaxis_title='Energy Consumption (KWatt)',
    xaxis_title='Number of Cloudlets',
)

fig.update_layout(template="none")

fig.show()
##################################################################################################
fig = go.Figure()

fig.add_trace(go.Scatter(x=Delays, y=y_small_vm_energy, name="Lower Altitude",
                         mode="lines+markers", marker_symbol="square",
                         marker=dict(color='#121111', size=8),
                         line=dict(color='#45403f', width=2, dash='dash'),
                         error_y=dict(
                             type='data',
                             array=std_energy_small_vm,
                             visible=True)

                         ))

fig.add_trace(go.Scatter(x=Delays, y=y_big_vm_energy, name="Higher Altitude",
                         mode="lines+markers", marker_symbol="diamond-open-dot",
                         marker=dict(color='#121111', size=8),
                         line=dict(color='#45403f', width=2, dash='dashdot'),
                         error_y=dict(
                             type='data',
                             array=std_energy_big_vm,
                             visible=True)

                         ))

fig.update_layout(
    title_text="x:x:MeanDelay y:EnergyConsumptionInKw, NumberOfCloudlet 2000",
    width=1200,
    yaxis_title='Energy Consumption (KWatt)',
    xaxis_title='Mean Delay (second)',
)

fig.update_layout(template="none")

fig.show()