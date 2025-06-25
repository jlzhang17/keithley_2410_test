# keithley_2410_test
I–V measurements with a Keithley 2410 source-meter

June 6 Update:
In the afternoon, Shu Xian and I successfully used this program to test the IV curve of the silicon microstrip used in the Alibava system. The curve shape appeared relatively normal, but it showed a trend of breakdown around 150V, with a sharp increase in current. Upon comparison, we found that the breakdown voltage was lower than that shown in the test curve from the EASy system manual. We have contacted the manufacturer regarding this issue.

June 13 Evening:
No response has been received from the manufacturer yet.

June 23:
Finally the laser system arrived, waiting for testing.

June 25：
Connection Configuration:
The Keithley 2410 outputs a negative high voltage, with the following wiring:
1. 2410 OUTPUT HI -------- Alibava daughter board LEMO negative terminal (short wire ---) -------- Dark green wire -------- Bias ring (p⁺ strips) on the Si microstrip detector.
2. 2410 OUTPUT LO (GND) -------- Alibava daughter board LEMO positive terminal (long wire +++) -------- Red wire -------- n⁺ backside electrode of the Si microstrip detector.

Ensures the electric field direction is from n⁺ (backside) → p⁺ (strips, bias) (i.e., bottom to top). The n⁺ electrode remains at ground potential (0V), while the p⁺ strips are biased with negative voltage.
