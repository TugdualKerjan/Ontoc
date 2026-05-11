# Integrated Systems TODO

A checklist of CPUs, GPUs, accelerators, and unconventional compute engines to integrate into the database one at a time.

## 1. General-purpose CPUs

### Mainframe lineage
- [x] IBM System/360 (1964)
- [ ] CDC 6600 (1964)
- [ ] DEC PDP-8
- [ ] DEC PDP-11
- [ ] DEC VAX

### Minicomputer → workstation
- [ ] DEC Alpha 21064
- [ ] MIPS R2000
- [ ] MIPS R3000
- [ ] HP PA-RISC
- [ ] Sun SPARC v8
- [ ] Sun SPARC v9

### x86 lineage
- [ ] Intel 8086
- [ ] Intel 286
- [ ] Intel 386
- [ ] Intel 486
- [ ] Intel Pentium
- [ ] Intel P6 (Pentium Pro)
- [ ] Intel Pentium 4 (NetBurst)
- [ ] Intel Core (Yonah)
- [ ] Intel Nehalem
- [ ] Intel Sandy Bridge
- [ ] Intel Haswell
- [ ] Intel Skylake
- [ ] AMD Zen
- [ ] AMD Zen 2
- [ ] AMD Zen 3
- [ ] AMD Zen 4
- [ ] Intel Alder Lake (hybrid)

### ARM lineage
- [ ] ARM2
- [ ] ARM6
- [ ] ARM7TDMI
- [ ] ARM9
- [ ] ARM Cortex-A8
- [ ] ARM Cortex-A9
- [ ] ARM Cortex-A15
- [ ] ARM Cortex-A53 (big.LITTLE)
- [ ] ARM Cortex-A57 (big.LITTLE)
- [ ] ARM Cortex-A72
- [ ] ARM Cortex-A76
- [ ] ARM Cortex-A78
- [ ] ARM Cortex-X1
- [ ] ARM Cortex-X2
- [ ] ARM Cortex-X4
- [ ] ARM Neoverse N1
- [ ] ARM Neoverse V1

### RISC-V
- [ ] SiFive U54
- [ ] SiFive U74
- [ ] SiFive X280
- [ ] Alibaba XuanTie C910
- [ ] Ventana Veyron

### PowerPC / POWER
- [ ] POWER1
- [ ] POWER2
- [ ] POWER3
- [ ] POWER4
- [ ] POWER5
- [ ] POWER6
- [ ] POWER7
- [ ] POWER8
- [ ] POWER9
- [ ] POWER10
- [ ] Apple G3
- [ ] Apple G4
- [ ] Apple G5
- [ ] Cell BE (heterogeneous outlier)

### Exotic / dead ends worth preserving
- [ ] Intel Itanium (EPIC/VLIW)
- [ ] Transmeta Crusoe (code morphing)
- [ ] Mill Computing (belt architecture)
- [ ] SPARC (Sun → Oracle → open-sourced)

## 2. Embedded & microcontroller cores

### Classic embedded
- [ ] Intel 8051 (1980)
- [ ] Microchip PIC10
- [ ] Microchip PIC12
- [ ] Microchip PIC16
- [ ] Microchip PIC18
- [ ] Microchip PIC24
- [ ] Microchip PIC32
- [ ] Atmel/Microchip AVR ATmega
- [ ] Atmel/Microchip AVR ATtiny
- [ ] Atmel/Microchip AVR32
- [ ] TI MSP430

### ARM Cortex-M
- [ ] ARM Cortex-M0
- [ ] ARM Cortex-M0+
- [ ] ARM Cortex-M3
- [ ] ARM Cortex-M4
- [ ] ARM Cortex-M7
- [ ] ARM Cortex-M33
- [ ] ARM Cortex-M55
- [ ] ARM Cortex-M85

### RISC-V embedded
- [ ] ESP32-C3
- [ ] ESP32-C6
- [ ] GD32VF

## 3. DSPs

- [ ] TI TMS320 C2000
- [ ] TI TMS320 C5000
- [ ] TI TMS320 C6000
- [ ] Qualcomm Hexagon
- [ ] Tensilica Xtensa
- [ ] CEVA DSP cores

## 4. GPUs (as compute engines)

### NVIDIA
- [ ] NVIDIA Tesla
- [ ] NVIDIA Fermi
- [ ] NVIDIA Kepler
- [ ] NVIDIA Maxwell
- [ ] NVIDIA Pascal
- [ ] NVIDIA Volta
- [ ] NVIDIA Turing
- [ ] NVIDIA Ampere
- [ ] NVIDIA Hopper
- [ ] NVIDIA Blackwell

### AMD
- [ ] AMD Terascale
- [ ] AMD GCN
- [ ] AMD RDNA
- [ ] AMD RDNA2
- [ ] AMD RDNA3
- [ ] AMD RDNA4
- [ ] AMD CDNA

### Intel
- [ ] Intel Xe-LP
- [ ] Intel Xe-HPG
- [ ] Intel Xe-HPC (Ponte Vecchio)
- [ ] Intel Xe2

### Others
- [ ] Apple GPU (in-house since M1)
- [ ] Imagination PowerVR
- [ ] ARM Mali T6xx
- [ ] ARM Mali G5x
- [ ] ARM Mali G7x
- [ ] ARM Mali G9x
- [ ] ARM Mali G12x

## 5. AI accelerators (NPUs / systolic arrays)

- [ ] Google TPU v1
- [ ] Google TPU v2
- [ ] Google TPU v3
- [ ] Google TPU v4
- [ ] Google TPU v5
- [ ] Apple ANE (Neural Engine)
- [ ] AWS Inferentia
- [ ] AWS Trainium
- [ ] Graphcore IPU
- [ ] Cerebras WSE
- [ ] SambaNova RDU
- [ ] Tenstorrent Grayskull
- [ ] Tenstorrent Wormhole
- [ ] Groq TSP
- [ ] Qualcomm Hexagon NPU

## 6. Unconventional / non-von Neumann

### Dataflow
- [ ] Manchester Dataflow
- [ ] MIT Tagged-Token

### Neuromorphic
- [ ] Intel Loihi 1
- [ ] Intel Loihi 2
- [ ] IBM TrueNorth
- [ ] BrainScaleS
- [ ] SpiNNaker

### Quantum
- [ ] IBM Eagle
- [ ] IBM Osprey
- [ ] IBM Condor
- [ ] Google Sycamore
- [ ] IonQ

### Analog / thermodynamic
- [ ] Normal Computing stochastic processing units
- [ ] IBM analog AI chip

### In-memory compute
- [ ] UPMEM PIM
- [ ] Samsung HBM-PIM

### Optical
- [ ] Lightmatter Passage
- [ ] Luminous Computing
