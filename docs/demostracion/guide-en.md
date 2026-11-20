# English · Guayaquil through radar

**English** · [Spanish](README.md)

[Interactive viewer](https://rxn1n.github.io/Illari/docs/demostracion/visor-en.html) · [Illustrated presentation (PDF)](https://rxn1n.github.io/Illari/docs/demostracion/ILLARI_Guayaquil_English.pdf) · [PowerPoint](ILLARI_Guayaquil_English.pptx) · [Download the standalone HTML](https://raw.githubusercontent.com/Dariuxcks/Illari/main/docs/demostracion/visor-en.html)

ILLARI uses real NISAR radar observations to investigate where the signal returned from the surface changed between two acquisitions. The worked example covers the same urban area of Guayaquil on **7 and 19 October 2026**. It lets a reader check the connection between the observations, the interactive comparison and the reported change. [Dancing with the SARs challenge brief](https://edeon.sonoma.edu/nasaspaceapps-26/index.html)

## Read the maps

1. The **before/after slider** reveals the 7 October image on the left and 19 October on the right. Both use the same greyscale. Choose **HH** to view horizontally transmitted and received radar, or **HV** for the vertically received component of a horizontally transmitted signal.
2. The **change map** subtracts 7 October from 19 October in decibels at each paired pixel. Blue indicates a weaker return on the later date, orange a stronger return. The colour scale saturates at −6 and +6 dB. Display images are reduced in size after calculation.
3. **Box A** identifies the same 500 × 500 m square on both panels, centred at 2.14843° S, 79.91730° W. Toggle **Show box A** to see the underlying pixels. The example was chosen to illustrate a local increase.

| Median paired change | Full urban crop (1,771,545 pixels) | Box A (2,500 pixels) |
|---|---:|---:|
| HH | +0.23 dB | +0.67 dB |
| HV | +0.13 dB | +0.64 dB |

Both observations are **NISAR L2 GCOV PROVISIONAL**, descending track 112, frame 090, acquisition mode 4005, polarization code DHDH. The HH and HV bands share a 1,335 × 1,327 grid in UTM zone 17S at 10 m spacing. The case viewer uses calibrated backscatter. The live dashboard separately displays NASA GIBS daily false-colour mosaics. [Acquisition IDs and provenance](../../CASO_NISAR_GUAYAQUIL.md) · [Reproduce the measurements](reproduce.md).

## Can the changes be attributed to flooding?

Surface moisture, vegetation and built structures can all influence radar return. In an exploratory check, the OPERA DSWx-S1 display mosaics from **6 and 18 October** each preceded the corresponding NISAR acquisition by one day. Of **1,413** equivalent cells marked as apparent new open water by OPERA, **7** also met the NISAR rule for a decrease in both channels. That is **0.50%** of those OPERA cells. The NISAR rule alone selected **5,265** cells.

This limited overlap describes agreement between two screening rules. Estimating flood extent or detector accuracy would require appropriate before/after observations, original WTR classes and quality masks, and an independent dated reference. The storm of **26 October** occurred after all four observations. [Method and results of the OPERA comparison (Spanish)](../../CASO_NISAR_OPERA_GUAYAQUIL.md).

Data: NASA–ISRO NISAR via ASF DAAC. [Project team](../../AUTHORS.md) · [AI assistance](../../USO_DE_IA.md).
