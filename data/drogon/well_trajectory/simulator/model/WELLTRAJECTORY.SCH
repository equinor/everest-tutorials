
RPTRST
  BASIC=4 / 

TUNING
 1* 30 /
/
/

INCLUDE
 '../../A1.SCH' /

INCLUDE
 '../../A2.SCH' /

INCLUDE
 '../../A3.SCH' /

INCLUDE
 '../../A4.SCH' /

INCLUDE
 '../../A5.SCH' /

INCLUDE
 '../../A6.SCH' /


WCONPROD
--WELL OP/SH   CTL       ORAT       WRAT       GRAT       LRAT       RRAT        BHP        THP   VFP        ALQ
 'A1'   SHUT  LRAT       3000       3000         1*       4000         1*        150         1*    1*         1* /
 'A2'   SHUT  LRAT       4000       4000         1*       2500         1*        150         1*    1*         1* /
 'A3'   SHUT  LRAT       4000       4000         1*       2500         1*        150         1*    1*         1* /
 'A4'   SHUT  LRAT       4000       4000         1*       4000         1*        150         1*    1*         1* /
/

WCONINJE
--WELL PHASE OP/SH   CTL       SRAT       RRAT        BHP        THP   VFP
 'A5'  WATER  SHUT  RATE       6500         1*        500         1*    1* /
 'A6'  WATER  SHUT  RATE       6500         1*        500         1*    1* /
/

DATES
 1 JAN 2023 /
/

WELOPEN
  'A1' 'OPEN' /
/

DATES
 1 APR 2023 /
/

DATES
 02 MAY 2023 /
/

WELOPEN
  'A2' 'OPEN' /
/

DATES
 1 JLY 2023 /
/

DATES
 31 AUG 2023 /
/

WELOPEN
  'A3' 'OPEN' /
/

DATES
 1 OCT 2023 /
/

DATES
 30 DEC 2023 /
/

WELOPEN
  'A4' 'OPEN' /
/

DATES
 1 JAN 2024 /
/

DATES
 1 APR 2024 /
/

DATES
 29 APR 2024 /
/

WELOPEN
  'A5' 'OPEN' /
/

DATES
 1 JLY 2024 /
/

DATES
 28 AUG 2024 /
/

WELOPEN
  'A6' 'OPEN' /
/

DATES
 1 OCT 2024 /
/

DATES
 1 JAN 2025 /
/

DATES
 1 APR 2025 /
/

DATES
 1 JLY 2025 /
/

DATES
 1 OCT 2025 /
/

DATES
 1 JAN 2026 /
/

DATES
 1 APR 2026 /
/

DATES
 1 JLY 2026 /
/

DATES
 1 OCT 2026 /
/

DATES
 1 JAN 2027 /
/

DATES
 1 APR 2027 /
/

DATES
 1 JLY 2027 /
/

DATES
 1 OCT 2027 /
/

DATES
 1 JAN 2028 /
/

DATES
 1 APR 2028 /
/

DATES
 1 JLY 2028 /
/

DATES
 1 OCT 2028 /
/

DATES
 1 JAN 2029 /
/

DATES
 1 APR 2029 /
/

DATES
 1 JLY 2029 /
/

DATES
 1 OCT 2029 /
/

DATES
 1 JAN 2030 /
/

END



