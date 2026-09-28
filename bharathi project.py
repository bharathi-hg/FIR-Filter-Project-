import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter
from pathlib import Path
import time

# ============================================================
# VLSI DESIGN OF FIR FILTER FOR DSP APPLICATIONS
# ============================================================

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
COEFF_DIR = BASE_DIR / "coefficients"
RESULT_DIR = BASE_DIR / "results"

COEFF_DIR.mkdir(exist_ok=True)
RESULT_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------
# 1. FIR FILTER DESIGN
# ------------------------------------------------------------

NUM_TAPS = 16
CUTOFF = 0.25
SCALE = 32768

coeff = firwin(NUM_TAPS, CUTOFF)

print("=" * 55)
print("VLSI DESIGN OF FIR FILTER FOR DSP APPLICATIONS")
print("=" * 55)

print("\n1. FIR FILTER COEFFICIENTS")
print("-" * 40)

for i, c in enumerate(coeff):
    print(f"h[{i:2}] = {c:.6f}")

# Fixed-point coefficients
fixed_coeff = np.round(coeff * SCALE).astype(int)

print("\n2. FIXED-POINT COEFFICIENTS")
print("-" * 40)
print(fixed_coeff)

# Save coefficients
np.savetxt(
    COEFF_DIR / "coefficients.txt",
    fixed_coeff,
    fmt="%d"
)

# ------------------------------------------------------------
# 2. INPUT SIGNAL
# ------------------------------------------------------------

fs = 1000
t = np.arange(0, 1, 1 / fs)

# Input signal containing two frequencies
input_signal = (
    np.sin(2 * np.pi * 50 * t)
    + 0.5 * np.sin(2 * np.pi * 300 * t)
)

# ------------------------------------------------------------
# 3. FIR FILTER SIMULATION
# ------------------------------------------------------------

start_time = time.perf_counter()

output_signal = lfilter(coeff, 1.0, input_signal)

end_time = time.perf_counter()

execution_time = end_time - start_time

print("\n3. FILTER SIMULATION")
print("-" * 40)
print("Input samples :", len(input_signal))
print("Output samples:", len(output_signal))
print(f"Execution time: {execution_time:.6f} seconds")

# ------------------------------------------------------------
# 4. PERFORMANCE PARAMETERS
# ------------------------------------------------------------

# Approximate hardware parameters for project analysis
multipliers = NUM_TAPS
adders = NUM_TAPS - 1

area_estimate = multipliers + adders

# Approximate critical path
critical_path = NUM_TAPS

# Throughput at one sample per clock
clock_frequency = 100e6
throughput = clock_frequency

print("\n4. HARDWARE ANALYSIS")
print("-" * 40)
print("Number of taps      :", NUM_TAPS)
print("Multipliers required:", multipliers)
print("Adders required     :", adders)
print("Area estimate       :", area_estimate, "units")
print("Clock frequency     :", clock_frequency / 1e6, "MHz")
print("Throughput          :", throughput / 1e6, "samples/sec")

# ------------------------------------------------------------
# 5. SAVE RESULTS
# ------------------------------------------------------------

results_file = RESULT_DIR / "results.txt"

with open(results_file, "w") as f:

    f.write("VLSI DESIGN OF FIR FILTER FOR DSP APPLICATIONS\n")
    f.write("=" * 55 + "\n\n")

    f.write("FILTER PARAMETERS\n")
    f.write(f"Number of taps : {NUM_TAPS}\n")
    f.write(f"Cutoff frequency : {CUTOFF}\n")
    f.write(f"Sampling frequency : {fs} Hz\n\n")

    f.write("FIXED-POINT COEFFICIENTS\n")
    f.write(str(fixed_coeff))
    f.write("\n\n")

    f.write("HARDWARE ANALYSIS\n")
    f.write(f"Multipliers : {multipliers}\n")
    f.write(f"Adders : {adders}\n")
    f.write(f"Area estimate : {area_estimate} units\n")
    f.write(f"Clock frequency : {clock_frequency / 1e6} MHz\n")
    f.write(f"Throughput : {throughput / 1e6} samples/sec\n")

print("\n5. RESULTS SAVED")
print("-" * 40)
print(results_file)

# ------------------------------------------------------------
# 6. INPUT AND OUTPUT GRAPH
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(t[:300], input_signal[:300], label="Input Signal")
plt.plot(t[:300], output_signal[:300], label="Filtered Output")

plt.title("FIR Filter Input and Output")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()

graph_file = RESULT_DIR / "fir_filter_output.png"
plt.savefig(graph_file, dpi=300)

print("Graph saved:", graph_file)

plt.show()

# ------------------------------------------------------------
# 7. FREQUENCY RESPONSE
# ------------------------------------------------------------

plt.figure(figsize=(10, 5))

w = np.linspace(0, np.pi, 512)
H = np.zeros(512, dtype=complex)

for k in range(NUM_TAPS):
    H += coeff[k] * np.exp(-1j * w * k)

frequency = w / np.pi

plt.plot(frequency, 20 * np.log10(np.maximum(np.abs(H), 1e-8)))

plt.title("FIR Filter Frequency Response")
plt.xlabel("Normalized Frequency")
plt.ylabel("Magnitude (dB)")
plt.grid(True)

response_file = RESULT_DIR / "frequency_response.png"
plt.savefig(response_file, dpi=300)

print("Frequency response saved:", response_file)

plt.show()

# ------------------------------------------------------------
# COMPLETE
# ------------------------------------------------------------

print("\n" + "=" * 55)
print("PROJECT EXECUTION COMPLETED SUCCESSFULLY")
print("=" * 55)

print("\nGenerated files:")
print("1. coefficients/coefficients.txt")
print("2. results/results.txt")
print("3. results/fir_filter_output.png")
print("4. results/frequency_response.png")