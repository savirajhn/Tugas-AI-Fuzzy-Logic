import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Baca data dari file Excel
data = pd.read_excel('data_cuaca.xlsx')
print(data.shape)

# Input variables
suhu = ctrl.Antecedent(np.arange(10, 41, 1), 'suhu')
kelembapan = ctrl.Antecedent(np.arange(20, 101, 1), 'kelembapan')
kecepatan_angin = ctrl.Antecedent(np.arange(0, 11, 1), 'kecepatan_angin')

# Output variable
cuaca = ctrl.Consequent(np.arange(0, 101, 1), 'cuaca')

# Fungsi keanggotaan untuk suhu
suhu.automf(3)
kelembapan.automf(3)
kecepatan_angin.automf(3)

# Fungsi keanggotaan untuk cuaca
cuaca['cerah'] = fuzz.trimf(cuaca.universe, [0, 25, 50])
cuaca['berawan'] = fuzz.trimf(cuaca.universe, [40, 60, 80])
cuaca['hujan'] = fuzz.trimf(cuaca.universe, [60, 75, 100])

# Rules
rule1 = ctrl.Rule(suhu['poor'] | kelembapan['poor'] | kecepatan_angin['poor'], cuaca['cerah'])
rule2 = ctrl.Rule(suhu['average'] | kelembapan['average'] | kecepatan_angin['average'], cuaca['berawan'])
rule3 = ctrl.Rule(suhu['good'] | kelembapan['good'] | kecepatan_angin['good'], cuaca['hujan'])

# Control system
cuaca_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
cuaca_sim = ctrl.ControlSystemSimulation(cuaca_ctrl)

# List untuk menyimpan hasil
hasil = []

# Loop melalui setiap record data dan lakukan simulasi kontrol untuk masing-masing
for idx, row in data.iterrows():
    suhu_val = row['suhu']
    kelembapan_val = row['kelembapan']
    kecepatan_angin_val = row['kecepatan_angin']
    # Set nilai input berdasarkan record saat ini
    cuaca_sim.input['suhu'] = suhu_val
    cuaca_sim.input['kelembapan'] = kelembapan_val
    cuaca_sim.input['kecepatan_angin'] = kecepatan_angin_val

    # Lakukan perhitungan
    cuaca_sim.compute()

    # Tentukan keterangan cuaca berdasarkan nilai output
    nilai_cuaca = cuaca_sim.output['cuaca']
    keterangan_cuaca = ''
    if nilai_cuaca <= 25:
        keterangan_cuaca = 'Cerah'
    elif nilai_cuaca <= 50:
        keterangan_cuaca = 'Berawan'
    else:
        keterangan_cuaca = 'Hujan'

    # Simpan hasil untuk record saat ini
    hasil.append({'Record': idx+1, 'Perkiraan Cuaca': nilai_cuaca, 'Keterangan Cuaca': keterangan_cuaca})

# Buat dataframe dari hasil
hasil_df = pd.DataFrame(hasil)

# Simpan dataframe ke dalam file Excel
hasil_df.to_excel('hasil_perkiraan_cuaca.xlsx', index=False)

print("Hasil telah disimpan dalam file 'hasil_perkiraan_cuaca.xlsx'")